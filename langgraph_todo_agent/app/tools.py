from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from app.config import Settings
from app.graph_client import GraphClient


class StudyTodoTools:
    def __init__(self, access_token: str, settings: Settings) -> None:
        self.client = GraphClient(access_token)
        self.settings = settings
        self.list_id = self.client.get_default_list_id()

    def _find_task_by_key(self, task_key: str) -> dict[str, Any]:
        tasks = self.client.list_tasks(self.list_id, top=200)
        for task in tasks:
            if task.get("id") == task_key:
                return task
        matched = [t for t in tasks if task_key in (t.get("title") or "")]
        if not matched:
            raise RuntimeError(f"未找到任务: {task_key}")
        if len(matched) > 1:
            titles = ", ".join(item.get("title", "") for item in matched[:5])
            raise RuntimeError(f"匹配到多个任务，请更具体。候选: {titles}")
        return matched[0]

    def add_task(self, title: str, due_datetime: str | None = None, reminder_datetime: str | None = None, note: str | None = None) -> str:
        task = self.client.add_task(
            list_id=self.list_id,
            title=title,
            due_datetime=due_datetime,
            reminder_datetime=reminder_datetime,
            timezone=self.settings.todo_timezone,
            note=note,
        )
        return f"已添加任务: {task.get('title')} (id={task.get('id')})"

    def move_task(self, task_key: str, new_due_datetime: str, split_count: int = 1, note: str | None = None) -> str:
        task = self._find_task_by_key(task_key)
        payload: dict[str, Any] = {
            "dueDateTime": {"dateTime": new_due_datetime, "timeZone": self.settings.todo_timezone}
        }
        if note:
            payload["body"] = {"content": note, "contentType": "text"}
        self.client.update_task(self.list_id, task["id"], payload)

        if split_count <= 1:
            return f"已移动任务: {task.get('title')} -> {new_due_datetime}"

        created_ids: list[str] = []
        for i in range(2, split_count + 1):
            part_due = datetime.fromisoformat(new_due_datetime) + timedelta(hours=(i - 1) * 2)
            new_title = f"{task.get('title')} ({i}/{split_count})"
            created = self.client.add_task(
                list_id=self.list_id,
                title=new_title,
                due_datetime=part_due.strftime("%Y-%m-%dT%H:%M:%S"),
                reminder_datetime=None,
                timezone=self.settings.todo_timezone,
                note=note,
            )
            created_ids.append(created.get("id", ""))

        first_title = f"{task.get('title')} (1/{split_count})"
        self.client.update_task(self.list_id, task["id"], {"title": first_title})
        return f"已移动并拆分任务: {first_title}，新增 {split_count - 1} 个子任务"

    def delete_task(self, task_key: str) -> str:
        task = self._find_task_by_key(task_key)
        self.client.delete_task(self.list_id, task["id"])
        return f"已删除任务: {task.get('title')}"

    def show_schedule(self, start_date: str | None = None, end_date: str | None = None) -> str:
        tasks = self.client.list_tasks(self.list_id, top=200)
        filtered = []

        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        for task in tasks:
            due = task.get("dueDateTime", {}).get("dateTime")
            if not due:
                continue
            due_dt = datetime.fromisoformat(due.replace("Z", ""))
            if start_dt and due_dt < start_dt:
                continue
            if end_dt and due_dt > end_dt:
                continue
            filtered.append((due_dt, task))

        filtered.sort(key=lambda x: x[0])
        if not filtered:
            return "当前时间范围没有复习任务。"

        lines = ["你的复习日程如下:"]
        for due_dt, task in filtered:
            reminder = task.get("reminderDateTime", {}).get("dateTime")
            reminder_text = reminder or "无提醒"
            lines.append(f"- {due_dt:%Y-%m-%d %H:%M} | {task.get('title')} | 提醒: {reminder_text} | id={task.get('id')}")
        return "\n".join(lines)

    def auto_plan(
        self,
        topic: str,
        start_date: str,
        end_date: str,
        total_sessions: int,
        duration_minutes: int = 90,
        preferred_hour: int = 20,
    ) -> str:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if end < start:
            raise RuntimeError("结束日期必须晚于开始日期")
        if total_sessions <= 0:
            raise RuntimeError("total_sessions 必须大于 0")

        days = (end.date() - start.date()).days + 1
        if total_sessions > days * 2:
            raise RuntimeError("会话数过多，请减少 total_sessions 或扩大日期范围")

        slots: list[datetime] = []
        current = start
        while current.date() <= end.date():
            first = datetime.combine(current.date(), datetime.min.time()).replace(hour=preferred_hour, minute=0)
            second = first + timedelta(hours=2)
            slots.extend([first, second])
            current += timedelta(days=1)

        picked = slots[:total_sessions]
        for i, slot in enumerate(picked, start=1):
            due = slot.strftime("%Y-%m-%dT%H:%M:%S")
            reminder = (slot - timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
            note = f"自动排期: 第{i}/{total_sessions}次, 预计{duration_minutes}分钟"
            self.client.add_task(
                list_id=self.list_id,
                title=f"{topic} 复习 {i}/{total_sessions}",
                due_datetime=due,
                reminder_datetime=reminder,
                timezone=self.settings.todo_timezone,
                note=note,
            )

        return f"已自动排期 {total_sessions} 个复习任务，主题: {topic}"
