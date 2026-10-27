import json
import logging
from pathlib import Path
from datetime import datetime, timezone


LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "petition_monitoring.log"

logger = logging.getLogger("petition_monitoring")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def log_workflow_event(
    event: str,
    petition_id: str,
    status: str,
    details: dict | None = None,
) -> None:
    """Write a structured workflow event to the monitoring log."""

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "petition_id": petition_id,
        "status": status,
        "details": details or {},
    }

    logger.info(json.dumps(record, ensure_ascii=False))