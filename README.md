# 竞品调研 Agent（Competitor Research Agent）

> 输入一个竞品 / 公司名，自动浏览官网与多个网页，生成结构化的竞品调研报告。

产品经理做竞品调研，通常要手动开一堆网页、搜索、复制粘贴、再汇总成报告，耗时且容易遗漏。这个项目用 **AI Agent 自动化完成「搜索 → 浏览 → 归纳 → 出报告」**，是「AI 在 B 端业务调研场景」的一个可运行 demo。

## 功能特性

- **网页界面**：双击 `运行.bat` 自动打开网页，在网页里输入竞品名即可（无需命令行）
- **一句话调研**：只需输入竞品名称，Agent 自动完成调研全流程
- **批量调研**：支持一次调研多个竞品，逐个生成报告
- **结构化报告**：输出 Markdown，包含产品定位、核心功能、目标用户、商业模式、技术亮点、竞品与市场动态
- **来源可追溯**：报告尽可能标注信息来源网址

## 演示

```bash
$ python main.py Dify RAGFlow

>>> 开始调研：Dify
✅ 已保存报告：reports/Dify_20260912_153000.md

>>> 开始调研：RAGFlow
✅ 已保存报告：reports/RAGFlow_20260912_153400.md
```

生成的报告示例（节选）：

```markdown
# 竞品调研报告：Dify
- 产品定位：开源 LLM 应用开发平台……
- 核心功能：可视化工作流编排 / RAG 知识库 / Agent……
- 商业模式：社区版免费 + 企业版订阅……
```

## 快速开始

### 1. 环境要求

- Python >= 3.11

### 2. 安装依赖

```bash
python -m venv .venv
# Windows
.venv\Scripts\pip install -r requirements.txt
# macOS / Linux
.venv/bin/pip install -r requirements.txt
```

### 3. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 DeepSeek key：

```
DEEPSEEK_API_KEY=sk-xxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
```

### 4. 运行

```bash
# Windows
.venv\Scripts\python.exe main.py Dify

# macOS / Linux
.venv/bin/python main.py Dify
```

**推荐方式（网页版）**：双击 `运行.bat`，浏览器会自动打开网页界面，在网页里输入竞品名即可；报告显示在网页上，同时保存到 `reports/`。

也可以运行命令行版 `python main.py Dify`（不传参则交互式输入竞品名称）。

## 技术架构

| 层 | 技术 | 说明 |
|----|------|------|
| 浏览器自动化引擎 | [browser-use](https://github.com/browser-use/browser-use) | 让 LLM 像人一样操控浏览器（开源，~114k star） |
| 大脑（LLM） | DeepSeek（`deepseek-chat`） | 负责规划步骤、理解网页、生成报告 |
| 任务设计 | `prompts.py` | 标准化的调研任务与报告结构（PM 的核心工作） |
| Web 界面 | Flask | 网页输入竞品名、展示报告（`app.py` + `templates/`） |
| 报告输出 | Markdown 文件 | 保存到 `reports/` 目录 |

**执行链路**：`输入竞品名 → 构造调研任务 prompt → browser-use Agent 操控浏览器搜索/浏览 → LLM 归纳 → 生成 Markdown 报告`。

## 目录结构

```
competitor-research-agent/
├── app.py              # Web 界面入口（Flask）
├── templates/          # 网页界面（index.html）
├── main.py             # 命令行入口
├── research_agent.py   # 核心 Agent 逻辑（调研 + 落盘）
├── prompts.py          # 调研任务与报告模板
├── requirements.txt    # 依赖声明
├── 运行.bat            # 双击启动（自动打开网页）
├── .env.example        # 配置模板
└── reports/            # 生成的报告（已 gitignore）
```

## 致谢与协议

- 本项目代码采用 **MIT License**。
- 核心浏览器自动化能力基于开源框架 [browser-use](https://github.com/browser-use/browser-use)（遵循其自身协议），本项目仅在其上做了「竞品调研」这一产品场景的封装与任务设计。
