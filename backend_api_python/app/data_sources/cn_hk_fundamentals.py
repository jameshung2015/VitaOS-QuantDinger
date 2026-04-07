"""
A-share / HK share fundamentals — multi-tier fallback.

Priority (when TWELVE_DATA_API_KEY configured):
  Twelve Data /statistics + /profile  →  AkShare (Eastmoney, fragile overseas)

Without API key:
  AkShare only (may fail from overseas servers)

Keys are aligned with MarketDataCollector expectations (pe_ratio, pb_ratio, etc.).
"""

from __future__ import annotations

import math
import time
from typing import Any, Dict, Optional

import requests

from app.data_sources.asia_stock_kline import (
    _get_twelve_data_api_key,
    _td_symbol_and_exchange,
    ak_a_code_from_tencent,
    ak_hk_code_from_tencent,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)

_TD_TIMEOUT = 15
_TD_MAX_ATTEMPTS = 2
_TD_BACKOFF_SEC = 2.0


def _float_clean(x: Any) -> Optional[float]:
    if x is None or x == "":
        return None
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Twelve Data fundamentals (globally stable, paid)
# ---------------------------------------------------------------------------

def _td_request(endpoint: str, symbol: str, exchange: str) -> Optional[Dict[str, Any]]:
    """Generic Twelve Data GET with retry."""
    api_key = _get_twelve_data_api_key()
    if not api_key:
        return None
    url = f"https://api.twelvedata.com{endpoint}"
    params = {"symbol": symbol, "exchange": exchange, "apikey": api_key}
    for attempt in range(_TD_MAX_ATTEMPTS):
        try:
            resp = requests.get(url, params=params, timeout=_TD_TIMEOUT)
            data = resp.json()
            if data.get("status") == "error":
                code = data.get("code", "")
                msg = (data.get("message") or "")[:120]
                if code == 429 or "API credits" in msg or "minute limit" in msg:
                    logger.warning("TwelveData rate limit on %s %s/%s: %s", endpoint, symbol, exchange, msg)
                else:
                    logger.debug("TwelveData %s error %s/%s: %s", endpoint, symbol, exchange, msg)
                return None
            return data
        except Exception as e:
            if attempt + 1 < _TD_MAX_ATTEMPTS:
                time.sleep(_TD_BACKOFF_SEC)
                continue
            logger.warning("TwelveData %s request failed %s/%s: %s", endpoint, symbol, exchange, e)
    return None


def fetch_twelvedata_fundamental(tencent_code: str, is_hk: bool) -> Dict[str, Any]:
    """Fetch PE/PB/PS/PEG/ROE/margin/market_cap/52w from Twelve Data /statistics."""
    symbol, exchange = _td_symbol_and_exchange(tencent_code, is_hk)
    data = _td_request("/statistics", symbol, exchange)
    if not data or "statistics" not in data:
        return {}

    stats = data["statistics"]
    result: Dict[str, Any] = {"source": "twelvedata"}

    vm = stats.get("valuations_metrics") or {}
    result["market_cap"] = _float_clean(vm.get("market_capitalization"))
    result["pe_ratio"] = _float_clean(vm.get("trailing_pe"))
    result["forward_pe"] = _float_clean(vm.get("forward_pe"))
    result["pb_ratio"] = _float_clean(vm.get("price_to_book_mrq"))
    result["ps_ratio"] = _float_clean(vm.get("price_to_sales_ttm"))
    result["peg"] = _float_clean(vm.get("peg_ratio"))
    result["enterprise_value"] = _float_clean(vm.get("enterprise_value"))

    fin = stats.get("financials") or {}
    result["profit_margin"] = _float_clean(fin.get("profit_margin"))
    result["gross_margin"] = _float_clean(fin.get("gross_margin"))
    result["operating_margin"] = _float_clean(fin.get("operating_margin"))
    result["roe"] = _float_clean(fin.get("return_on_equity_ttm"))
    result["roa"] = _float_clean(fin.get("return_on_assets_ttm"))

    ss = stats.get("stock_statistics") or {}
    result["total_shares"] = _float_clean(ss.get("shares_outstanding"))
    result["float_shares"] = _float_clean(ss.get("float_shares"))

    sp = stats.get("stock_price_summary") or {}
    result["52w_high"] = _float_clean(sp.get("fifty_two_week_high"))
    result["52w_low"] = _float_clean(sp.get("fifty_two_week_low"))
    result["beta"] = _float_clean(sp.get("beta"))

    div = stats.get("dividends_and_splits") or {}
    result["dividend_yield"] = _float_clean(div.get("trailing_annual_dividend_yield"))
    result["dividend_rate"] = _float_clean(div.get("trailing_annual_dividend_rate"))

    non_null = sum(1 for v in result.values() if v is not None and v != "twelvedata")
    logger.debug("TwelveData /statistics %s/%s: %d non-null fields", symbol, exchange, non_null)
    return result


def fetch_twelvedata_profile(tencent_code: str, is_hk: bool) -> Dict[str, Any]:
    """Fetch company info from Twelve Data /profile."""
    symbol, exchange = _td_symbol_and_exchange(tencent_code, is_hk)
    data = _td_request("/profile", symbol, exchange)
    if not data or not data.get("name"):
        return {}

    out: Dict[str, Any] = {"source": "twelvedata"}
    for src, dst in (
        ("name", "name"),
        ("industry", "industry"),
        ("sector", "sector"),
        ("website", "website"),
        ("description", "description"),
        ("employees", "employees"),
        ("name", "full_name"),
    ):
        v = data.get(src)
        if v is not None and str(v).strip():
            out[dst] = str(v).strip() if isinstance(v, str) else v

    country = data.get("country")
    if country:
        out["country"] = country

    logger.debug("TwelveData /profile %s/%s: name=%s industry=%s", symbol, exchange, out.get("name"), out.get("industry"))
    return out


