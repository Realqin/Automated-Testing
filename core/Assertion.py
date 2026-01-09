def assert_value(actual, expected, compare_type="*"):
    """
    统一断言函数，根据actual参数的结构自动选择断言方式
    :param actual: 实际值，可以是普通列表或嵌套列表
    :param expected: 预期值，可以是单个值或列表（多个预期值）
    :param compare_type: 比较类型，支持 '=', '包含', '>', '>=', '<', '<='  # !^不以这些开头     !$不以这些结尾   * 包含   !* 不包含
    :return: bool 断言结果

    示例1（普通列表）：判断接口提取到的北斗号都等于456772：([4567721,4567722,456772],456772,"=")
    示例2（嵌套列表）：对于列表[[1,2],[3,4],[5,6]]，查找每个子列表中是否包含3
    示例3：期望[1,3] - 实际值包含1或3中的任何一个都算通过
    """
    # 检查输入参数
    if not isinstance(actual, list):
        print(f'实际值必须是列表类型，当前类型为{type(actual)}')
        return False

    # 将expected转换为列表形式，方便统一处理
    if not isinstance(expected, list):
        expected_list = [expected]
    else:
        expected_list = expected

    # 判断是否为嵌套列表（至少有一个元素是列表）
    is_nested = any(isinstance(item, list) for item in actual)

    if is_nested:
        # 嵌套列表逻辑
        for i, sublist in enumerate(actual):
            # 检查子列表是否为列表类型
            if not isinstance(sublist, list):
                print(f'第{i + 1}个元素不是列表类型')
                return False

            # 检查子列表中是否至少有一个元素匹配任何一个预期值
            found = False
            for item in sublist:
                for exp in expected_list:
                    if str(exp).strip().upper() in str(item).strip().upper():
                        found = True
                        break
                if found:
                    break

            # 如果当前子列表中没有找到匹配任何一个预期值，则断言失败
            if not found:
                print(f'在子列表{sublist}中未找到任何一个预期值{expected_list}')
                return False

        return True
    else:
        # 普通列表逻辑
        if compare_type == "=":
            # 检查实际列表中的每个元素是否等于任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    # 获取实际值的类型
                    if type(i) == type(exp):
                        # 类型相同直接比较
                        if exp == i:
                            matched = True
                            break
                    else:
                        # 类型不同，都转为字符串比较
                        if str(exp).strip().upper() == str(i).strip().upper():
                            matched = True
                            break

                if not matched:
                    print(f'实际值{i}不等于任何一个预期值{expected_list}')
                    return False

        elif compare_type == "*":
            # 检查实际列表中的每个元素是否包含任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    if str(exp).strip().upper() in str(i).strip().upper():
                        matched = True
                        break

                if not matched:
                    print(f'实际值{i}不包含任何一个预期值{expected_list}')
                    return False

        elif compare_type == "!*":
            # 检查实际列表中的每个元素是否不包含所有预期值
            for i in actual:
                for exp in expected_list:
                    if str(exp).strip().upper() in str(i).strip().upper():
                        print(f'实际值{i}包含了预期值{exp}')
                        return False

        elif compare_type == "^":  # 以任何一个预期值开头
            # 检查实际列表中的每个元素是否以任何一个预期值开头
            for i in actual:
                matched = False
                for exp in expected_list:
                    if str(i).strip().upper().startswith(str(exp).strip().upper()):
                        matched = True
                        break

                if not matched:
                    print(f'实际值{i}不以任何一个预期值{expected_list}开头')
                    return False

        elif compare_type == "!^":  # 不以任何一个预期值开头
            # 检查实际列表中的每个元素是否不以任何一个预期值开头
            for i in actual:
                for exp in expected_list:
                    if str(i).strip().upper().startswith(str(exp).strip().upper()):
                        print(f'实际值{i}以预期值{exp}开头')
                        return False

        elif compare_type == "$":  # 以任何一个预期值结尾
            # 检查实际列表中的每个元素是否以任何一个预期值结尾
            for i in actual:
                matched = False
                for exp in expected_list:
                    if str(i).strip().upper().endswith(str(exp).strip().upper()):
                        matched = True
                        break

                if not matched:
                    print(f'实际值{i}不以任何一个预期值{expected_list}结尾')
                    return False

        elif compare_type == "!$":  # 不以任何一个预期值结尾
            # 检查实际列表中的每个元素是否不以任何一个预期值结尾
            for i in actual:
                for exp in expected_list:
                    if str(i).strip().upper().endswith(str(exp).strip().upper()):
                        print(f'实际值{i}以预期值{exp}结尾')
                        return False

        elif compare_type == ">":
            # 检查实际列表中的每个元素是否大于任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    try:
                        if float(i) > float(exp):
                            matched = True
                            break
                    except ValueError:
                        print(f'无法将{i}或{exp}转换为数值类型')
                        return False

                if not matched:
                    print(f'实际值{i}不大于任何一个预期值{expected_list}')
                    return False

        elif compare_type == ">=":
            # 检查实际列表中的每个元素是否大于等于任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    try:
                        if float(i) >= float(exp):
                            matched = True
                            break
                    except ValueError:
                        print(f'无法将{i}或{exp}转换为数值类型')
                        return False

                if not matched:
                    print(f'实际值{i}不小于任何一个预期值{expected_list}')
                    return False

        elif compare_type == "<":
            # 检查实际列表中的每个元素是否小于任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    try:
                        if float(i) < float(exp):
                            matched = True
                            break
                    except ValueError:
                        print(f'无法将{i}或{exp}转换为数值类型')
                        return False

                if not matched:
                    print(f'实际值{i}不小于任何一个预期值{expected_list}')
                    return False

        elif compare_type == "<=":
            # 检查实际列表中的每个元素是否小于等于任何一个预期值
            for i in actual:
                matched = False
                for exp in expected_list:
                    try:
                        if float(i) <= float(exp):
                            matched = True
                            break
                    except ValueError:
                        print(f'无法将{i}或{exp}转换为数值类型')
                        return False

                if not matched:
                    print(f'实际值{i}不小于等于任何一个预期值{expected_list}')
                    return False

        else:
            print(f'不支持的比较类型: {compare_type}')
            return False

        return True


