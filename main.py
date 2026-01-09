# main.py
import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import threading

from core.logger import show_auto_close_message

# 项目根目录
ROOT_DIR = Path(__file__).parent.resolve()
ALLURE_RESULTS_DIR = ROOT_DIR / "reports" / "allure-results"
ALLURE_REPORT_DIR = ROOT_DIR / "reports" / "allure-report"


def ensure_directories():
    """确保报告目录存在"""
    # show_auto_close_message("正在创建报告目录...", "目录初始化")
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "reports" / "screenshots").mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "reports" / "traces").mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "reports" / "logs").mkdir(parents=True, exist_ok=True)
    # show_auto_close_message("报告目录创建完成", "目录初始化")


def run_tests(reruns=0, delay=1, open_report=True):
    """
    执行自动化测试并生成 Allure 报告

    :param reruns: 失败重试次数
    :param delay: 重试间隔（秒）
    :param open_report: 是否自动打开 Allure 报告
    """
    show_auto_close_message("🚀 开始执行自动化测试...", "测试开始")
    ensure_directories()

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]

    # 添加重试参数（如果需要）
    if reruns > 0:
        cmd.extend(["--reruns", str(reruns), "--reruns-delay", str(delay)])
        
    # 添加allure报告参数
    cmd.extend(["--alluredir", str(ALLURE_RESULTS_DIR)])

    try:
        # 执行测试
        # show_auto_close_message("正在执行测试...", "测试执行")
        result = subprocess.run(cmd, cwd=ROOT_DIR, check=False)
        show_auto_close_message(f"✅ 测试执行完成，退出码: {result.returncode}", "测试完成")

        if open_report and result.returncode == 0:
            generate_and_open_allure_report()

    except KeyboardInterrupt:
        show_auto_close_message("⚠️ 用户中断测试", "测试中断")
    except Exception as e:
        show_auto_close_message(f"❌ 执行失败: {e}", "执行失败")
        sys.exit(1)


def generate_and_open_allure_report():
    """生成并打开 Allure 报告"""
    show_auto_close_message("📊 正在生成 Allure 报告...", "报告生成")

    # 检查是否安装 allure 命令
    try:
        subprocess.run(["allure", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        msg = ("❗ 未检测到 'allure' 命令，请先安装 Allure CLI：\n"
               "Windows (推荐): scoop install allure\n"
               "或从 https://github.com/allure-framework/allure2/releases 下载并配置 PATH")
        show_auto_close_message(msg, "Allure缺失", 4000)
        return

    # 启动临时 Web 服务并打开浏览器
    # show_auto_close_message("🌐 启动 Allure 报告服务...", "报告服务")
    proc = subprocess.Popen([
        "allure", "serve", str(ALLURE_RESULTS_DIR)
    ])

    # 等待几秒让服务启动，然后打开浏览器
    time.sleep(3)
    webbrowser.open("http://localhost:59847")  # Allure serve 默认端口

    try:
        # show_auto_close_message("Allure报告服务已启动，按 Ctrl+C 停止", "报告服务")
        proc.wait()  # 保持服务运行
    except KeyboardInterrupt:
        # show_auto_close_message("🛑 停止 Allure 服务...", "服务停止")
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    # 可通过命令行参数控制行为
    import argparse

    parser = argparse.ArgumentParser(description="Playwright 自动化测试执行器")
    parser.add_argument("--no-open", action="store_true", help="不自动打开 Allure 报告")
    parser.add_argument("--reruns", type=int, default=0, help="失败重试次数（默认: 0）")
    parser.add_argument("--delay", type=int, default=1, help="重试间隔秒数（默认: 1）")

    args = parser.parse_args()

    run_tests(
        reruns=args.reruns,
        delay=args.delay,
        open_report=not args.no_open
    )