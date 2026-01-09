import logging
import os
from datetime import datetime
import threading
import tkinter as tk
import time

from config.setting import LOG_DIR

# 创建日志目录
os.makedirs(LOG_DIR, exist_ok=True)

# 创建一个全局的日志记录器
logger = logging.getLogger("automated_testing")
logger.setLevel(logging.INFO)

# 防止重复添加处理器
if not logger.handlers:
    # 配置日志文件路径
    log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y%m%d')}.log")
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式器并添加到处理器
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg)

def log_warning(msg):
    logger.warning(msg)

def log_debug(msg):
    logger.debug(msg)

def show_auto_close_message(message, title="提示", duration=2000):
    """显示自动关闭的消息弹框"""
    def popup():
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        
        # 创建顶层窗口并直接居中显示
        top = tk.Toplevel(root)
        top.title(title)
        top.geometry("300x100")
        top.resizable(False, False)
        top.attributes("-topmost", True)
        
        # 计算居中位置
        x = (top.winfo_screenwidth() // 2) - (300 // 2)
        y = (top.winfo_screenheight() // 2) - (100 // 2)
        top.geometry(f"300x100+{x}+{y}")
        
        # 添加消息标签
        label = tk.Label(top, text=message, wraplength=280)
        label.pack(expand=True)
        
        # 确保窗口显示
        top.update_idletasks()
        
        # 自动关闭
        top.after(duration, top.destroy)
        root.after(duration, root.quit)
        
        top.mainloop()
        root.mainloop()
        
    thread = threading.Thread(target=popup, daemon=True)
    thread.start()
    # 等待一段时间确保弹框显示
    time.sleep(duration / 1000.0)