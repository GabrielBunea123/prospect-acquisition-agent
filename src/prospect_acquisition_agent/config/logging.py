import logging
import sys

from src.prospect_acquisition_agent.config.settings import LoggingSettings
from src.prospect_acquisition_agent.helper.context import get_trace_id


class TraceIdFilter(logging.Filter):
    """Logging filter that adds trace_id to log records"""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add trace_id to the log record if available
        :param record: The log to filter
        :return: True to allow the record to be filtered
        """
        record.trace_id = get_trace_id()
        return True


def setup_logging(settings: LoggingSettings) -> None:
    """
    Configure the logging with trace ID support
    :param settings:  logging settings
    :return:
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [trace_id=%(trace_id)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    handler.addFilter(TraceIdFilter())

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.level)

    # override uvicorn logger
    for name in logging.root.manager.loggerDict:
        if name in ("uvicorn"):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.addHandler(handler)
            uvicorn_logger.setLevel(settings.level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
