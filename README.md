# 萤火 · AIU 创智部二面实战项目

> 一台 RTX 5070（8GB 显存）笔记本上，把「本地大模型 + 智能体 + YOLO + 一个能玩的网页游戏」全部跑通的综合项目。
>
> **模型后端双路兼容**：默认用本地 Ollama 的 `qwen2.5:7b`；在 `llm-agent/.env` 里把 `LLM_PROVIDER` 改成 `deepseek` 并填入自己的 `DEEPSEEK_API_KEY`，同一个智能体代码即可切到云端，无需改代码。

## 我做了什么（一页看懂）

| 题目 | 完成情况 | 位置 |
|------|----------|------|
| 一、本地大模型部署 | ✅ Ollama + `qwen2.5:7b`，OpenAI 兼容接口 | [llm-agent/](llm-agent/) |
| 一、搭建智能体并通过 API 接入应用 | ✅ 自带工具调用的轻量 Agent，CLI + Web 两种接入；兼容 DeepSeek 云端 | [llm-agent/agent.py](llm-agent/agent.py) |
| 二、YOLO 训练 | ✅ ultralytics 一次完整训练（coco8，mAP50=0.858） | [yolo/train.py](yolo/train.py) |
| 二、YOLO 实时推理 + 接入 Web | ✅ 摄像头实时检测，网页视频流 | [yolo/detect_realtime.py](yolo/detect_realtime.py)、[webapp/](webapp/) |
| 三、硬件结合 | ⏭️ 无单片机硬件，本次跳过（见工程日志说明） | — |
| 五、创意作品 | ✅ **萤火·AI 文字冒险网页游戏**，由大模型实时生成剧情 | [webapp/static/index.html](webapp/static/index.html) |
| 工程规范 | ✅ 干净目录 / README / 工程日志 / Git 提交 | 本仓库 |

## 整体思路（面试官关心的不是代码细节，是思路）

1. **先把重模型跑起来**：本机只有 8GB 显存，所以选 Q4 量化的 7B 模型（`qwen2.5:7b`），显存占用约 6GB，响应够快。Ollama 一键拉起，并暴露 OpenAI 兼容接口，这一步等于把"大模型"变成了一个普通的 HTTP 服务。
2. **在 HTTP 服务之上做智能体**：没有上 Docker 版 Dify，而是直接写了一个带工具调用循环的 Agent（取时间、计算、写笔记）。这样逻辑透明、好调试，同时这个 OpenAI 兼容地址也能直接填进 Dify/n8n/扣子当 model provider。
3. **YOLO 走标准管线**：先用 ultralytics 自带的 coco8 把"训练→出权重→实时推理"整条链路跑通，参数自己定（epochs=30, batch=4, imgsz=640）。真实数据集只需换一个 yaml。
4. **最后把它们接进一个 Web 应用**：FastAPI 一个后端，同时提供 `/api/chat`（大模型）和 `/yolo/stream`（检测视频流），前端原生三件套。创意作品"AI 文字冒险"就长在这个后端上。
5. **做减法**：全程没有堆无用的框架，每个模块单独可跑，README 说人话。

## 快速复现

```powershell
# 0. 装 ollama 后拉模型
ollama pull qwen2.5:7b

# 1. 跑 YOLO 训练
conda activate yolo
pip install ultralytics
cd yolo; python train.py; cd ..

# 2. 启动 Web（游戏 + YOLO 实时画面）
pip install -r requirements.txt
cd webapp; uvicorn server:app --port 8000
# 浏览器打开 http://127.0.0.1:8000/

# 3. 或直接玩命令行智能体
cd llm-agent; pip install httpx; python cli.py
```

## AI 使用情况（如实说明）

代码骨架、调试与文档在本地完成；编写过程中使用了 AI 辅助生成样板代码并逐段核对运行结果。所有命令、模型、路径均为本机真实执行环境，可按上面步骤复现。

## 目录结构

```
.
├── README.md
├── requirements.txt
├── docs/
│   └── progress.md        # 工程日志：进度、卡点、想法
├── llm-agent/            # 本地大模型 + 智能体 + CLI
├── yolo/                 # YOLO 训练与实时推理
└── webapp/               # FastAPI + 前端（创意作品）
```
