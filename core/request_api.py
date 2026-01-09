import json

import jsonpath
import requests
from jsonpath import JSONPath

from core.logger import show_auto_close_message, log_info, log_error


def request_api(url, method="GET", params=None, data=None, headers=None, timeout=10):
    """
    封装通用的API调用函数

    Args:
        url (str): 接口地址
        method (str): 请求方法，默认为GET
        params (dict): URL参数，默认为None
        data (dict): 请求体数据，默认为None
        headers (dict): 请求头，默认为None
        timeout (int): 超时时间，默认为10秒

    Returns:
        response: requests.Response对象

    Raises:
        requests.RequestException: 请求异常
    """
    try:
        log_info(f"正在调用接口: {method} {url}")
        show_auto_close_message(f"正在调用接口: {method} {url}", "接口调用")

        # 使用requests.request简化代码
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=headers,
            timeout=timeout
        )

        response.raise_for_status()
        log_info(f"接口调用成功: {response.status_code}")
        show_auto_close_message(f"接口调用成功: {response.status_code}", "接口调用成功")
        return response
    except requests.RequestException as e:
        log_error(f"接口调用失败: {str(e)}")
        show_auto_close_message(f"接口调用失败: {str(e)}", "接口调用失败")
        raise



# 获取第一个不为空的值的辅助函数
def get_first_non_empty_value(json, path):
    """
    从数据中按优先级获取第一个不为空的值
    :param data: 数据字典
    :param keys: 键名列表，按优先级排序
    :return: 第一个不为空的值，如果没有则返回None
    """

    try:
        values = JSONPath(path).parse(json)
        log_info(f"尝试从JSON路径 {path} 获取值")
        if values:
            # 遍历数组，返回第一个不为 None 或空字符串的值
            for value in values:
                if value is not None and value != "" and value != 0 and value != "None" and len(str(value))>=4:
                    log_info(f"成功获取到值: {value}")
                    return value
        log_info("未能获取到有效的值")
        return None
    except Exception as e:
        log_error(f"没有获取到值: {str(e)}")
        print(f"没有获取到值")
        return None

def get_value(json, path):
    """
    从数据中按优先级获取值，支持单路径和多路径(逗号分隔)
    :param json: JSON数据
    :param path: JSON路径字符串，可以是单个路径或逗号分隔的多个路径
    :return: 单路径时返回第一个不为空的值，多路径时返回按路径分组的值列表
    """
    
    # 判断是否为多路径
    if ',' in path:
        # 多路径处理逻辑
        paths = path.split(',')
        result = []
        
        # 对每个路径提取值
        for p in paths:
            p = p.strip()  # 去除空格
            try:
                values = JSONPath(p).parse(json)
                log_info(f"从JSON路径 {p} 获取值: {values}")
                if values is not None:
                    # 如果返回的是单个值而非列表，将其包装成列表
                    if not isinstance(values, list):
                        values = [values]
                    result.append(values)
                else:
                    # 如果没有提取到值，添加一个空列表占位
                    result.append([])
            except Exception as e:
                log_error(f"从路径 {p} 获取值时出错: {str(e)}")
                # 出错时添加空列表占位
                result.append([])
        
        # 转置结果，使同一索引的数据项组合在一起
        # 例如：[[1,2,3],[1,2,4],[2,2,4]] 表示有3条记录，每条记录包含3个字段
        if not result:
            return []
        
        # 计算最大长度
        max_length = max(len(r) for r in result) if result else 0
        
        # 创建转置后的结果
        transposed_result = []
        for i in range(max_length):
            row = []
            for r in result:
                if i < len(r):
                    row.append(r[i])
                else:
                    row.append(None)  # 缺少字段的用None补充
            transposed_result.append(row)
        
        return transposed_result
    else:
        # 单路径处理逻辑
        try:
            value = JSONPath(path).parse(json)
            log_info(f"从JSON路径 {path} 获取值: {value}")
            if value is not None and value != "" and value != 0 and value != "None":
                return value
        except Exception as e:
            log_error(f"没有获取到值: {str(e)}")
            print(f"没有获取到值")
            return None