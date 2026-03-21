# 轻量化 LangGraph 复习日程助手

一个可部署的中文日程管理 Agent，支持自然语言新增/修改/删除/查询复习任务，并同步到 Microsoft To Do（到期时间、提醒、备注）。

## 功能

- 中文自然语言交互（Web 聊天界面）
- Microsoft 身份平台 OAuth2 登录
- LangGraph Agent + Tool 调用
- Graph API 同步 Microsoft To Do
- 支持智能排期（包括任务拆分）

## Agent Workflow

User input -> LLM reasoning -> 调用 tool -> Graph API

## Tools

- `add_task`
- `move_task`
- `delete_task`
- `show_schedule`
- `auto_plan`

## 1. Microsoft 应用注册

1. 打开 Azure Portal -> Entra ID -> App registrations -> New registration。
2. Redirect URI 填 `http://localhost:8000/auth/callback`。
3. 在 API permissions 中添加 Microsoft Graph Delegated 权限：
   - `Tasks.ReadWrite`
   - `openid`
   - `profile`
   - `offline_access`
4. 创建 Client Secret，并保存值。

## 2. 安装依赖

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## 3. 配置环境变量

复制 `.env.example` 为 `.env`，填入真实配置。

PowerShell 示例：

```powershell
Copy-Item .env.example .env
```

## 4. 运行

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

打开 `http://localhost:8000`。

## 示例指令

- 新增任务：`新增任务 高数错题复习，明天晚上8点截止，提前30分钟提醒，备注做第3章。`
- 移动并拆分：`把下周三的复习移动到周五晚间，并且分两次完成。`
- 查询：`看看我这周的复习安排。`
- 自动排期：`帮我把英语阅读在 2026-03-20 到 2026-03-27 自动排 6 次。`

## 生产部署建议

- 使用 Docker 或云函数容器运行 FastAPI。
- 使用 HTTPS 并将 Redirect URI 改为生产域名。
- 将 session key 与 client secret 放入密钥管理系统。
- 建议加上 Redis 会话存储与访问日志。
