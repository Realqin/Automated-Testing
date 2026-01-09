# tests/test_target_search.py
from time import sleep

import pytest
import allure

from core.console import get_RealTimeTargetLog_data
from core.logger import show_auto_close_message, log_info, log_error
from core.Assertion import assert_value
from core.request_api import get_value



# 小目标：船长<20
# 高速目标：速度>=20

# 字段映射表（集中管理）
SEARCH_CONFIG = {
    "小目标": {"filter_key": "len","description":"船长<20米"},
    "高速目标": {"filter_key": "speed","description":"速度≥20节"},
    "低速目标": {"filter_key": "speed","description":"速度<2节"},
    "非大陆籍": {"filter_key": "mmsi","description":"MMSI非412,413,414开头，且属于正常国籍范围的船"},
    "渔船": {"filter_key": "shipType","description":"渔船"},
    "纯雷达": {"filter_key": "type","description":"纯雷达"},
    "AIS目标": {"filter_key": "type","description":"AIS目标"},
    "北斗目标": {"filter_key": "type","description":"北斗目标"},
    "AIS信息异常": {"filter_key": "mmsi","description":"AIS信息异常"}

    # "船舶目标": {"filter_key": "len","description":"船舶目标"},
}

# 全局标记（模块级）
_one_click_setup_done = False

@pytest.fixture(scope="function")
def prepare_one_click_filter(page):
    global _one_click_setup_done
    if not _one_click_setup_done:
        log_info("首次执行：点击【目标筛选】→【一键筛选】")
        page.locator("xpath=//html/body/div[1]/div/div[1]/main/div/div[2]/div[10]/div[3]/div[1]/span").click()
        sleep(2)
        # page.locator("text=环渤海").click()
        page.locator("text=目标筛选").click()
        page.locator("text=一键筛选").click()
        _one_click_setup_done = True
    else:
        log_info("已初始化一键筛选面板，跳过导航")
    return page



def perform_search_and_assert(page, filter,filter_key: str, Condition: str):
    try:

        # page.locator(f"text={filter}").click()
        # page.get_by_role("button", name="{filter}").click()

        page.locator(f"button:has-text('{filter}')").click()
        #制等2s，等待过滤响应
        sleep(2)
        # 等待数据就绪并获取
        result = page.wait_for_function(f"""
                   async () => {{
                       if (!window.g || typeof window.g.openRealTimeTargetLog !== 'function') 
                           return false;
                       const data = await window.g.openRealTimeTargetLog('{filter_key}');
                       // 自定义就绪条件，例如：有 logs 数组且非空
                       return data
                   }}
               """).json_value()
        print(result)
        if result:
            show_auto_close_message(f"{filter} 筛选结果: {get_RealTimeTargetLog_data(result)}", "目标筛选")
            if filter=="小目标":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 20, "<"),  f"{filter_key} 与预期不匹配")
            elif filter=="高速目标":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 20, ">="),  f"{filter_key} 与预期不匹配")
            elif filter=="低速目标":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 2, "<"),  f"{filter_key} 与预期不匹配")
            elif filter=="非大陆籍":
                # !^不以这些开头     !$不以这些结尾   * 包含   !* 不包含
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), ["412","413","414"], "!^"),  f"{filter_key} 与预期不匹配")
            elif filter=="渔船":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 1, "="),  f"{filter_key} 与预期不匹配")
            elif filter=="纯雷达":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), "RADAR", "="),  f"{filter_key} 与预期不匹配")
            elif filter=="AIS目标":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), "AIS", "*"),  f"{filter_key} 与预期不匹配")
            elif filter=="北斗目标":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), "BDS", "*"),  f"{filter_key} 与预期不匹配")
            elif filter=="AIS信息异常":
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), "9", "len()="),  f"{filter_key} 与预期不匹配")
                pytest.assume(assert_value(get_RealTimeTargetLog_data(result), "vesselName", "len()<"),
                              f"{filter_key} 与预期不匹配")
        else:
            show_auto_close_message(f"{filter} 筛选没有结果", "目标筛选")
            pytest.assume(True, f"{filter_key} 筛选结果为空,算测试通过")
        # elif filter=="AIS信息异常":
        #     pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 2, "<"),  f"{filter_key} 与预期不匹配")
        # elif filter=="船舶目标":
        #     pytest.assume(assert_value(get_RealTimeTargetLog_data(result), 2, "<"),  f"{filter_key} 与预期不匹配")




    except Exception as e:
        log_error(f"搜索 {filter} 时发生错误: {str(e)}")
        raise



# === 参数化测试用例 ===
@allure.feature("实时目标筛选-一键筛选")
@pytest.mark.parametrize("filter", ["小目标","高速目标","低速目标","非大陆籍","渔船","纯雷达","AIS目标","北斗目标"])
def test_target_filter_by_oneClick(prepare_one_click_filter, filter):
    """统一入口：通过不同字段搜索目标"""
    log_info(f"开始执行测试用例: test_target_filter_by_oneClick[{filter}]")
    page = prepare_one_click_filter
    config = SEARCH_CONFIG[filter]
    perform_search_and_assert(page, filter,config["filter_key"], config["description"])
    log_info(f"测试用例执行完成: test_target_filter_by_oneClick[{filter}]")
