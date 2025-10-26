from typing import Annotated

from fastapi import Depends

from src.prospect_acquisition_agent.config.settings import AppSettings, get_app_settings


async def create_app_settings() -> AppSettings:
    return get_app_settings()

app_settings_dep = Annotated[AppSettings, Depends(create_app_settings)]


