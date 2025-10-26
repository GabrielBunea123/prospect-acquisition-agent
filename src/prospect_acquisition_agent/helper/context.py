from contextvars import ContextVar
from typing import Optional

# Context variable to store trace_id across async execution context
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)


def set_trace_id(trace_id: str) -> None:
    """
    Set the trace ID in the current context.
    :param trace_id: new trace id value
    :return: The trace ID to set (typically a UUID string)
    """
    trace_id_var.set(trace_id)


def get_trace_id() -> Optional[str]:
    """
    Get the trace ID from the current context.
    :return: The trace ID if set, None otherwise
    """
    return trace_id_var.get()
