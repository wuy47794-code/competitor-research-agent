"""竞品调研 Agent —— Web 界面入口。

启动后浏览器会自动打开 http://127.0.0.1:5000，
在网页里输入竞品名即可看到调研报告（同时保存到 reports/ 目录）。
"""
import asyncio
import threading
import webbrowser

import markdown as md_lib
from flask import Flask, jsonify, render_template, request

from research_agent import research, save_report

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/research", methods=["POST"])
def api_research():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "error": "请输入竞品名称"}), 400

    try:
        # Agent 是异步的，Flask 是同步的，用 asyncio.run 起独立事件循环执行
        markdown_text = asyncio.run(research(name))
        save_report(name, markdown_text)  # 顺便落盘到 reports/
        html = md_lib.markdown(markdown_text, extensions=["tables", "fenced_code"])
    except Exception as e:  # noqa: BLE001
        return jsonify({"ok": False, "error": f"调研失败：{e}"}), 500

    return jsonify({"ok": True, "name": name, "html": html})


def main():
    port = 5000
    url = f"http://127.0.0.1:{port}"
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    print("=" * 56)
    print("  竞品调研 Agent 已启动")
    print(f"  网页地址：{url}")
    print("  请保持本窗口打开，关闭即停止服务")
    print("  按 Ctrl + C 可退出")
    print("=" * 56)
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
