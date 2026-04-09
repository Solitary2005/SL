from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

from app.agent import StudyPlannerAgent
from app.auth import MicrosoftAuth
from app.config import get_settings


settings = get_settings()
auth = MicrosoftAuth(settings)
agent = StudyPlannerAgent(settings)

app = FastAPI(title="LangGraph Study Planner", version="0.1.0")
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret_key)

base_dir = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")
templates = Jinja2Templates(directory=str(base_dir / "templates"))


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user_name = request.session.get("user_name")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_name": user_name,
            "logged_in": bool(request.session.get("access_token")),
        },
    )


@app.get("/auth/login")
def login(request: Request):
    flow = auth.initiate_auth_flow()
    request.session["auth_flow"] = flow
    return RedirectResponse(flow["auth_uri"])


@app.get("/auth/callback")
def auth_callback(request: Request):
    flow = request.session.get("auth_flow")
    if not flow:
        raise HTTPException(status_code=400, detail="Auth flow is missing.")

    result = auth.acquire_token_by_auth_code_flow(flow, dict(request.query_params))
    if "access_token" not in result:
        raise HTTPException(status_code=401, detail=result.get("error_description", "OAuth failed"))

    request.session["access_token"] = result["access_token"]
    claims = result.get("id_token_claims", {})
    request.session["user_name"] = claims.get("name", "Microsoft User")
    request.session.pop("auth_flow", None)
    return RedirectResponse(url="/")


@app.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"ok": True}


@app.post("/api/chat")
def chat(request: Request, body: ChatRequest):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="请先登录 Microsoft 账号")
    try:
        answer = agent.run(body.message, token)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"reply": answer}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
