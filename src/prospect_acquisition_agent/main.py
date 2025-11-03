from src.prospect_acquisition_agent.api.app import app

if __name__ == "__main__":
    import uvicorn
    from src.prospect_acquisition_agent.config.settings import get_app_settings

    settings = get_app_settings()
    uvicorn.run(app, host=settings.api.host, port=settings.api.port)
