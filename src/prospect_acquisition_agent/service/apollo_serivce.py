from src.prospect_acquisition_agent.config.settings import AppSettings, get_app_settings
from src.prospect_acquisition_agent.service.base_third_party_api_service import (
    BaseThirdPartyAPIService,
)


class ApolloService(BaseThirdPartyAPIService):
    def __init__(self):
        settings: AppSettings = get_app_settings()
        headers = {
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "x-api-key": f"{settings.apollo_api.api_key}"
        }
        super().__init__("https://api.apollo.io/api/v1/", headers)

    def people_search(self, endpoint: str = "mixed_people/search", params: dict = None) -> dict:
        pass

    def organizations_search(self, endpoint: str = "mixed_companies/search", params: dict = None) -> dict:
        pass
