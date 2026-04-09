const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const logoutBtn = document.getElementById("logoutBtn");
const loggedIn = document.body.dataset.loggedIn === "1";

function appendMessage(role, text) {
  const line = document.createElement("div");
  line.className = `msg ${role}`;
  line.textContent = text;
  messagesEl.appendChild(line);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  appendMessage("user", text);
  inputEl.value = "";

  if (!loggedIn) {
    appendMessage("assistant", "请先点击右上角 Microsoft 登录后再操作任务。");
    return;
  }

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    if (!res.ok) {
      appendMessage("assistant", `请求失败: ${data.detail || "未知错误"}`);
      return;
    }
    appendMessage("assistant", data.reply);
  } catch (err) {
    appendMessage("assistant", `网络异常: ${err.message}`);
  }
}

if (sendBtn) {
  sendBtn.addEventListener("click", sendMessage);
}

if (inputEl) {
  inputEl.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    await fetch("/auth/logout", { method: "POST" });
    window.location.reload();
  });
}

appendMessage("assistant", "你好，我可以帮你新增、移动、删除和自动排期复习任务。");
