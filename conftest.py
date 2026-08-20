from typing import Any

import pytest
from playwright.sync_api import Page

import tkinter as tk

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args): #传入的参数是字典
    print("browser_context_args 已被加载")
    try:
        # 获取屏幕分辨率（在加载时执行一次）
        root = tk.Tk()
        root.withdraw()  # 不显示 tkinter 窗口
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        # 覆盖默认的上下文参数
    except (tk.TclError, ImportError):
        screen_width=1920
        screen_height=1080
    return {
        **browser_context_args, #**表示把原来的字典加进来
        "viewport": {"width": screen_width, "height": screen_height},
        "record_video_dir": "videos/",   # 自动录屏
    }

@pytest.fixture(scope="function")
def page(page: Page) -> Page|None|Any:
    print("page的config已经加载")
    # 可以在每个测试前后添加额外操作，例如自动登录
    page.goto("https://www.baidu.com")
    yield page
    # 测试结束后会自动关闭 page（插件已处理）
    print("execute after finishing the test case")
