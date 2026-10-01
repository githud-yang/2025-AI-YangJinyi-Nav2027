# YOLO 训练与实时推理（yolo）

## 环境

本机已有 conda 环境 `yolo` / `pest-yolo`，并装有 `torch 2.11.0+cu128` 与 `opencv`。

```powershell
conda activate yolo
pip install ultralytics
```

## 1. 训练（完成一次训练，参数自定）

```powershell
python train.py
```

- 数据：`coco8.yaml`（ultralytics 自带 8 张图，自动下载，便于快速验证管线）
- 超参：`epochs=30, imgsz=640, batch=4, device=0(RTX 5070)`
- 产物：`runs/detect/coco8_baseline/weights/best.pt`

> 真实项目把 `data` 换成自己标注的数据集 yaml（可用 labelImg，本机已有 `labelimg` 环境）。

## 2. 实时推理

```powershell
python detect_realtime.py            # 本机摄像头
python detect_realtime.py demo.mp4    # 视频文件
```

按 `q` 退出。脚本会自动优先用训练出的 `best.pt`，没有则回退 `yolo11n.pt`。

## 3. 接入 Web 应用

`webapp/server.py` 提供 `/yolo/stream` 视频流接口，直接在浏览器里看实时检测画面，
对应题目「YOLO 接入应用（web）」。

## 性能优化方向（可后续做）

- `model.export(format="onnx")` → ONNXRuntime 提速；
- 进一步用 TensorRT / C++(libtorch) / Rust(ort) 优化。
