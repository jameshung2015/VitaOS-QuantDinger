"""Monthly key events wrapper service.

Uses the external fin-event-agent folder as the primary execution surface and
normalizes its output for QuantDinger APIs.
"""
from __future__ import annotations

import importlib.util
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from app.data_providers.news import get_economic_calendar
from app.utils.logger import get_logger

logger = get_logger(__name__)

SH_TZ = ZoneInfo("Asia/Shanghai")
DEFAULT_HOST_AGENT_DIR = (
    r"D:\document\Obsidian\vaults\J-Workspace\AGI\Agents\projects\fin-event-agent"
)
DEFAULT_CONTAINER_AGENT_DIR = "/external/fin-event-agent"


def _china_now() -> datetime:
    return datetime.now(SH_TZ)


def _host_agent_dir() -> str:
    return os.getenv("FIN_EVENT_AGENT_HOST_DIR", DEFAULT_HOST_AGENT_DIR)


def _agent_dir() -> str:
    configured = str(os.getenv("FIN_EVENT_AGENT_DIR") or "").strip()
    if configured:
        return configured
    return DEFAULT_HOST_AGENT_DIR if os.name == "nt" else DEFAULT_CONTAINER_AGENT_DIR


def _result_path(agent_dir: str) -> str:
    return os.path.join(agent_dir, "data", "monthly_key_events_result.json")


def _parse_date(value: str) -> datetime | None:
    s = str(value or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            dt = datetime.strptime(s, fmt)
            if fmt == "%Y-%m":
                dt = dt.replace(day=1)
            return dt.replace(tzinfo=SH_TZ)
        except Exception:
            continue
    return None


def _fallback_items(days: int) -> List[Dict[str, Any]]:
    now = _china_now()
    end = now + timedelta(days=days)
    raw = get_economic_calendar() or []
    items: List[Dict[str, Any]] = []
    for idx, event in enumerate(raw):
        dt = _parse_date(event.get("date"))
        if not dt or bool(event.get("is_released")):
            continue
        if not (now.date() <= dt.date() <= end.date()):
            continue
        importance = str(event.get("importance") or "").lower()
        score = 5 if importance == "high" else (3 if importance == "medium" else 2)
        items.append({
            "event_id": str(event.get("id") or f"fallback_{idx+1}"),
            "date": str(event.get("date") or ""),
            "time": str(event.get("time") or ""),
            "title": str(event.get("name") or event.get("name_en") or ""),
            "region": str(event.get("country") or "GLOBAL"),
            "importance": score,
            "bias": str(event.get("expected_impact") or "neutral"),
            "reason": str(event.get("impact_desc") or ""),
        })
    items.sort(key=lambda x: (x.get("date") or "", -int(x.get("importance") or 0)))
    return items[:8]


def _fallback_payload(days: int, language: str, agent_dir: str) -> Dict[str, Any]:
    items = _fallback_items(days)
    summary = "未来一个月重点事件，已按中国时间窗口筛选。" if items else "未来一个月暂无可提取的重点事件。"
    return {
        "summary": summary,
        "items": items,
        "agent": {
            "name": "fin-event-agent",
            "agent_dir": agent_dir,
            "host_agent_dir": _host_agent_dir(),
            "result_path": _result_path(agent_dir),
            "model_provider": "fallback",
            "model_name": "rule-based",
            "source_mode": "internal_fallback",
            "timezone": "Asia/Shanghai",
        },
        "window_days": days,
        "generated_at": _china_now().isoformat(),
        "language": language,
    }


def _load_external_agent(agent_dir: str):
    entry = os.path.join(agent_dir, "app.py")
    if not os.path.exists(entry):
        raise FileNotFoundError(f"fin-event-agent app.py not found: {entry}")
    spec = importlib.util.spec_from_file_location("fin_event_agent_runtime", entry)
    if not spec or not spec.loader:
        raise ImportError(f"Unable to load fin-event-agent entry: {entry}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "generate_monthly_key_events"):
        raise AttributeError("fin-event-agent app.py missing generate_monthly_key_events")
    return module


def _normalize_items(items: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not isinstance(items, list):
        return normalized
    for item in items[:8]:
        if not isinstance(item, dict):
            continue
        normalized.append({
            "event_id": str(item.get("event_id") or ""),
            "date": str(item.get("date") or ""),
            "time": str(item.get("time") or ""),
            "title": str(item.get("title") or ""),
            "region": str(item.get("region") or ""),
            "importance": int(item.get("importance") or 0),
            "bias": str(item.get("bias") or "neutral"),
            "reason": str(item.get("reason") or ""),
        })
    return normalized


def _normalize_payload(payload: Dict[str, Any], days: int, language: str, agent_dir: str) -> Dict[str, Any]:
    agent = payload.get("agent") if isinstance(payload.get("agent"), dict) else {}
    return {
        "summary": str(payload.get("summary") or ""),
        "items": _normalize_items(payload.get("items")),
        "agent": {
            "name": str(agent.get("name") or "fin-event-agent"),
            "agent_dir": str(agent.get("agent_dir") or agent_dir),
            "host_agent_dir": str(agent.get("host_agent_dir") or _host_agent_dir()),
            "result_path": str(agent.get("result_path") or _result_path(agent_dir)),
            "model_provider": str(agent.get("model_provider") or ""),
            "model_name": str(agent.get("model_name") or ""),
            "source_mode": str(agent.get("source_mode") or "external_agent"),
            "timezone": str(agent.get("timezone") or "Asia/Shanghai"),
        },
        "window_days": int(payload.get("window_days") or days),
        "generated_at": str(payload.get("generated_at") or _china_now().isoformat()),
        "language": str(payload.get("language") or language),
    }


def extract_monthly_key_events(days: int = 30, language: str = "zh-CN") -> Dict[str, Any]:
    days = max(1, min(int(days or 30), 60))
    agent_dir = _agent_dir()
    try:
        module = _load_external_agent(agent_dir)
        payload = module.generate_monthly_key_events(days=days, language=language, agent_dir=agent_dir)
        if isinstance(payload, dict):
            normalized = _normalize_payload(payload, days, language, agent_dir)
            if normalized["summary"] and normalized["items"]:
                return normalized
    except Exception as e:
        logger.warning(f"fin-event-agent execution failed, fallback to internal provider: {e}")

    return _fallback_payload(days, language, agent_dir)
