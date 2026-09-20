# 2027导航组第一次面试考核研究报告

华南农业大学 · 2025级人工智能 · 杨锦毅

本仓库对应 Taurus 战队导航组 2027 招新第一次面试考核。环境为 Ubuntu 24.04 + ROS 2 Jazzy，代码按考核要求分成 `exam1`、`exam2`。更换路径后，按下面步骤即可重新编译运行。

---

## 一、环境与工作空间

1. 安装 Ubuntu 24.04 和 ROS 2 Jazzy（可用鱼香 ROS 一键安装）。
2. 终端每次启动会读取 `~/.bashrc`。系统 ROS 一般已经写入：

```bash
source /opt/ros/jazzy/setup.bash
```

3. 自己的工作空间还要再 source 一次，否则 `ros2 run` / `ros2 launch` 找不到包。可以写进 `~/.bashrc`，也可以每次手动执行：

```bash
cd ~/nav_ws
source ./install/setup.bash
```

第一次编译用 Release，方便后续部署和测试：

```bash
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

之后同一工作空间再编译，直接 `colcon build` 即可。`--symlink-install` 会把脚本做成符号链接，改 Python/launch 后不用每次重装。

---

## 二、考核一：C++ 基础

文件在 `exam1/`。

### 第一题：升序

给定 `5 8 2 10 7 15 13 11 20 18`，用冒泡排序从小到大输出。

- 外层循环控制轮数，内层循环做相邻比较。
- 如果前一个比后一个大，就交换。每一轮会把当前最大的数“冒”到后面。
- 运行结果：`2 5 7 8 10 11 13 15 18 20`

```bash
g++ -std=c++17 -o q1 exam1/第一题_升序.cpp
./q1
```

### 第二题：结构体、指针、动态内存

`Student` 含 `name[50]`、`id`、`score`。`input()` 和 `display()` 都接收指针，成员访问必须用 `->`。

- `stu->name` 等价于 `(*stu).name`。
- `new Student` 在堆上创建，用完 `delete`，避免内存泄漏。
- 按题目样例输入 `张三 / 123 / 90.5`，输出为：

```text
姓名：张三
学号：123
成绩：90.5
```

### 第三题：类、构造与析构

`Car` 的颜色和车牌号放在 private 里，外部只能通过公有函数访问。

- 构造函数在创建对象时自动调用，负责初始化。
- 析构函数在对象离开作用域时自动调用，调用顺序和构造相反。
- `display()` 输出车辆信息（题目原文写成了“学生信息”，按题意输出车辆）。

---

## 三、考核二：ROS 2 编译与运行

官方附件 `src.zip` 解压到工作空间后，包名是 `daohang`，可执行程序名是 `daohang.cpp`。该程序每 0.5 秒打印一句考核文字，用来检查工作空间、colcon 和环境变量有没有配好。需要注意，这份附件没有使用 `rclcpp::Node` 创建 ROS 2 节点，因此它是由 `ros2 run` 启动的可执行程序，不会出现在 `ros2 node list` 中。

```bash
cd ~/nav_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source ./install/setup.bash
ros2 run daohang daohang.cpp
```

终端应循环出现：`这里是2027导航考核第二题awa`。截图见 `exam2/`。

对应关系：

| 概念 | 这次实际用到的 |
| --- | --- |
| 功能包 | `daohang`（`package.xml` + `CMakeLists.txt`） |
| 可执行程序 | `daohang.cpp`（未创建 `rclcpp::Node`） |
| 构建 | `colcon` + `ament_cmake` |
| 环境 | `source /opt/ros/jazzy/setup.bash` 再 `source install/setup.bash` |

---

## 四、Git / GitHub 使用记录

GitHub 账号：`githud-yang`。仓库设为 **Public**，本文件就是考核要求的研究报告。

```bash
git init
git add exam1 exam2 README.md .gitignore
git commit -m "完成2027导航组第一次面试考核，并整理可复现环境说明。"
git branch -M main
git remote add origin https://github.com/githud-yang/2025-AI-YangJinyi-Nav2027.git
git push -u origin main
```

换电脑后：先 `git clone` 上述地址，再按第一节配置 ROS 2 环境即可复现。

---

## 五、学习指南

### 1. ROS 2 基础与导航

建议先掌握工作空间、功能包、节点、话题、服务和动作，再学习 launch、YAML、TF2 坐标变换和 Nav2。学习时应同步完成示例，不能只观看视频。

- [小鱼动手学 ROS 2](https://fishros.com/d2lros2/)：建议按入门篇、机器人学篇、坐标变换和 Nav2 导航篇的顺序学习，并配合视频完成练习。
- [赵虚左 ROS 2 理论与实践](https://www.bilibili.com/video/BV1VB4y137ys/)：适合系统理解 ROS 2 的环境搭建、通信机制、功能包和常用工具。
- [ROS 2 Jazzy 官方教程](https://docs.ros.org/en/jazzy/Tutorials.html)：前两套中文资料的部分章节基于较早发行版；遇到命令、包名或 API 差异时，以 Jazzy 官方文档为准。

完成这一阶段后，应能独立完成以下任务：

- 创建并编译 C++ 或 Python 功能包。
- 编写发布者和订阅者，并使用 `ros2 topic`、`rqt_graph` 等工具检查通信。
- 理解服务与动作的适用场景。
- 使用 launch 启动多个节点，使用 YAML 管理参数。
- 解释 TF2 中父子坐标系及坐标变换的作用。
- 在仿真环境中运行 Nav2，并理解全局规划、局部规划、定位和控制的基本关系。

### 2. 运动规划与控制

先区分路径规划、轨迹规划和运动控制，再了解 PID 及常见规划算法。阅读[图解自动驾驶中的运动规划 Motion Planning](https://mr-winter.blog.csdn.net/article/details/128738977)时，重点关注以下内容：

- Dijkstra、A* 等图搜索算法如何计算可行路径。
- RRT 等采样算法适合解决什么问题。
- 全局规划与局部规划的输入、输出和职责区别。
- PID 中比例、积分、微分项分别怎样影响响应速度、稳态误差和振荡。
- 规划结果如何转化为机器人可以执行的速度或控制指令。

### 3. EKF-SLAM 与状态估计

- [EKF-SLAM hands-on tutorial](https://jihongju.github.io/2019/07/06/ekfslam-hands-on-tutorial/)
- [University of Freiburg Robot Mapping 课程资料](https://ais.informatik.uni-freiburg.de/teaching/ws13/mapping/)

学习时重点回答以下问题：

- 状态均值和协方差分别表示什么。
- 预测阶段和观测更新阶段分别改变哪些量。
- 过程噪声和观测噪声如何通过 Q、R 矩阵影响估计结果。
- 卡尔曼增益如何平衡模型预测与传感器观测。
- 噪声参数设置过大或过小时，轨迹和地图会出现什么变化。

### 4. 无线电与协议分析 拓展方向

无线电是拓展方向。第一阶段不要求推导复杂公式，应先建立“信号长什么样”的直觉，理解调制、频偏、信噪比、采样率和 IQ 数据等基本概念。可以在视频平台搜索“通信原理 通俗”“GFSK 入门”“SDR 入门”。

- [GNU Radio 官方教程](https://wiki.gnuradio.org/index.php?title=NewTutorial)：从 GRC、流图、采样率和 IQ 信号开始，再学习 FSK、PSK、滤波与数据包通信。
- [GNU Radio GFSK Demod 示例](https://wiki.gnuradio.org/index.php/GFSK_Demod)：观察调制前后的比特流、时域波形和频谱变化。

协议分析比背公式更重要。拿到一份通信规则后，应能画出以下处理链：

```text
空口信号 -> 解调与同步 -> 原始字节 -> 帧头与长度检查 -> CRC 校验 -> 业务字段解析
```

建议完成一个小练习：使用 GNU Radio 搭建简单的 FSK/GFSK 收发流图，观察频偏和噪声对解调结果的影响，再用 Python 或 C++ 解析一段包含帧头、长度、载荷和 CRC 的模拟数据。

### 5. 推荐学习顺序

1. Ubuntu、Git、C++ 或 Python 基础。
2. ROS 2 工作空间、功能包和基本通信机制。
3. launch、YAML、TF2、URDF 与仿真工具。
4. Nav2、路径规划、PID 和机器人运动控制。
5. 概率基础、卡尔曼滤波与 EKF-SLAM。
6. 无线电、SDR、GNU Radio 和协议分析作为拓展方向。

每个阶段都应保留代码、运行截图和问题复盘。学习成果以“能够运行、解释原理、定位问题并复现”为验收标准。
