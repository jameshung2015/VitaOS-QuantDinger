"""Live quality gate for /api/global-market/monthly-key-events.

Usage:
  python tests/run_monthly_key_events_quality.py

Optional env vars:
  QD_API_BASE_URL=http://localhost:5000
  QD_ADMIN_USER=quantdinger
  QD_ADMIN_PASSWORD=123456
  QD_MONTHLY_DAYS=30
    QD_MIN_ITEMS=3
  QD_REQUEST_TIMEOUT=120
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Dict, List

import requests

DATE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")


def _env(name: str, default: str) -> str:
    v = os.getenv(name)
    if v is None:
        return default
    v = str(v).strip()
    return v if v else default


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def _warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def _ok(msg: str) -> None:
    print(f"[OK] {msg}")


def _login(base_url: str, username: str, password: str) -> str:
    url = f"{base_url}/api/auth/login"
    resp = requests.post(url, json={"username": username, "password": password}, timeout=20)
    if resp.status_code != 200:
        _fail(f"Login HTTP {resp.status_code}: {resp.text[:300]}")
    body = resp.json()
    if body.get("code") != 1:
        _fail(f"Login code={body.get('code')} msg={body.get('msg')}")
    token = (((body.get("data") or {}).get("token")) or "").strip()
    if not token:
        _fail("Login token is empty")
    return token


def _validate_item(item: Dict[str, Any], idx: int, errors: List[str], warnings: List[str]) -> None:
    title = str(item.get("title") or "").strip()
    reason = str(item.get("reason") or "").strip()
    date = str(item.get("date") or "").strip()
    bias = str(item.get("bias") or "").strip()

    try:
        importance = int(item.get("importance") or 0)
    except Exception:
        importance = 0

    if not title:
        errors.append(f"items[{idx}].title is empty")
    if not date:
        errors.append(f"items[{idx}].date is empty")
    elif not DATE_RE.match(date):
        warnings.append(f"items[{idx}].date malformed: {date}")

    if importance < 1 or importance > 5:
        warnings.append(f"items[{idx}].importance out of range 1-5: {importance}")

    if not bias:
        warnings.append(f"items[{idx}].bias is empty")
    if not reason:
        warnings.append(f"items[{idx}].reason is empty")


def main() -> int:
    base_url = _env("QD_API_BASE_URL", "http://localhost:5000").rstrip("/")
    username = _env("QD_ADMIN_USER", "quantdinger")
    password = _env("QD_ADMIN_PASSWORD", "123456")
    days = int(_env("QD_MONTHLY_DAYS", "30"))
    min_items = int(_env("QD_MIN_ITEMS", "3"))
    request_timeout = int(_env("QD_REQUEST_TIMEOUT", "120"))

    print("[INFO] Running monthly key events quality gate")
    print(f"[INFO] base_url={base_url}, days={days}, min_items={min_items}, request_timeout={request_timeout}")

    health = requests.get(f"{base_url}/api/health", timeout=15)
    if health.status_code != 200:
        _fail(f"Health HTTP {health.status_code}")
    _ok("Backend health passed")

    token = _login(base_url, username, password)
    _ok("Login passed")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept-Language": "zh-CN",
    }
    url = f"{base_url}/api/global-market/monthly-key-events"
    resp = requests.get(url, headers=headers, params={"days": days, "force": 1}, timeout=request_timeout)
    if resp.status_code != 200:
        _fail(f"monthly-key-events HTTP {resp.status_code}: {resp.text[:300]}")

    body = resp.json()
    if body.get("code") != 1:
        _fail(f"monthly-key-events code={body.get('code')} msg={body.get('msg')}")

    data = body.get("data") or {}
    summary = str(data.get("summary") or "").strip()
    items = data.get("items") if isinstance(data.get("items"), list) else []
    agent = data.get("agent") if isinstance(data.get("agent"), dict) else {}
    generated_at = str(data.get("generated_at") or "").strip()

    if not summary:
        _fail("data.summary is empty")
    _ok("summary is non-empty")

    if len(items) < min_items:
        _fail(f"items length {len(items)} < required minimum {min_items}")
    _ok(f"items length check passed ({len(items)})")

    required_agent_keys = ["agent_dir", "result_path", "model_provider", "model_name", "timezone"]
    missing = [k for k in required_agent_keys if not str(agent.get(k) or "").strip()]
    if missing:
        _fail(f"agent metadata missing: {', '.join(missing)}")
    _ok("agent metadata check passed")

    if agent.get("timezone") != "Asia/Shanghai":
        _fail(f"timezone mismatch: {agent.get('timezone')}")
    _ok("timezone check passed")

    if not generated_at or "+08:00" not in generated_at:
        _fail(f"generated_at is not China time: {generated_at}")
    _ok("generated_at China time check passed")

    result_path = str(agent.get("result_path") or "").strip()
    if not result_path:
        _fail("result_path is empty")
    if os.path.exists(result_path):
        _ok(f"agent result file exists: {result_path}")
    else:
        _warn(f"agent result file not visible on current host path: {result_path}")

    errors: List[str] = []
    warnings: List[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{i}] is not object")
            continue
        _validate_item(item, i, errors, warnings)

    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        _fail("quality gate failed due to hard errors")

    for w in warnings:
        _warn(w)

    print("[INFO] First 3 items:")
    for i, it in enumerate(items[:3]):
        print(
            f"  {i+1}. {it.get('date', '--')} {it.get('time', '--')} | {it.get('title', '--')} | "
            f"importance={it.get('importance', '--')} | bias={it.get('bias', '--')}"
        )

    out_path = os.path.join(os.path.dirname(__file__), "monthly_key_events_last_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
    _ok(f"Saved raw response to {out_path}")

    if warnings:
        print(f"[INFO] quality gate passed with {len(warnings)} warning(s)")
    else:
        print("[INFO] quality gate passed with no warnings")

    return 0


if __name__ == "__main__":
    sys.exit(main())
