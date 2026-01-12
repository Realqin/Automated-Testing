from time import sleep
import pytest
from conftest import global_data
from core.Assertion import assert_value
from core.console import get_result_from_console
from core.logger import log_info, show_auto_close_message
from core.scroll_click import click_button_with_scroll

# 全局标记（模块级）
_high_filter_setup_done = False

@pytest.fixture(scope="class")
def prepare_high_filter_filter(page):
    global _high_filter_setup_done
    if not _high_filter_setup_done:
        log_info("首次执行：点击【目标筛选】→【高级筛选】")
        page.locator("text=目标筛选").click()
        # 注意：你原代码中是 "高级筛选筛选"，可能是笔误？通常应为 "高级筛选"
        page.locator("text=高级筛选").click()  # ← 建议确认文本是否正确
        _high_filter_setup_done = True
    else:
        log_info("已初始化一键筛选面板，跳过导航")
    return page





class TestAdvancedFilter:
    # 高级筛选 - 船名筛选
    @pytest.mark.parametrize("vessel_name", ["CHANG", "SHUN"])  # ← 在这里添加你要测的名称
    def test_01(self, prepare_high_filter_filter, vessel_name):
        page = prepare_high_filter_filter

        page.locator("#shipName").fill(vessel_name)
        click_button_with_scroll(page.locator(".sure-reload"),name="确 定")
        pytest.assume(assert_value(get_result_from_console(page,"vesselName"), vessel_name, "*"), f"船名与预期不匹配")
        click_button_with_scroll(page.locator(".sure-reload"), name="重 置")



        # button2 = page.locator(".nationalityFiltering__default").get_by_role("button", name='中国大陆', exact=True)
        # button2.scroll_into_view_if_needed()
        # sleep(2)
        # button2.click()


        # result = filter(page, "aa")  # 如果 filter 是自定义函数，需确保已定义
        # pytest.assume(assert_value(result, 'aa', "*"), f"与预期不匹配")
        # show_auto_close_message(f"筛选结果: {result}", "目标筛选")

    # # 目标类型筛选
    # def test_02(self, prepare_high_filter_filter):
    #     page = prepare_high_filter_filter
    #     page.locator(".targetTypeFiltering__content").get_by_role("button", name="雷 达", exact=True).click()

        # 目标类型筛选 —— 参数化支持多个按钮

    @pytest.mark.parametrize("button_name", ["雷 达", "AIS_A","AIS_B","北斗目标","雷达AIS_A", "雷达AIS_B", "其 他"])  # ← 在这里添加你要测的名称
    def test_02_target_type_filter(self, prepare_high_filter_filter, button_name):
        page = prepare_high_filter_filter
        log_info(f"正在点击目标类型按钮: {button_name}")

        # 先点击清除
        click_button_with_scroll(page.locator(".targetTypeFiltering__header"), name="清除")
        # 再点击目标类型按钮
        click_button_with_scroll(page.locator(".targetTypeFiltering__content"), name=button_name)
        pytest.assume(assert_value(get_result_from_console(page, "sClass"), 20, "<"), f"船名与预期不匹配")

