import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

import structlog
from structlog.types import EventDict, Processor

# Base JSON event fields (never dropped)
_BASE_KEYS: frozenset[str] = frozenset({
    'timestamp',
    'level',
    'logger',
    'event',
    'exception',
    'stack',
})

# Fields the shipped ErrorHandler itself relies on — not user configurable
_INTERNAL_KEYS: tuple[str, ...] = ('error_code',)

# Fields allowed to pass through extra=... into JSON
_EXTRA_WHITELIST: tuple[str, ...] = (
    'log_file',
    # Example
    # 'run_id',
    # 'step',
    # 'tool',
    # 'latency_ms',
)

_ALLOWED_KEYS = _BASE_KEYS | frozenset(_INTERNAL_KEYS) | frozenset(_EXTRA_WHITELIST)


def _add_whitelisted_extras(_logger: Any, _method_name: str, event_dict: EventDict) -> EventDict:
    """
    Copy whitelisted LogRecord fields into event_dict.

    _INTERNAL_KEYS are copied unconditionally: the shipped ErrorHandler relies on error_code, and that
    contract must not depend on whether the user whitelist is empty.

    Args:
        _logger (Any): structlog logger (unused).
        _method_name (str): Logging method name (unused).
        event_dict (EventDict): Current structlog event dictionary.

    Returns:
        EventDict: The same event dictionary, enriched with whitelisted extras.
    """
    record = event_dict.get('_record')
    if record is None:
        return event_dict

    for key in (*_INTERNAL_KEYS, *_EXTRA_WHITELIST):
        value = record.__dict__.get(key)
        if value is not None:
            event_dict[key] = value

    return event_dict


def _filter_event_dict(_logger: Any, _method_name: str, event_dict: EventDict) -> EventDict:
    """
    Return a new event_dict with only allowed keys and non-None projected fields.

    Pure function: does not mutate the input, which is safer if context_class is ever changed from dict.

    Args:
        _logger: structlog logger (unused).
        _method_name: Logging method name (unused).
        event_dict: Current structlog event dictionary.

    Returns:
        EventDict: A new dict with only allowed keys and non-None values.
    """
    return {
        key: value
        for key, value in event_dict.items()
        if key in _ALLOWED_KEYS
           and not (key in (*_INTERNAL_KEYS, *_EXTRA_WHITELIST) and value is None)
    }


def _build_shared_processors() -> list[Processor]:
    """
    Build the processor chain shared by foreign stdlib logs.

    The final JSONRenderer is intentionally excluded here: rendering is done exactly once, inside
    ProcessorFormatter.processors.

    Returns:
        list[Processor]: Ordered list of pre-render processors.
    """
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt='iso', utc=True, key='timestamp'),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _add_whitelisted_extras,
    ]


def _is_ours(handler: logging.Handler) -> bool:
    """
    Return True if the handler was installed by setup_logging.

    Foreign handlers (pytest plugins, host applications) must not prevent our handlers from being installed,
    and must not be treated as evidence that setup already ran.

    Args:
        handler (logging.Handler): Any logging handler attached to root.

    Returns:
        bool: True if the handler carries the _structlog_handler marker.
    """
    return getattr(handler, '_structlog_handler', False)


def setup_logging(logs_dir: Path, log_filename: str = 'app.log') -> logging.Logger:
    """
    Configure structured JSON logging to a rotating file and the console.

    Fields passed via extra=... are projected onto the JSON event when their names are in the whitelist
    (by default: log_file). error_code is an internal key, always projected and not configurable.

    Foreign handlers already attached to the root logger are left untouched: idempotency is defined as
    "our handlers are present", not "root has no handlers".

    Args:
        logs_dir (Path): Directory where logs will be stored.
        log_filename (str, optional): Log file name (default: "app.log").

    Returns:
        logging.Logger: Configured root logger with JSON handlers.
    """
    logger = logging.getLogger()

    # Prevent duplicate installation of *our* handlers. Foreign handlers (plugins, host app) must be ignored,
    # not treated as evidence that setup already ran.
    if any(_is_ours(h) for h in logger.handlers):
        return logger

    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, log_filename)

    # Configure structlog to route through stdlib logging
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt='iso', utc=True, key='timestamp'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            _add_whitelisted_extras,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Single JSON formatter; JSONRenderer lives only here (no double encoding)
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=_build_shared_processors(),
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            _filter_event_dict,
            structlog.processors.JSONRenderer(ensure_ascii=False),
        ],
    )

    # Create rotating file handler
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8',
    )
    file_handler._structlog_handler = True
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler._structlog_handler = True
    console_handler.setFormatter(formatter)

    # Configure logging
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Suppress verbose HTTP client logs (Azure SDK, httpx, httpcore)
    # Example: azure.core.pipeline.policies.http_logging_policy
    # for noisy_logger in (
    #         "azure.core.pipeline.policies.http_logging_policy",
    #         "httpx",
    #         "httpcore",
    # ):
    #     logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    logger.info(
        f"Logging setup complete. Logs are stored in {log_file}",
        extra={'log_file': log_file},
    )

    return logger
