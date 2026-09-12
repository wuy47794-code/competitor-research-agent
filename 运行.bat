@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

if not exist .env (
    echo ============================================
    echo   [错误] 缺少 .env 文件
    echo   请复制 .env.example 为 .env，并填入 DEEPSEEK_API_KEY
    echo ============================================
    pause
    exit /b 1
)

echo.
echo ============================================
echo   竞品调研 Agent 正在启动...
echo.
echo   1) 这个黑窗口是"服务器"，请保持打开，不要关闭！
echo   2) 浏览器会自动弹出网页（约 1~2 秒后）
echo   3) 如果浏览器没自动弹出，请手动打开浏览器，
echo      在地址栏输入并回车：
echo.
echo          http://127.0.0.1:5000
echo.
echo ============================================
echo.

.venv\Scripts\python.exe app.py
echo.
pause
