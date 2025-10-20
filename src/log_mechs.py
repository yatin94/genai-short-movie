from pathlib import Path
import logging
import os

# Ensure logs directory exists
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def get_user_logger(user_id: str) -> logging.Logger:
    """
    Return a logger that writes to logs/<user_id>.log and to console.
    Safe to call multiple times; handlers won't be duplicated.
    """
    name = f"{__name__}.{user_id}"
    logger = logging.getLogger(name)

    if getattr(logger, "_user_logger_configured", False):
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    file_path = str(LOGS_DIR / f"{user_id}.log")
    fh = logging.FileHandler(file_path, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Avoid propagating to root handlers to prevent duplicate logs
    logger.propagate = False
    logger._user_logger_configured = True

    return logger

# Default module logger (writes to logs/default.log). Use get_user_logger(user_id) elsewhere.
logger = get_user_logger("default")