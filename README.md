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

官方附件 `src.zip` 解压到工作空间后，包名是 `daohang`，可执行文件名是 `daohang.cpp`。节点本身每 0.5 秒打印一句考核文字，用来检查工作空间、colcon 和环境变量有没有配好。

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
| 节点 / 可执行文件 | `daohang.cpp` |
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

## 五、面试时可以讲清楚的点

- 为什么要 `source`：bash 只认环境变量里的路径，不 source 就找不到自己编出来的包。
- 为什么第一次用 Release：关闭调试信息、打开优化，适合运行和测试。
- 指针 `->`、`new/delete`、构造/析构的调用时机。
- 导航组后续会用到节点、话题、服务、launch、yaml，这次考核先把工作空间跑通。
