"""
YOLO 训练脚本（题目：完成 ultralytics 的一次训练）
=====================================================
为了在面试演示里快速跑通，使用 ultralytics 自带的极小数据集 coco8（8 张图），
它会自动下载。真实项目里把 data 换成自己的数据集 yaml 即可。

用法：
    # 在已有的 yolo conda 环境中
    conda activate yolo
    pip install ultralytics   # 本机已有 torch 2.11+cu128
    python train.py
"""
from pathlib import Path

from ultralytics import YOLO

# 让训练产物固定落在脚本所在目录的 runs/ 下，不受启动时工作目录影响
RUNS_DIR = Path(__file__).resolve().parent / "runs" / "detect"


def main() -> None:
    # 选用成熟的 nano 权重，小显存也能快速迭代
    model = YOLO("yolo11n.pt")

    # 训练参数（自己决定）：小 batch、少量 epoch，便于快速验证管线
    results = model.train(
        data="coco8.yaml",     # ultralytics 自带小数据集，自动下载
        epochs=30,
        imgsz=640,
        batch=4,
        device=0,              # 用 RTX 5070（CUDA）
        workers=2,
        project=str(RUNS_DIR),
        name="coco8_baseline",
        exist_ok=True,
    )

    # 训练完顺手在验证集上评估
    metrics = model.val()
    print("mAP50:", metrics.box.map50)
    print("权重已保存到 runs/detect/coco8_baseline/weights/best.pt")


if __name__ == "__main__":
    main()
