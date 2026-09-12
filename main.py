"""竞品调研 Agent —— 命令行入口。

用法：
    python main.py Dify RAGFlow          # 批量调研多个竞品
    python main.py                       # 不传参则交互式输入
    python main.py --output reports Dify # 自定义报告输出目录
"""
import argparse
import asyncio

from research_agent import research, save_report


async def run(names, output_dir: str) -> None:
    for name in names:
        print(f"\n>>> 开始调研：{name}")
        try:
            body = await research(name)
            path = save_report(name, body, output_dir)
            print(f"✅ 已保存报告：{path}")
        except Exception as e:  # noqa: BLE001 —— 单个失败不影响后续
            print(f"❌ {name} 调研失败：{e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="竞品调研 Agent：自动浏览网页并生成结构化调研报告"
    )
    parser.add_argument(
        "names", nargs="*", help="要调研的竞品名称，多个用空格分隔，如：Dify RAGFlow"
    )
    parser.add_argument(
        "--output", default="reports", help="报告输出目录（默认 reports）"
    )
    args = parser.parse_args()

    names = args.names
    if not names:
        raw = input("请输入要调研的竞品名称（多个用空格分隔）：").strip()
        names = raw.split()

    if not names:
        print("未输入任何名称，退出。")
        return

    asyncio.run(run(names, args.output))


if __name__ == "__main__":
    main()
