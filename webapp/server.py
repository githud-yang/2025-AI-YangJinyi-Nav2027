"""
Web 应用（FastAPI）—— 题目要求的接入形式
============================================
整合两大模块：
  1) /            AI 对话冒险小游戏（后端调用本地 ollama 智能体）
  2) /yolo        YOLO 实时摄像头检测画面

运行：
    pip install fastapi "uvicorn[standard]" httpx
    uvicorn server:app --reload --port 8000
"""
import sys
from pathlib import Path

import cv2
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 让 webapp 能 import 到上一级的 llm-agent
sys.path.append(str(Path(__file__).resolve().parent.parent / "llm-agent"))
from agent import LocalLLMAgent  # noqa: E402

app = FastAPI(title="AIU 创智部二面 · 综合演示")
BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "static")

agent = LocalLLMAgent()


# --------------------------------------------------------------------------
# AI 对话冒险游戏
# --------------------------------------------------------------------------
GAME_SYSTEM = (
    "你是一个文字冒险游戏主持人。玩家身处一个可自由探索的场景，"
    "每轮用 3-4 句话描述当前发生的事并给出 2-3 个可选行动，推动剧情。"
    "开场场景设定为：玩家在一间摆满旧电脑的实验室醒来，桌上有一台闪着光标、"
    "已经跑起本地大模型的终端。"
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/chat")
async def api_chat(request: Request):
    body = await request.json()
    user_text = body.get("message", "")
    history = body.get("history", [])

    messages = [{"role": "system", "content": GAME_SYSTEM}]
    for h in history[-10:]:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["ai"]})

    answer = agent.chat(user_text, history=messages[1:])
    return {"reply": answer}


# --------------------------------------------------------------------------
# YOLO 实时检测视频流
# --------------------------------------------------------------------------
@app.get("/yolo", response_class=HTMLResponse)
def yolo_page(request: Request):
    return templates.TemplateResponse(request, "yolo.html")


def gen_frames():
    from ultralytics import YOLO

    weights = BASE.parent / "yolo" / "runs" / "detect" / "coco8_baseline" / "weights" / "best.pt"
    try:
        model = YOLO(str(weights))
    except Exception:  # noqa: BLE001
        model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(0)
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            results = model(frame, verbose=False)
            buf = cv2.imencode(".jpg", results[0].plot())[1].tobytes()
            yield (
                b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf + b"\r\n"
            )
    finally:
        cap.release()


@app.get("/yolo/stream")
def yolo_stream():
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
