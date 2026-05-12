"""
Tushare Pro helpers for China A-share historical K-lines.

Used only for CNStock historical bars. Real-time quote paths remain unchanged.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import requests

from app.config import APIKeys
from app.data_sources.asia_stock_kline import _merge_every_n_sorted_bars
from app.utils.logger import get_logger

logger = get_logger(__name__)

_TUSHARE_URL = "http://api.waditu.com"
_TRUTHY = {"1", "true", "yes", "on"}

_TIMEFRAME_SPECS: Dict[str, Dict[str, Any]] = {
    "1m": {"api_name": "stk_mins", "freq": "1min", "time_field": "trade_time", "merge": 1},
    "5m": {"api_name": "stk_mins", "freq": "5min", "time_field": "trade_time", "merge": 1},
    "15m": {"api_name": "stk_mins", "freq": "15min", "time_field": "trade_time", "merge": 1},
    "30m": {"api_name": "stk_mins", "freq": "30min", "time_field": "trade_time", "merge": 1},
    "1H": {"api_name": "stk_mins", "freq": "60min", "time_field": "trade_time", "merge": 1},
    "4H": {"api_name": "stk_mins", "freq": "60min", "time_field": "trade_time", "merge": 4},
    "1D": {"api_name": "daily", "time_field": "trade_date", "merge": 1},
    "1W": {"api_name": "weekly", "time_field": "trade_date", "merge": 1},
}


def _tushare_enabled() -> bool:
    raw = (os.getenv("ENABLE_TUSHARE") or "").strip().lower()
    if raw:
        return raw in _TRUTHY
    try:
        from app.utils.config_loader import load_addon_config

        enabled = load_addon_config().get("tushare", {}).get("enabled")
        if enabled is None:
            return False
        return bool(enabled)
    except Exception:
        return False


def normalize_tushare_code(symbol: str) -> str:
    s = (symbol or "").strip().upper()
    if not s:
        return s
    if s.endswith(".SH") or s.endswith(".SZ"):
        return s
    if s.endswith(".SS"):
        return s[:-3] + ".SH"
    if s.startswith("SH") and len(s) >= 8:
        return s[2:] + ".SH"
    if s.startswith("SZ") and len(s) >= 8:
        return s[2:] + ".SZ"
    if s.isdigit() and len(s) == 6:
        return s + (".SH" if s.startswith("6") else ".SZ")
    return s


def _request_window(timeframe: str, limit: int, before_time: Optional[int], merge_factor: int) -> Tuple[str, str]:
    effective_limit = max(int(limit or 1), 1) * max(int(merge_factor or 1), 1)
    end_dt = datetime.fromtimestamp(int(before_time)) if before_time else datetime.now()
    if timeframe == "1m":
        delta = timedelta(days=max(2, (effective_limit // 240) + 2))
    elif timeframe == "5m":
        delta = timedelta(days=max(3, (effective_limit // 48) + 3))
    elif timeframe == "15m":
        delta = timedelta(days=max(5, effective_limit + 3))
    elif timeframe == "30m":
        delta = timedelta(days=max(8, effective_limit + 5))
    elif timeframe in ("1H", "4H"):
        delta = timedelta(days=max(20, effective_limit * 2 + 10))
    elif timeframe == "1W":
        delta = timedelta(days=max(120, effective_limit * 7 + 30))
    else:
        delta = timedelta(days=max(60, effective_limit + 30))

    start_dt = end_dt - delta
    return start_dt.strftime("%Y%m%d"), end_dt.strftime("%Y%m%d")


def _parse_ts(raw_value: Any) -> Optional[int]:
    raw = str(raw_value or "").strip()
    if not raw:
        return None
    for fmt in (
        "%Y%m%d",
        "%Y-%m-%d",
        "%Y%m%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
    ):
        try:
            return int(datetime.strptime(raw, fmt).timestamp())
        except ValueError:
            continue
    return None


def _request_tushare(api_name: str, token: str, params: Dict[str, Any], fields: str) -> Dict[str, Any]:
    resp = requests.post(
        _TUSHARE_URL,
        json={
            "api_name": api_name,
            "token": token,
            "params": params,
            "fields": fields,
        },
        timeout=20,
    )
    return resp.json() if resp.text else {}


def fetch_tushare_klines(
    *,
    symbol: str,
    timeframe: str,
    limit: int,
    before_time: Optional[int],
) -> List[Dict[str, Any]]:
    if not _tushare_enabled():
        return []

    token = (APIKeys.TUSHARE_TOKEN or "").strip()
    if not token:
        logger.info("ENABLE_TUSHARE is on but TUSHARE_TOKEN is empty; skipping Tushare")
        return []

    spec = _TIMEFRAME_SPECS.get(timeframe)
    if not spec:
        return []

    ts_code = normalize_tushare_code(symbol)
    merge_factor = int(spec.get("merge") or 1)
    start_date, end_date = _request_window(timeframe, limit, before_time, merge_factor)

    params: Dict[str, Any] = {
        "ts_code": ts_code,
        "start_date": start_date,
        "end_date": end_date,
    }
    if spec.get("freq"):
        params["freq"] = spec["freq"]

    fields = f"{spec['time_field']},open,high,low,close,vol"

    try:
        payload = _request_tushare(spec["api_name"], token, params, fields)
    except Exception as exc:
        logger.warning("Tushare request failed for %s tf=%s: %s", ts_code, timeframe, exc)
        return []

    code = payload.get("code", -1)
    if int(code) != 0:
        logger.warning(
            "Tushare error for %s tf=%s: code=%s msg=%s",
            ts_code,
            timeframe,
            code,
            payload.get("msg"),
        )
        return []

    data = payload.get("data") or {}
    field_names = data.get("fields") or []
    items = data.get("items") or []
    if not field_names or not items:
        return []

    out: List[Dict[str, Any]] = []
    for item in items:
        try:
            row = dict(zip(field_names, item))
            ts = _parse_ts(row.get(spec["time_field"]))
            if ts is None:
                continue
            open_ = float(row.get("open") or 0)
            high = float(row.get("high") or 0)
            low = float(row.get("low") or 0)
            close = float(row.get("close") or 0)
            volume = float(row.get("vol") or 0)
            if open_ == 0 and close == 0:
                continue
            out.append(
                {
                    "time": ts,
                    "open": round(open_, 4),
                    "high": round(high, 4),
                    "low": round(low, 4),
                    "close": round(close, 4),
                    "volume": round(volume, 2),
                }
            )
        except Exception:
            continue

    out.sort(key=lambda row: row["time"])
    if merge_factor > 1 and out:
        out = _merge_every_n_sorted_bars(out, merge_factor)
    logger.debug("Tushare returned %d bars for %s tf=%s", len(out), ts_code, timeframe)
    return out
