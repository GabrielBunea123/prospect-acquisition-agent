from contextlib import asynccontextmanager

from src.prospect_acquisition_agent.config.logging import setup_logging, get_logger
from src.prospect_acquisition_agent.config.settings import AppSettings
from src.prospect_acquisition_agent.helper.context import set_trace_id
from src.prospect_acquisition_agent.helper.id_generator import generate_id

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app):
    """
    Lifespan event handler for application startup and shutdown.
    """
    set_trace_id(generate_id())
    app_settings: AppSettings = app.state.app_settings
    setup_logging(app_settings.logging)

    logger.info("Configure startup dependencies")
