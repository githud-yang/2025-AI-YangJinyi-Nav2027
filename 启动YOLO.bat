@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动 YOLO 实时检测（会打开摄像头窗口，按 q 退出）...
conda run -n yolo python yolo\detect_realtime.py
pause
