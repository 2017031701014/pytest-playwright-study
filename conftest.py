from typing import Any

import tkinter as tk

import pandas as pd
from pathlib import Path

from fixtures import *

# pytest_configure 是 pytest 在启动时，会自动查找并调用的函数
# config 是 pytest 传进来的全局配置对象。
def pytest_configure(config):
# addinivalue_line 是它的一个方法，意思是：往某个配置项里追加一行内容。
    config.addinivalue_line(
        "markers", "test_id: 指定用例 ID，用于定位对应的 CSV 数据文件"
    )
# 这里的配置项是 "markers"，也就是 marker 列表。
# 第二个参数是你要追加的那一行字符串
# 格式是marker名字: 说明文字

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

# 数据文件存放的根目录，你可以根据需要修改
# __file__ 这是 Python 的一个内置变量，代表当前正在执行的脚本文件的路径。 在你的场景里，这段代码写在 conftest.py 中，所以 __file__ 就是 conftest.py 这个文件的路径。
# Path(__file__) 把上面那个文件路径字符串，转换成一个 pathlib.Path 对象。 用来优雅地处理文件路径.
# .parent 获取当前文件（conftest.py）所在的上一级目录（也就是文件夹）。

# / 不是字符串里的斜杠，而是 Path 对象重载的运算符
# 这里的 DATA_DIR 是一个 Path 对象（在 Windows 上是 WindowsPath），不是普通的字符串。
# Python 实际调用的是 Path 类里的 __truediv__ 方法。这个方法会根据当前操作系统自动使用正确的路径分隔符。
# 在 Windows 上，它内部会使用 \
# 在 Linux/Mac 上，它内部会使用 /
DATA_DIR = Path(__file__).parent / "data"
@pytest.fixture
#request 是 pytest 自动传给你的一个内置 fixture，它代表了当前正在执行的测试用例的上下文信息
# 只要你把 request 写进 fixture 函数的参数列表，pytest 就认识它。
# request 是一个对象，上面挂了很多属性,request.node.get_closest_marker("test_id")就是用来读取marker的
def data(request):
    # 读取 @pytest.mark.test_id("FTM-999")
    # request 是请求单，负责管理这次 fixture 调用的上下文（配置、参数、路径）。
    # request.node 是实际被执行的测试函数/节点，标记、名字、函数对象都挂在它身上。
    # 所以凡是要拿测试函数身上的东西（marker、name、function），就要通过 request.node。
    # 凡是要拿本次请求或全局的东西（config、param、fspath），直接在 request 上就行
    marker = request.node.get_closest_marker("test_id")

    # pytest.UsageError，这是 pytest 自己定义的一个异常类型，专门用来表示“用户用错了 pytest”，比如：
    # 命令行参数写错了
    # 配置有问题
    # 缺少必要的标记或环境
    if marker is None:
        raise pytest.UsageError(
            f"测试用例 {request.node.name} 缺少 @pytest.mark.test_id 标记"
        )
    if not marker.args:
        raise pytest.UsageError(
            f"测试用例 {request.node.name} 的 @pytest.mark.test_id 没有传 ID"
        )

    # pytest 会把 marker 括号里传的位置参数收集到 marker.args 里，类型是一个元组。
    # @pytest.mark.test_id("FTM-999") ->  marker.args == ("FTM-999",) -> 它是一个元组，里面只有一个元素 "FTM-999"。
    # marker.args[0] 就是 marker 里传的第一个参数，也就是 "FTM-999"
    case_id = str(marker.args[0])   # "FTM-999"

    data_file = DATA_DIR / f"{case_id}.csv" #from pathlib import Path， 这个/是Path的语法，就是下一层的路径

    if not data_file.exists():
        raise FileNotFoundError(
            f"找不到数据文件: {data_file} (用例ID: {case_id})"
        )
    # 在 f-string 里写 {data_file}，Python 会自动把它转成字符串，Path 对象本身也支持这种转换。

    return pd.read_csv(str(data_file)).fillna("")  #type:ignore
    # pd.read_csv(...) 返回的是一个 pandas.DataFrame 对象
    # pd.read_csv() 是 pandas 用来读取 CSV 文件的核心函数。它会把 CSV 文件里的表格数据，转换成 pandas 的 二维表格对象（DataFrame）
    #df 就是这样一个 DataFrame：
    """
        AAA	BBB
    0	v1	b1
    1	v2	b2
    2	v3	b3 
    """