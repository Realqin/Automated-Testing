# mapping.py 或 utils.py

# ====== 通过名字找实际要过滤的值
TYPE_MAPPING = {
    "雷达": "RADAR",
    "AIS_A": "AIS_A",
    "AIS_B": "AIS_B",
    "北斗目标": "BEIDOU",
    "雷达AIS_A": "RADAR_AIS_A",
    "雷达AIS_B": "RADAR_AIS_B",
    "雷达北斗": "RADAR_BEIDOU",
    "光电目标": "PHOTOELECTRIC",
    "雷达光电": "RADAR_PHOTOELECTRIC",
    "雷达AB北斗": "RADAR_AB_BEIDOU",
    "光电信号": "PHOTOELECTRIC_SIGNAL",
    "其他": "OTHER",
    "渔船": "1",
    "货船": "2",
    "客船": "3",
    "油船": "4",
    "公务船": "5",
    "作业船": "8",
    "拖船": "10",
    "其他": "9"
}


def get_type_value(display_name: str) -> str:
    """
    获取目标类型的后端值

    示例:
        get_target_type_value("雷达") → "RADAR"
        get_target_type_value("AIS_A") → "AIS_A"
    """
    if display_name not in TYPE_MAPPING:
        raise ValueError(f"未知的目标类型: {display_name}")
    return TYPE_MAPPING[display_name]
