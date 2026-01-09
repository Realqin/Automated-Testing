from time import sleep
import pytest
from conftest import global_data
from core.Assertion import assert_value
from core.logger import log_info, show_auto_close_message

# 全局标记（模块级）
_one_click_setup_done = False

@pytest.fixture(scope="class")
def prepare_one_click_filter1(page):
    global _one_click_setup_done
    if not _one_click_setup_done:
        log_info("首次执行：点击【目标筛选】→【高级筛选】")
        page.locator("text=目标筛选").click()
        # 注意：你原代码中是 "高级筛选筛选"，可能是笔误？通常应为 "高级筛选"
        page.locator("text=高级筛选").click()  # ← 建议确认文本是否正确
        _one_click_setup_done = True
    else:
        log_info("已初始化一键筛选面板，跳过导航")
    return page


# core/utils.py

from playwright.sync_api import Page, Locator


def click_button_by_name(page: Page, name: str, exact: bool = True, timeout: float = 5000):
    """
    智能点击按钮：自动滚动到可见区域再点击

    :param page: Playwright Page 对象
    :param name: 按钮显示文本（如 "雷 达"）
    :param exact: 是否精确匹配文本
    :param timeout: 查找超时时间（毫秒）
    """
    button = page.get_by_role("button", name=name, exact=exact)

    # 自动等待并滚动到可见区域（Playwright 内置方法）
    button.scroll_into_view_if_needed(timeout=timeout)

    # 确保可点击（避免被遮挡）
    button.wait_for(state="visible", timeout=timeout)
    button.wait_for(state="enabled", timeout=timeout)

    button.click()

class TestAdvancedFilter:
    # 高级筛选 - 船名筛选
    def test_01(self, prepare_one_click_filter1):
        page = prepare_one_click_filter1
        page.locator("#shipName").fill('aa')

        button = page.locator(".sure-reload").get_by_role("button", name='确 定', exact=True)
        button.scroll_into_view_if_needed()
        button.click()
        sleep(2)

        button2 = page.locator(".nationalityFiltering__default").get_by_role("button", name='中国大陆', exact=True)
        button2.scroll_into_view_if_needed()
        sleep(2)
        button2.click()


        # result = filter(page, "aa")  # 如果 filter 是自定义函数，需确保已定义
        # pytest.assume(assert_value(result, 'aa', "*"), f"与预期不匹配")
        # show_auto_close_message(f"筛选结果: {result}", "目标筛选")

    # # 目标类型筛选
    # def test_02(self, prepare_one_click_filter1):
    #     page = prepare_one_click_filter1
    #     page.locator(".targetTypeFiltering__content").get_by_role("button", name="雷 达", exact=True).click()

        # 目标类型筛选 —— 参数化支持多个按钮

    @pytest.mark.parametrize("button_name", ["雷 达", "AIS_A","AIS_B","雷达AIS_A", "雷达AIS_B", "其 他"])  # ← 在这里添加你要测的名称
    def test_02_target_type_filter(self, prepare_one_click_filter1, button_name):
        page = prepare_one_click_filter1
        log_info(f"正在点击目标类型按钮: {button_name}")
        # 先点击清除
        page.locator(".targetTypeFiltering__group").get_by_role("button", name='清除', exact=True).click()

        # 从 .targetTypeFiltering__content 容器中查找 exact 匹配的按钮
        page.locator(".targetTypeFiltering__content").get_by_role("button", name=button_name, exact=True).click()
        sleep(2)
