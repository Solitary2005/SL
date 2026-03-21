import msal

from app.config import Settings


class MicrosoftAuth:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = msal.ConfidentialClientApplication(
            client_id=settings.microsoft_client_id,
            authority=settings.authority,
            client_credential=settings.microsoft_client_secret,
        )

    def initiate_auth_flow(self) -> dict:
        return self.client.initiate_auth_code_flow(
            scopes=self.settings.scopes,
            redirect_uri=self.settings.microsoft_redirect_uri,
        )

    def acquire_token_by_auth_code_flow(self, flow: dict, auth_response: dict) -> dict:
        return self.client.acquire_token_by_auth_code_flow(flow, auth_response)
