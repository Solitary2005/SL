from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx


class GraphClient:
    base_url = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: str) -> None:
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, json_data: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=20.0) as client:
            response = client.request(method=method, url=url, headers=self._headers, json=json_data)
        if response.status_code >= 400:
            raise RuntimeError(f"Graph API error {response.status_code}: {response.text}")
        if not response.text:
            return {}
        return response.json()

    def list_todo_lists(self) -> list[dict[str, Any]]:
        data = self._request("GET", "/me/todo/lists")
        return data.get("value", [])

    def get_default_list_id(self) -> str:
        lists = self.list_todo_lists()
        if not lists:
            raise RuntimeError("No Microsoft To Do list found for this account.")

        for item in lists:
            if item.get("displayName", "").lower() in {"tasks", "任务"}:
                return item["id"]
        return lists[0]["id"]

    def list_tasks(self, list_id: str, top: int = 100) -> list[dict[str, Any]]:
        path = f"/me/todo/lists/{list_id}/tasks?$top={top}"
        data = self._request("GET", path)
        return data.get("value", [])

    def add_task(
        self,
        list_id: str,
        title: str,
        due_datetime: str | None = None,
        reminder_datetime: str | None = None,
        timezone: str = "China Standard Time",
        note: str | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"title": title}
        if due_datetime:
            payload["dueDateTime"] = {"dateTime": due_datetime, "timeZone": timezone}
        if reminder_datetime:
            payload["reminderDateTime"] = {"dateTime": reminder_datetime, "timeZone": timezone}
            payload["isReminderOn"] = True
        if note:
            payload["body"] = {"content": note, "contentType": "text"}

        return self._request("POST", f"/me/todo/lists/{list_id}/tasks", json_data=payload)

    def update_task(self, list_id: str, task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("PATCH", f"/me/todo/lists/{list_id}/tasks/{task_id}", json_data=payload)

    def delete_task(self, list_id: str, task_id: str) -> None:
        self._request("DELETE", f"/me/todo/lists/{list_id}/tasks/{task_id}")

    @staticmethod
    def to_iso_local(value: str) -> str:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
