"""竞品调研 Agent：封装 browser-use 的核心逻辑。"""
import os
from datetime import datetime

from dotenv import load_dotenv
from browser_use import Agent, ChatDeepSeek

from prompts import RESEARCH_TASK_TEMPLATE, REPORT_HEADER_TEMPLATE


def build_llm() -> ChatDeepSeek:
    """构造 LLM（默认 DeepSeek，模型可通过环境变量 DEEPSEEK_MODEL 覆盖）。"""
    load_dotenv()
    return ChatDeepSeek(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
    )


async def research(name: str) -> str:
    """对单个竞品执行调研，返回报告正文（Markdown）。"""
    llm = build_llm()
    task = RESEARCH_TASK_TEMPLATE.format(name=name)
    # max_steps 限制 Agent 最多执行多少步（每步 = 一次浏览操作 + 一次大模型调用），
    # 步数越少越快；调研类任务 10 步通常足够。
    agent = Agent(task=task, llm=llm, max_steps=10)
    history = await agent.run()
    return history.final_result()


def save_report(name: str, body: str, output_dir: str = "reports") -> str:
    """把报告正文写入 Markdown 文件，返回文件路径。"""
    os.makedirs(output_dir, exist_ok=True)
    safe_name = name.strip().replace("/", "_").replace("\\", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"{safe_name}_{timestamp}.md")

    header = REPORT_HEADER_TEMPLATE.format(
        name=name, date=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header + "\n\n" + body)
    return filename