# ---------------------------------------------------------------------------
# AkShare fundamentals (Eastmoney — fragile overseas, used as fallback)
# ---------------------------------------------------------------------------

def _eastmoney_a_em_symbol(tencent_code: str) -> str:
    c = ak_a_code_from_tencent(tencent_code)
    c = (c or "").zfill(6)
    if c.startswith("6"):
        return "SH" + c
    return "SZ" + c


def _individual_info_map(symbol_6: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    try:
        import akshare as ak  # type: ignore
        df = ak.stock_individual_info_em(symbol=symbol_6)
    except Exception as e:
        logger.debug("stock_individual_info_em failed %s: %s", symbol_6, e)
        return out
    if df is None or getattr(df, "empty", True) or len(df.columns) < 2:
        return out
    kcol, vcol = df.columns[0], df.columns[1]
    for _, row in df.iterrows():
        try:
            k = str(row[kcol]).strip()
            if k:
                out[k] = row[vcol]
        except Exception:
            continue
    return out


def fetch_cn_fundamental_akshare(tencent_code: str) -> Dict[str, Any]:
    """PE/PB/PS, market cap, ROE proxy, EPS for A-share (best-effort)."""
    sym6 = ak_a_code_from_tencent(tencent_code)
    if not sym6:
        return {}
    result: Dict[str, Any] = {"source": "akshare_em"}
    info = _individual_info_map(sym6)
    if info:
        result["market_cap"] = _float_clean(info.get("总市值"))
        result["float_market_cap"] = _float_clean(info.get("流通市值"))
        ind = info.get("行业")
        if ind is not None and str(ind).strip():
            result["industry"] = str(ind).strip()
        result["total_shares"] = _float_clean(info.get("总股本"))
        result["float_shares"] = _float_clean(info.get("流通股"))

    em_sym = _eastmoney_a_em_symbol(tencent_code)
    try:
        import akshare as ak  # type: ignore
        vdf = ak.stock_zh_valuation_comparison_em(symbol=em_sym)
    except Exception as e:
        logger.debug("stock_zh_valuation_comparison_em failed %s: %s", em_sym, e)
        vdf = None

    if vdf is not None and not vdf.empty and "代码" in vdf.columns:
        hit = vdf[vdf["代码"].astype(str).str.replace(".0", "", regex=False).str.zfill(6) == sym6.zfill(6)]
        if not hit.empty:
            r = hit.iloc[0]
            pe = _float_clean(r.get("市盈率-TTM"))
            if pe is not None:
                result["pe_ratio"] = pe
            pb = _float_clean(r.get("市净率-MRQ"))
            if pb is not None:
                result["pb_ratio"] = pb
            ps = _float_clean(r.get("市销率-TTM"))
            if ps is not None:
                result["ps_ratio"] = ps
            peg = _float_clean(r.get("PEG"))
            if peg is not None:
                result["peg"] = peg

    return result


def fetch_hk_fundamental_akshare(tencent_code: str) -> Dict[str, Any]:
    hk5 = ak_hk_code_from_tencent(tencent_code)
    if not hk5:
        return {}
    result: Dict[str, Any] = {"source": "akshare_em"}
    try:
        import akshare as ak  # type: ignore
        df = ak.stock_hk_financial_indicator_em(symbol=hk5)
    except Exception as e:
        logger.debug("stock_hk_financial_indicator_em failed %s: %s", hk5, e)
        return result
    if df is None or df.empty:
        return result
    r = df.iloc[0]
    result["pe_ratio"] = _float_clean(r.get("市盈率"))
    result["pb_ratio"] = _float_clean(r.get("市净率"))
    result["eps"] = _float_clean(r.get("基本每股收益(元)"))
    result["roe"] = _float_clean(r.get("股东权益回报率(%)"))
    result["profit_margin"] = _float_clean(r.get("销售净利率(%)"))
    mcap = _float_clean(r.get("总市值(港元)")) or _float_clean(r.get("港股市值(港元)"))
    if mcap is not None:
        result["market_cap"] = mcap
    result["dividend_yield"] = _float_clean(r.get("股息率TTM(%)"))
    return result


def fetch_cn_company_extras(tencent_code: str) -> Dict[str, Any]:
    sym6 = ak_a_code_from_tencent(tencent_code)
    if not sym6:
        return {}
    info = _individual_info_map(sym6)
    out: Dict[str, Any] = {}
    if info.get("行业"):
        out["industry"] = str(info["行业"]).strip()
    if info.get("上市时间"):
        out["ipo_date"] = str(info["上市时间"]).strip()
    return out


def fetch_hk_company_extras(tencent_code: str) -> Dict[str, Any]:
    hk5 = ak_hk_code_from_tencent(tencent_code)
    if not hk5:
        return {}
    out: Dict[str, Any] = {}
    try:
        import akshare as ak  # type: ignore
        df = ak.stock_hk_company_profile_em(symbol=hk5)
    except Exception as e:
        logger.debug("stock_hk_company_profile_em failed %s: %s", hk5, e)
        return out
    if df is None or df.empty:
        return out
    r = df.iloc[0]
    for key, col in (
        ("industry", "所属行业"),
        ("ipo_date", "公司成立日期"),
        ("website", "公司网址"),
        ("full_name", "公司名称"),
    ):
        v = r.get(col)
        if v is not None and str(v).strip():
            out[key] = str(v).strip()
    return out
