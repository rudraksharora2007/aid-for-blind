"""Rich-backed application logging."""
import logging
from rich.logging import RichHandler


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return the root VisionAssist logger."""
    logger = logging.getLogger("visionassist")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, show_path=False)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    logger.propagate = False
    return logger
