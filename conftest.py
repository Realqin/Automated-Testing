# conftest.py
import json
from time import sleep

import pytest
from playwright.sync_api import sync_playwright
from config.setting import *
from core.logger import show_auto_close_message, log_info, log_error
from core.request_api import request_api, get_first_non_empty_value
import allure
import os
from pathlib import Path


@pytest.fixture(scope="session")
def browser():
    """启动浏览器实例"""
    log_info("开始启动浏览器实例")
    with sync_playwright() as p:
        # 启用缓存并使用用户数据目录保存登录状态
        browser = p.chromium.launch(
            headless=False,
        )
        log_info("浏览器实例启动成功")
        yield browser
        browser.close()
        log_info("浏览器实例已关闭")


@pytest.fixture(scope="session")
def global_data():
    """获取全局公共参数的fixture"""
    show_auto_close_message("正在获取全局公共参数,请稍等..., ","参数获取")
    log_info("开始获取全局公共参数")
    # 在这里调用需要的API接口获取公共参数
    try:

        #前提：先登录获取到token
        log_info("正在请求登录接口获取token")
        response_token = request_api(f"{BASE_URL}/{API}/uaa/user/login", method="POST", data={"username": USERNAME, "password": PASSWORD,"grant_type":"password","tenantCode":90001})
        token = get_first_non_empty_value(response_token.json(),'$.data.tokenValue')

        # 调用目标接口，获取公共参数：mmsi,targetid,imo,呼号，北斗号，ais船名，北斗船名，船舶档案船名
        log_info("正在请求目标接口获取公共参数")
        response = request_api(f"{BASE_URL}/{API}/targetv2/target/all/simplified", method="POST", data=FILTER_PARAMS, headers={"Authorization": f"Bearer {token}"})
        response_bds = request_api(f"{BASE_URL}/{API}/targetv2/target/all/simplified", method="POST", data=FILTER_PARAMS_BDS, headers={"Authorization": f"Bearer {token}"})


        targetId = get_first_non_empty_value(response.json(),'$.data.data[*][0]')
        mmsi  =  get_first_non_empty_value(response.json(),'$.data.data[*][2]')
        callSign = get_first_non_empty_value(response.json(),'$.data.data[*][32]')
        imo = get_first_non_empty_value(response.json(),'$.data.data[*][31]')
        terminal = get_first_non_empty_value(response_bds.json(),'$.data.data[*][21]')
        vesselName = get_first_non_empty_value(response.json(),'$.data.data[*][14]')
        shipName = get_first_non_empty_value(response_bds.json(),'$.data.data[*][13]')

        log_info(f"获取到的参数: targetId={targetId}, mmsi={mmsi}, callSign={callSign}, imo={imo}, terminal={terminal}, vesselName={vesselName}, shipName={shipName}")

        global_params = {
            "token":token,
            "targetId": targetId,
            "mmsi": mmsi,
            "callSign": callSign,
            "imo": imo,
            "terminal": terminal,
            "vesselName": vesselName,  #目标的综合船名
            "shipName": shipName   #shipName是北斗目标的船名
            # "user_info": user_info,
            # 可以添加更多公共参数
        }
        
        # 遍历global_params字典并显示所有键值对
        params_info = "参数获取成功:\n"
        for key, value in global_params.items():
            # 对于较长的值（如token）进行截断处理，便于显示
            if isinstance(value, str) and len(value) > 50:
                display_value = value[:50] + "..."
            else:
                display_value = value
            params_info += f"{key}: {display_value}\n"
        
        show_auto_close_message(params_info.strip(), "参数获取成功")
        log_info("全局公共参数获取成功")
        return global_params
    except Exception as e:
        show_auto_close_message(f"获取全局公共参数失败: {str(e)}", "参数获取失败")
        log_error(f"获取全局公共参数失败: {str(e)}")
        raise


@pytest.fixture(scope="session")
def page(browser, global_data):
    """创建页面并执行登录"""
    log_info("开始创建页面并执行登录")
    # 创建带缓存的浏览器上下文
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        # 启用缓存
        java_script_enabled=True,
        # 设置用户代理
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # 创建trace目录
    trace_dir = Path("reports") / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace_path = trace_dir / "trace.zip"
    
    # 开始录制trace
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    page = context.new_page()
    
    # 设置导航超时为5分钟(300,000毫秒)
    page.set_default_navigation_timeout(300000)
    
    # 使用domcontentloaded事件而不是默认的load事件，加快页面加载速度
    log_info(f"正在导航到登录页面: {BASE_URL}/login")
    page.goto(f"{BASE_URL}/login", wait_until="load")
    
    # 此时global_data已经获取完成（因为它是此fixture的依赖）
    # 将全局数据存储在page对象中供测试用例使用
    page.global_data = global_data
    
    show_auto_close_message("正在执行登录", "登录")
    log_info("正在执行登录操作")
    # 等待并填写登录表单
    page.wait_for_selector("#username").fill(USERNAME)
    page.wait_for_selector("#password").fill(PASSWORD)
    page.wait_for_selector("button:has-text('登 录')").click()

    # 等待登录成功
    page.wait_for_selector("#exit")
    page.wait_for_load_state("networkidle")  # 或 "load"
    log_info("登录成功")

    #跳转到有目标的区域
    page.locator("xpath=//html/body/div[1]/div/div[1]/main/div/div[2]/div[10]/div[3]/div[1]/span").click()
    sleep(2)

    yield page

    try:
        # 结束trace录制
        context.tracing.stop(path=trace_path)
        
        # 添加截图附件
        screenshot_dir = Path("reports") / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / "final_screenshot.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        
        # 添加trace和截图作为allure附件
        with open(trace_path, "rb") as f:
            allure.attach(f.read(), name="Playwright Trace", attachment_type=allure.attachment_type.APPLICATION_ZIP)
            
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name="Final Screenshot", attachment_type=allure.attachment_type.PNG)
            
    except Exception as e:
        log_error(f"添加Allure附件时出错: {str(e)}")
    finally:
        context.close()
        log_info("页面上下文已关闭")