import logging
import sys
import time
from typing import Any, Dict
import json

class StructuredFormatter(logging.Formatter):
    """
    Custom formatter to output logs in a structured (JSON-like) format.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "request_id": getattr(record, "request_id", "N/A"),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

def setup_logging():
    """
    Configure the root logger with our structured formatter.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)

    # Optional: Suppress noisy third-party logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
