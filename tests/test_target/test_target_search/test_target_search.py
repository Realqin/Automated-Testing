# tests/test_target_search.py
from time import sleep

import pytest
import allure
from core.logger import show_auto_close_message, log_info, log_error
from core.Assertion import assert_value
from core.request_api import get_value

# 字段映射表（集中管理）
SEARCH_CONFIG = {
    "targetId": {"field_name": "目标ID", "json_path": "$..targetId"},
    "mmsi": {"field_name": "MMSI", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
    "callSign": {"field_name": "呼号", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
    "imo": {"field_name": "IMO", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
    "terminal": {"field_name": "北斗号", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
    "vesselName": {"field_name": "北斗船名", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
    "shipName": {"field_name": "船名", "json_path": "$..callSign,$..targetId,$..mmsi,$..vesselName,$..shipName,$..imo"},
}

# 用提取到的参数值：船名、MMSI、呼号、IMO号、北斗号、ID进行搜索
def perform_search_and_assert(page, search_key: str, search_value: str, json_path: str):
    """公共搜索验证逻辑"""
    log_info(f"正在搜索 {search_key}: {search_value}")
    show_auto_close_message(f"正在搜索 {search_key}: {search_value}", "目标搜索")

    try:
        with page.expect_response("**/target/search*") as response_info:
            # 使用更精确的选择器定位输入框
            input_box = page.locator("xpath=//html/body/div[1]/div/div[1]/main/div/div[1]/div[11]/div/div/div/ul/li/div/input")
            # 确保 search_value 是字符串类型
            input_box.fill(str(search_value))
            input_box.press("Enter")  # 根据实际需要保留或删除
            # sleep(2)

            response = response_info.value
            log_info(f"接口返回状态码: {response.status}")
            pytest.assume(response.status == 200, f"接口返回状态码异常:{response.status}")

            actual_returned = get_value(response.json(), json_path)
            log_info(f"期望值: {search_value}, 实际返回值: {actual_returned}")
            pytest.assume(assert_value(actual_returned, search_value, "包含"), f"{search_key} 返回值不一致")
    except Exception as e:
        log_error(f"搜索 {search_key} 时发生错误: {str(e)}")
        raise


# === 参数化测试用例 ===
@allure.feature("目标搜索功能")
@pytest.mark.parametrize("search_key", ["mmsi","callSign", "imo", "terminal", "vesselName", "shipName","targetId"])
def test_target_search_by_field(page, global_data, search_key):
    """统一入口：通过不同字段搜索目标"""
    log_info(f"开始执行测试用例: test_target_search_by_field[{search_key}]")
    config = SEARCH_CONFIG[search_key]
    value = global_data[search_key]
    perform_search_and_assert(page, config["field_name"], value, config["json_path"])
    log_info(f"测试用例执行完成: test_target_search_by_field[{search_key}]")