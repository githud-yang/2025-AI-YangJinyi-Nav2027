"""
YOLO 实时推理（题目：实时推理部署）
====================================
默认调用本机摄像头做实时检测；无摄像头时可传入视频文件路径。
后续可用 TensorRT / ONNXRuntime / C++(libtorch) / Rust(ort) 进一步提速，
这里先保证管线正确跑通。

用法：
    python detect_realtime.py                 # 摄像头
    python detect_realtime.py path/to.mp4      # 视频文件
"""
import sys

import cv2
from ultralytics import YOLO


def run(source: str | int = 0, weights: str = "runs/detect/coco8_baseline/weights/best.pt") -> None:
    # 训练后用 best.pt；若还没训练，退回官方 nano 权重
    try:
        model = YOLO(weights)
    except Exception:  # noqa: BLE001
        model = YOLO("yolo11n.pt")

    cap = cv2.VideoCapture(source)
    print("按 q 退出")
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        # 推理并画框
        results = model(frame, verbose=False)
        annotated = results[0].plot()
        cv2.imshow("YOLO Real-time (q to quit)", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else 0
    if isinstance(src, str) and src.isdigit():
        src = int(src)
    run(src)
