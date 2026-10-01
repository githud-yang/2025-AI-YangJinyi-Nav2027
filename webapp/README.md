# Web 应用（webapp）—— 创意作品

一个 FastAPI + 原生前端三件套（HTML/CSS/JS）的综合演示，同时把两大模块接进了浏览器。

## 运行

```powershell
# 终端 1：确保本地大模型已启动
ollama serve        # 通常安装后自动常驻

# 终端 2：启动 Web
pip install fastapi "uvicorn[standard]" httpx python-multipart
cd webapp
uvicorn server:app --port 8000
```

浏览器打开：

- **http://127.0.0.1:8000/** —— AI 文字冒险游戏（创意作品）
  本地 `qwen2.5:7b` 通过 ollama OpenAI 兼容接口驱动剧情，玩家自由输入行动推进故事。
- **http://127.0.0.1:8000/yolo** —— YOLO 实时摄像头检测视频流

## 结构

```
webapp/
├── server.py            # FastAPI：/api/chat(大模型) + /yolo/stream(视频流)
├── static/
│   ├── index.html       # 游戏主页
│   ├── yolo.html        # 实时检测页
│   ├── style.css
│   └── app.js
└── uploads/
```
