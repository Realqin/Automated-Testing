import json

from core.logger import show_auto_close_message


#console返回的数据格式为：{"2512161632394061916":"30.4","2512160637024012186":"20.8"},需要把字符串里的数据提取出来
def get_RealTimeTargetLog_data(data):
    """
    从控制台返回的实时目标日志数据中提取数据
    
    Args:
        data (str/dict): 控制台返回的数据，可能是字符串格式的JSON或已经是字典
        
    Returns:
        list: 包含提取的数据的列表，每个元素是一个(key, value)元组
    """
    # 如果data是字符串，则解析为JSON对象
    if isinstance(data, str):
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            # 如果解析失败，返回空列表
            return []
    elif isinstance(data, dict):
        # 如果data已经是一个字典，直接使用
        parsed_data = data
    else:
        # 如果data既不是字符串也不是字典，返回空列表
        return []
    
    # 提取所有的键值对，转换为列表形式
    result_list = list(parsed_data.values())
    
    return result_list


# 弹框提示console过滤后的结果，并返回
def get_result_from_console(page, filter_key: str):
    result = page.wait_for_function(f"""
               async () => {{
                   if (!window.g || typeof window.g.openRealTimeTargetLog !== 'function') 
                       return false;
                   const data = await window.g.openRealTimeTargetLog('{filter_key}');
                   // 自定义就绪条件，例如：有 logs 数组且非空
                   return data
               }}
           """).json_value()
    final_result = get_RealTimeTargetLog_data(result)
    if result:
        show_auto_close_message(f"{filter_key} 筛选结果: {final_result}", "目标筛选")
    return final_result