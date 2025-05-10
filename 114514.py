# 使用一个集合来存储已经找到并打印的解，避免重复输出
solutions_set = set()
# 全局目标数字
aim_number_global = 0
# 原始dic字符串
dic_global = '114514'

def generate_number_partitions_recursive(s, current_s_idx, current_partition_list, all_partitions_result):
    """
    递归地将字符串s拆分为所有可能的数字列表组合。
    例如 "123" -> [[1,2,3], [1,23], [12,3], [123]]
    """
    if current_s_idx == len(s):
        if current_partition_list: # 确保当前组合不为空
            all_partitions_result.append(list(current_partition_list)) # 添加副本
        return

    for i in range(current_s_idx + 1, len(s) + 1):
        num_str = s[current_s_idx:i]
        current_partition_list.append(int(num_str))
        generate_number_partitions_recursive(s, i, current_partition_list, all_partitions_result)
        current_partition_list.pop() # 回溯

def solve_expressions_recursive(
    ops_count,           # 当前已使用的操作数/数字个数
    current_value,       # 当前表达式的计算结果
    current_eq_str,      # 当前构建的表达式字符串
    numbers_to_use,      # 剩余待使用的数字列表
    target_value,        # 目标计算结果
    max_allowed_ops      # 最大允许的操作数/数字个数
):
    """
    递归尝试所有运算组合，寻找目标值。
    只有当分区中的所有数字都被使用并且结果匹配时才打印。
    """
    # 基本情况：当前分区的所有数字都已处理完毕
    if not numbers_to_use:
        if current_value == target_value and ops_count > 0: # ops_count > 0 确保至少用了一个数字
            # current_eq_str 格式为 "  op1 N1 op2 N2 ..."
            # 我们需要移除开头的 "  op1 " 部分，得到 "N1 op2 N2 ..."
            final_eq_str_to_print = current_eq_str[3:] # "  + N1" -> "N1"
            solution_output_str = f"{final_eq_str_to_print} = {int(current_value)}"
            if solution_output_str not in solutions_set:
                print(solution_output_str)
                solutions_set.add(solution_output_str)
        return

    # 基本情况：达到最大操作/数字数量限制
    if ops_count >= max_allowed_ops:
        return

    num_from_list = numbers_to_use[0]
    remaining_nums_list = numbers_to_use[1:]

    # 尝试加法
    next_value_add = current_value + num_from_list
    next_eq_str_add = current_eq_str + " + " + str(num_from_list)
    solve_expressions_recursive(ops_count + 1, next_value_add, next_eq_str_add, remaining_nums_list, target_value, max_allowed_ops)

    # 尝试减法 (约束: current_value - num_from_list > 0)
    # 注意：此约束意味着如果 current_value 为 0 (初始调用时)，则 0 - num_from_list > 0 永不为真。
    # 这有效地阻止了以负数开头的表达式，除非第一个数字本身能使 current_value > 0 (例如通过加法)。
    # 这与原始代码的行为一致。
    next_value_sub = current_value - num_from_list
    if next_value_sub > 0:
        next_eq_str_sub = current_eq_str + " - " + str(num_from_list)
        solve_expressions_recursive(ops_count + 1, next_value_sub, next_eq_str_sub, remaining_nums_list, target_value, max_allowed_ops)
    
    # 尝试乘法 (约束: current_value != 0 因为 num_from_list 来自 "114514" 不为0)
    # 如果 current_value 为 0 (初始调用时)，此操作将被跳过。
    if current_value != 0:
        next_value_mul = current_value * num_from_list
        next_eq_str_mul = current_eq_str + " * " + str(num_from_list)
        solve_expressions_recursive(ops_count + 1, next_value_mul, next_eq_str_mul, remaining_nums_list, target_value, max_allowed_ops)

    # 尝试除法 (约束: num_from_list != 0, current_value % num_from_list == 0, 结果 != 0)
    # 如果 current_value 为 0 (初始调用时)，current_value % num_from_list == 0 为真，但 current_value // num_from_list = 0，所以结果 !=0 条件不满足。
    if num_from_list != 0 and current_value % num_from_list == 0: # num_from_list != 0 是防御性检查
        next_value_div = current_value // num_from_list
        if next_value_div != 0:
            next_eq_str_div = current_eq_str + " / " + str(num_from_list)
            solve_expressions_recursive(ops_count + 1, next_value_div, next_eq_str_div, remaining_nums_list, target_value, max_allowed_ops)

def main():
    global aim_number_global # 声明使用全局变量
    aim_number_global = int(input("输入目标数字："))
    max_ops_input = int(input("输入最大操作数/数字数量 (例如，1 到 {}，或更大以使用重复序列): ".format(len(dic_global))))

    if max_ops_input <= 0:
        print("最大操作数必须大于0")
        return

    # 计算 dic_global 需要重复的次数
    # 确保 effective_dic 至少有 dic_global 那么长，并且足够长以支持 max_ops_input 个数字（假设每个数字至少1位）
    num_repetitions = 1
    if max_ops_input > len(dic_global):
        # 如果每个数字至少一位，我们需要一个长度至少为 max_ops_input 的源字符串
        num_repetitions = (max_ops_input + len(dic_global) - 1) // len(dic_global)
    
    effective_dic = dic_global * num_repetitions
    
    all_partitions = []
    generate_number_partitions_recursive(effective_dic, 0, [], all_partitions)
    
    solutions_set.clear() # 清空上一轮的解 (如果多次调用main)

    found_solution = False
    for num_list_partition in all_partitions:
        if not num_list_partition: # 跳过空分区
            continue
        
        # 只考虑长度不超过用户指定最大操作数的分区
        if len(num_list_partition) > max_ops_input:
            continue
        
        # 对于符合长度要求的分区，尝试用其所有数字求解
        # max_allowed_ops 传递为当前分区的长度，以确保 solve_expressions_recursive 尝试用完所有数字
        current_solutions_count_before = len(solutions_set)
        solve_expressions_recursive(0, 0, " ", num_list_partition, aim_number_global, len(num_list_partition))
        if len(solutions_set) > current_solutions_count_before:
            found_solution = True

    if not found_solution:
        print(f"在最大操作数为 {max_ops_input} 的情况下，没有找到解。")

if __name__ == "__main__":
    main()

