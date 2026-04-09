import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    microsoft_client_id: str
    microsoft_client_secret: str
    microsoft_tenant_id: str
    microsoft_redirect_uri: str
    session_secret_key: str
    openai_api_key: str
    openai_model: str
    graph_scope: str
    todo_timezone: str


    @property
    def authority(self) -> str:
        return f"https://login.microsoftonline.com/{self.microsoft_tenant_id}"


    @property
    def scopes(self) -> list[str]:
        return [scope.strip() for scope in self.graph_scope.split(",") if scope.strip()]


def _get_env(name: str, default: str | None = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value or ""


def get_settings() -> Settings:
    return Settings(
        microsoft_client_id=_get_env("MICROSOFT_CLIENT_ID", required=True),
        microsoft_client_secret=_get_env("MICROSOFT_CLIENT_SECRET", required=True),
        microsoft_tenant_id=_get_env("MICROSOFT_TENANT_ID", default="common"),
        microsoft_redirect_uri=_get_env("MICROSOFT_REDIRECT_URI", default="http://localhost:8000/auth/callback"),
        session_secret_key=_get_env("SESSION_SECRET_KEY", required=True),
        openai_api_key=_get_env("OPENAI_API_KEY", required=True),
        openai_model=_get_env("OPENAI_MODEL", default="gpt-4o-mini"),
        graph_scope=_get_env("GRAPH_SCOPE", default="Tasks.ReadWrite,offline_access,openid,profile"),
        todo_timezone=_get_env("TODO_TIMEZONE", default="China Standard Time"),
    )