# 测试用例
if __name__ == "__main__":
    # 测试1: expected为列表，type="*"（包含）
    print("测试1 - 包含任何一个预期值:")
    actual = ["apple123", "banana456", "cherry789"]
    expected = ["apple", "grape"]  # 包含apple或grape都算通过
    result = assert_value(actual, expected, "*")
    print(f"结果: {result}")

    # 测试2: expected为列表，type="="（等于）
    print("\n测试2 - 等于任何一个预期值:")
    actual = [100, 200, 300]
    expected = [200, 400]  # 等于200或400都算通过
    result = assert_value(actual, expected, "=")
    print(f"结果: {result}")

    # 测试3: expected为列表，type="^"（以...开头）
    print("\n测试3 - 以任何一个预期值开头:")
    actual = ["error001", "warning002", "info003"]
    expected = ["error", "warn"]  # 以error或warn开头都算通过
    result = assert_value(actual, expected, "^")
    print(f"结果: {result}")

    # 测试4: expected为单个值，向后兼容
    print("\n测试4 - 单个预期值（向后兼容）:")
    actual = ["test123", "test456", "test789"]
    expected = "test"  # 单个值
    result = assert_value(actual, expected, "*")
    print(f"结果: {result}")

    # 测试5: 数值比较
    print("\n测试5 - 大于任何一个预期值:")
    actual = [50, 60, 70]
    expected = [55, 65]  # 大于55或65都算通过
    result = assert_value(actual, expected, ">")
    print(f"结果: {result}")