// AI 文字冒险前端逻辑
const chat = document.getElementById("chat");
const form = document.getElementById("input-form");
const input = document.getElementById("input");

// 保存对话历史，传给后端
const history = [];

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  div.innerHTML = `<p>${text.replace(/</g, "&lt;")}</p>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  const btn = form.querySelector("button");
  btn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history }),
    });
    const data = await res.json();
    history.push({ user: text, ai: data.reply });
    addMessage(data.reply, "ai");
  } catch (err) {
    addMessage("⚠️ 连不上后端，请确认 ollama 已启动且 server.py 在运行。", "ai");
  } finally {
    btn.disabled = false;
    input.focus();
  }
});
