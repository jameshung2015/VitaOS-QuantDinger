from app.data_sources.cn_stock import CNStockDataSource
from app.data_sources.tushare import fetch_tushare_klines, normalize_tushare_code


def test_normalize_tushare_code_accepts_common_cn_formats():
    assert normalize_tushare_code("600519") == "600519.SH"
    assert normalize_tushare_code("600519.SH") == "600519.SH"
    assert normalize_tushare_code("600519.SS") == "600519.SH"
    assert normalize_tushare_code("SZ000001") == "000001.SZ"


def test_fetch_tushare_klines_parses_daily_response(monkeypatch):
    class FakeResponse:
        text = "ok"

        @staticmethod
        def json():
            return {
                "code": 0,
                "data": {
                    "fields": ["trade_date", "open", "high", "low", "close", "vol"],
                    "items": [
                        ["20260509", "148.50", "150.20", "147.80", "149.90", "123456.0"],
                        ["20260508", "147.10", "149.00", "146.50", "148.20", "113000.0"],
                    ],
                },
            }

    calls = []

    def fake_post(url, json=None, timeout=None):
        calls.append({"url": url, "json": json, "timeout": timeout})
        return FakeResponse()

    monkeypatch.setenv("ENABLE_TUSHARE", "true")
    monkeypatch.setenv("TUSHARE_TOKEN", "test-token")
    monkeypatch.setattr("app.data_sources.tushare.requests.post", fake_post)

    rows = fetch_tushare_klines(symbol="600519.SH", timeframe="1D", limit=2, before_time=None)

    assert [row["close"] for row in rows] == [148.2, 149.9]
    assert calls[0]["json"]["api_name"] == "daily"
    assert calls[0]["json"]["params"]["ts_code"] == "600519.SH"


def test_cn_stock_uses_tushare_before_other_fallbacks(monkeypatch):
    tushare_rows = [{"time": 1715212800, "open": 1.0, "high": 1.2, "low": 0.9, "close": 1.1, "volume": 100.0}]

    def fail_if_called(*args, **kwargs):
        raise AssertionError("fallback should not run when tushare returned rows")

    monkeypatch.setattr("app.data_sources.cn_stock.fetch_tushare_klines", lambda **kwargs: tushare_rows)
    monkeypatch.setattr("app.data_sources.cn_stock.fetch_twelvedata_klines", fail_if_called)

    rows = CNStockDataSource().get_kline("600519.SH", "1D", 10)

    assert rows == tushare_rows


def test_cn_stock_falls_back_when_tushare_returns_empty(monkeypatch):
    tencent_rows = [["2026-05-09", "1.0", "1.1", "1.2", "0.9", "100"]]

    monkeypatch.setattr("app.data_sources.cn_stock.fetch_tushare_klines", lambda **kwargs: [])
    monkeypatch.setattr("app.data_sources.cn_stock.fetch_twelvedata_klines", lambda **kwargs: [])
    monkeypatch.setattr("app.data_sources.cn_stock.fetch_kline", lambda *args, **kwargs: tencent_rows)

    rows = CNStockDataSource().get_kline("600519.SH", "1D", 10)

    assert rows[0]["close"] == 1.1