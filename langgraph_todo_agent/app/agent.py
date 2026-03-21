from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from app.config import Settings
from app.tools import StudyTodoTools


SYSTEM_PROMPT = """
你是一个中文复习计划助手。你必须优先通过工具来执行操作，并以简洁中文回复用户。
可用工具:
- add_task: 新增任务
- move_task: 移动任务，可拆分
- delete_task: 删除任务
- show_schedule: 查询日程
- auto_plan: 自动排期
规则:
1. 用户要求新增/修改/删除/查询时，必须调用对应工具。
2. 时间统一使用 ISO 格式: YYYY-MM-DDTHH:MM:SS。
3. 如果用户时间不完整，优先补充到晚间 20:00。
4. 输出最终结果时，先说明操作结果，再给出下一步建议。
""".strip()


class AddTaskInput(BaseModel):
    title: str = Field(description="任务标题")
    due_datetime: str | None = Field(default=None, description="到期时间，ISO 格式")
    reminder_datetime: str | None = Field(default=None, description="提醒时间，ISO 格式")
    note: str | None = Field(default=None, description="备注")


class MoveTaskInput(BaseModel):
    task_key: str = Field(description="任务 id 或标题关键词")
    new_due_datetime: str = Field(description="新的到期时间，ISO 格式")
    split_count: int = Field(default=1, description="拆分次数")
    note: str | None = Field(default=None, description="备注")


class DeleteTaskInput(BaseModel):
    task_key: str = Field(description="任务 id 或标题关键词")


class ShowScheduleInput(BaseModel):
    start_date: str | None = Field(default=None, description="开始时间，ISO 格式")
    end_date: str | None = Field(default=None, description="结束时间，ISO 格式")


class AutoPlanInput(BaseModel):
    topic: str = Field(description="复习主题")
    start_date: str = Field(description="开始日期，ISO 格式")
    end_date: str = Field(description="结束日期，ISO 格式")
    total_sessions: int = Field(description="总复习次数")
    duration_minutes: int = Field(default=90, description="每次复习分钟数")
    preferred_hour: int = Field(default=20, description="偏好开始小时")


class StudyPlannerAgent:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
        )

    def _build_tools(self, access_token: str) -> list[StructuredTool]:
        tools = StudyTodoTools(access_token=access_token, settings=self.settings)

        return [
            StructuredTool.from_function(
                func=tools.add_task,
                name="add_task",
                description="新增复习任务并同步到 Microsoft To Do",
                args_schema=AddTaskInput,
            ),
            StructuredTool.from_function(
                func=tools.move_task,
                name="move_task",
                description="移动复习任务时间，可拆分为多次",
                args_schema=MoveTaskInput,
            ),
            StructuredTool.from_function(
                func=tools.delete_task,
                name="delete_task",
                description="删除复习任务",
                args_schema=DeleteTaskInput,
            ),
            StructuredTool.from_function(
                func=tools.show_schedule,
                name="show_schedule",
                description="查询复习日程",
                args_schema=ShowScheduleInput,
            ),
            StructuredTool.from_function(
                func=tools.auto_plan,
                name="auto_plan",
                description="根据时间区间自动排期复习任务",
                args_schema=AutoPlanInput,
            ),
        ]

    def run(self, user_message: str, access_token: str) -> str:
        graph = create_react_agent(self.llm, tools=self._build_tools(access_token))
        result: dict[str, Any] = graph.invoke(
            {
                "messages": [
                    SystemMessage(content=SYSTEM_PROMPT),
                    HumanMessage(content=user_message),
                ]
            }
        )
        messages = result.get("messages", [])
        if not messages:
            return "未收到有效响应，请重试。"
        content = messages[-1].content
        if isinstance(content, list):
            return "\n".join(str(item) for item in content)
        return str(content)
