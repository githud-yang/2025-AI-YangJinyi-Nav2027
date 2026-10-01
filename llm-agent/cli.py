"""
CLI 应用（题目要求的最基础应用形式）
====================================
一个带多轮历史的命令行对话入口，演示本地大模型 + 工具调用。
用法：
    python cli.py
"""
from agent import LocalLLMAgent


def main() -> None:
    agent = LocalLLMAgent()
    history: list = []
    print("=" * 56)
    print(f" 本地智能体已启动 | 模型: {agent.model} | 后端: ollama")
    print(" 试试：现在几点？ | 帮我算 (128+56)*3.5 | 记一下明天交作业")
    print(" 输入 exit 退出")
    print("=" * 56)
    while True:
        try:
            q = input("\n你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in {"exit", "quit", "退出"}:
            break
        if not q:
            continue
        answer = agent.chat(q, history=history)
        print(f"AI > {answer}")
        history.append({"role": "user", "content": q})
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
