# 萤火 · 本地大模型与智能体（llm-agent）

「萤火」是本项目的个人作品名。这一层负责把大模型变成一个可被 CLI / Web 调用的智能体。

## 0. 配置（两种后端，二选一）

```powershell
cd llm-agent
copy .env.example .env
# 用记事本打开 .env：
#   LLM_PROVIDER=ollama    # 用本地模型，无需 key
#   LLM_PROVIDER=deepseek  # 用 DeepSeek 云端，把 DEEPSEEK_API_KEY 填上
```

- **本地（题目要求）**：`LLM_PROVIDER=ollama`，跑本机 `qwen2.5:7b`。
- **云端（备用）**：`LLM_PROVIDER=deepseek`，在 [DeepSeek 开放平台](https://platform.deepseek.com) 申请 key 填入 `.env`。

> `.env` 已在 `.gitignore` 中，不会上传，key 只存在你本机。

## 1. 本地大模型部署（Ollama）

```powershell
# 安装：winget install Ollama.Ollama
ollama pull qwen2.5:7b
ollama run qwen2.5:7b "你好"
```

Ollama 在 `http://localhost:11434` 常驻，并提供 OpenAI 兼容接口 `/v1`。
DeepSeek 也是 OpenAI 兼容接口，所以 `agent.py` 用同一套工具调用代码切换两者。

## 2. 智能体（带工具调用）

`agent.py` 不依赖 Docker：内置 `get_time` / `calculate` / `note` 三个本地工具，
模型决定调工具 → 本地执行 → 结果回灌 → 生成最终回答。

```powershell
pip install httpx
python cli.py
```

## 3. 作为 Model Provider 接入 Dify / n8n / 扣子

| 平台 | Base URL |
|------|----------|
| Dify（Docker 内） | `http://host.docker.internal:11434/v1` |
| n8n / 扣子（本机） | `http://localhost:11434/v1` |

填法：选「OpenAI 兼容接口」，Key 任意非空，模型名 `qwen2.5:7b`。

## 文件

- `agent.py` — 智能体核心（可被 webapp 直接 import）
- `cli.py` — CLI 应用
- `.env.example` — 配置模板（复制为 `.env` 后填 key）
