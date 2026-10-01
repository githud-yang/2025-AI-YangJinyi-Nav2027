"""
大冒险 · 本地/云端智能体（LLM Agent）
====================================
一个文件同时支持两种模型后端，按同目录 .env 的 LLM_PROVIDER 自动切换：
  - ollama   ：本机本地大模型，无需 key（题目要求的本地部署）
  - deepseek ：DeepSeek 云端 API，OpenAI 兼容接口（需在 .env 填 DEEPSEEK_API_KEY）

两者都是 OpenAI Chat Completions 协议，因此工具调用循环完全一致。
配置：复制 .env.example 为 .env，填好 key 即可。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx

# ---------------------------------------------------------------------------
# 读取同目录 .env（轻量实现，不依赖 python-dotenv）
# ---------------------------------------------------------------------------
def _load_env() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


_load_env()


def _provider_cfg() -> dict:
    if os.getenv("LLM_PROVIDER", "ollama").lower() == "deepseek":
        return {
            "base_url": os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/") + "/v1",
            "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        }
    return {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/") + "/v1",
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
        "api_key": os.getenv("OLLAMA_API_KEY", "ollama"),
    }


# ---------------------------------------------------------------------------
# 工具注册表
# ---------------------------------------------------------------------------
def tool_get_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def tool_calculate(expr: str) -> str:
    allowed = set("0123456789+-*/().%^ ")
    if not set(expr).issubset(allowed):
        return "错误：表达式包含非法字符"
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as e:  # noqa: BLE001
        return f"计算失败：{e}"


def tool_note(content: str) -> str:
    with open(Path(__file__).resolve().parent / "agent_notes.txt", "a", encoding="utf-8") as f:
        f.write(f"[{tool_get_time()}] {content}\n")
    return f"已记录：{content}"


TOOLS = {
    "get_time": {
        "schema": {"type": "function", "function": {
            "name": "get_time", "description": "获取当前系统日期与时间",
            "parameters": {"type": "object", "properties": {}}}},
        "fn": lambda: tool_get_time(),
    },
    "calculate": {
        "schema": {"type": "function", "function": {
            "name": "calculate", "description": "计算数学表达式，如 (128+56)*3.5",
            "parameters": {"type": "object", "properties": {
                "expr": {"type": "string"}}}, "required": ["expr"]}},
        "fn": lambda expr: tool_calculate(expr),
    },
    "note": {
        "schema": {"type": "function", "function": {
            "name": "note", "description": "把待办/笔记保存到本地 agent_notes.txt",
            "parameters": {"type": "object", "properties": {
                "content": {"type": "string"}}}, "required": ["content"]}},
        "fn": lambda content: tool_note(content),
    },
}


class LocalLLMAgent:
    """对上层（CLI / Web）暴露统一接口，内部按 .env 切换后端。"""

    def __init__(self) -> None:
        cfg = _provider_cfg()
        self.base_url = cfg["base_url"]
        self.model = cfg["model"]
        self.api_key = cfg["api_key"]
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.system_prompt = (
            "你是「大冒险」游戏主持人。能调用本地工具时优先调用工具，不要编造时间或计算结果。"
            "回答简洁、中文。"
        )

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _chat(self, messages: list, tools: list | None = None) -> dict:
        payload = {"model": self.model, "messages": messages, "stream": False}
        if tools:
            payload["tools"] = tools
        r = httpx.post(
            f"{self.base_url}/chat/completions", json=payload,
            headers=self._headers(), timeout=120,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]

    def chat(self, user_input: str, history: list | None = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            messages += history
        messages.append({"role": "user", "content": user_input})
        schemas = [t["schema"] for t in TOOLS.values()]

        for _ in range(5):  # 工具调用最多 5 轮
            resp = self._chat(messages, schemas)
            messages.append(resp)
            if not resp.get("tool_calls"):
                return resp.get("content", "")
            for call in resp["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"] or "{}")
                observation = TOOLS[name]["fn"](**args)
                messages.append({
                    "role": "tool", "tool_call_id": call["id"],
                    "name": name, "content": observation,
                })
        return self._chat(messages).get("content", "")


if __name__ == "__main__":
    agent = LocalLLMAgent()
    print(f"大冒险已启动 | provider={agent.provider} | model={agent.model}")
    while True:
        q = input("\n你：").strip()
        if q.lower() in {"exit", "quit", "退出"}:
            break
        if q:
            print("\nAI：", agent.chat(q))
