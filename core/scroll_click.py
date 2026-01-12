from time import sleep

from playwright.sync_api import Locator


def click_button_with_scroll(
        base_locator: Locator,
        name: str = None,
        exact: bool = True,
        wait_after_click: float = 2.0
):
    """
    智能点击按钮：支持两种模式

    模式1（仅定位器）:
        click_button_with_scroll(page.locator(".sure-reload"))

    模式2（定位器 + 按钮文本）:
        click_button_with_scroll(page.locator(".sure-reload"), name="确 定", exact=True)

    :param base_locator: 基础定位器（如 page.locator(".sure-reload")）
    :param name: 按钮显示文本（如 "确 定"），若提供则在 base_locator 内部查找
    :param exact: 是否精确匹配文本
    :param wait_after_click: 点击后等待时间（秒）
    """
    if name is not None:
        # 模式2：在 base_locator 范围内按角色+文本过滤
        button = base_locator.get_by_role("button", name=name, exact=exact)
    else:
        # 模式1：直接使用 base_locator 作为按钮
        button = base_locator

    # 自动滚动到可见区域
    button.scroll_into_view_if_needed()

    # 等待可点击（增强稳定性）
    button.wait_for(state="visible", timeout=5000)

    # 点击
    button.click()

    # 点击后等待（可配置）
    if wait_after_click > 0:
        sleep(wait_after_click)