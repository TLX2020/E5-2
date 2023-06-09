# 定义一个函数，将十六进制字符串转换为十进制数
def hex_to_dec(hex_str):
    # 创建一个字典，存储十六进制数字和对应的十进制值
    hex_dict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                "8": 8, "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    # 初始化一个变量，存储结果
    dec_num = 0
    # 遍历十六进制字符串，从右往左
    for i in range(len(hex_str)):
        # 获取当前位的字符
        char = hex_str[-(i+1)]
        # 判断字符是否在字典中，如果不在，返回错误信息
        if char not in hex_dict:
            return "Invalid hexadecimal number"
        # 否则，将字符对应的十进制值乘以16的i次方，并累加到结果中
        else:
            dec_num += hex_dict[char] * (16 ** i)
    # 返回结果
    return dec_num


# 定义一个函数，将十进制数转换为十六进制字符串
def dec_to_hex(dec_num):
    # 创建一个字典，存储十进制值和对应的十六进制数字
    dec_dict = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
    # 初始化一个空字符串，存储结果
    hex_str = ""
    # 判断十进制数是否为零，如果是，返回"0"
    if dec_num == 0:
        return "0"
    # 否则，循环除以16，直到商为零
    while dec_num > 0:
        # 获取余数，并将其对应的十六进制数字添加到结果字符串的开头
        rem = dec_num % 16
        hex_str = dec_dict[rem] + hex_str
        # 更新商为下一次循环的被除数
        dec_num = dec_num // 16
    # 返回结果
    return hex_str


# 定义一个函数，实现两个十六进制数的加法
def hex_add(hex_a, hex_b):
    # 将两个十六进制数转换为十进制数
    dec_a = hex_to_dec(hex_a)
    dec_b = hex_to_dec(hex_b)

    # 如果转换出错，返回错误信息
    if isinstance(dec_a, str) or isinstance(dec_b, str):
        return f"Cannot add {hex_a} and {hex_b}"
    # 否则，将两个十进制数相加，并将结果转换为十六进制字符串
    else:
        dec_sum = dec_a + dec_b
        hex_sum = dec_to_hex(dec_sum)
        # 返回结果
        return hex_sum


# 定义一个函数，实现两个十六进制数的减法
def hex_sub(hex_a, hex_b):
    # 将两个十六进制数转换为十进制数
    dec_a = hex_to_dec(hex_a)
    dec_b = hex_to_dec(hex_b)
    # 如果转换出错，返回错误信息
    if isinstance(dec_a, str) or isinstance(dec_b, str):
        return f"Cannot subtract {hex_b} from {hex_a}"
    # 否则，将两个十进制数相减，并将结果转换为十六进制字符串
    else:
        dec_diff = dec_a - dec_b
        hex_diff = dec_to_hex(dec_diff)
        # 返回结果
        return hex_diff


# 定义一个函数，实现两个十六进制数的乘法
def hex_mul(hex_a, hex_b):
    # 将两个十六进制数转换为十进制数
    dec_a = hex_to_dec(hex_a)
    dec_b = hex_to_dec(hex_b)
    # 如果转换出错，返回错误信息
    if isinstance(dec_a, str) or isinstance(dec_b, str):
        return f"Cannot multiply {hex_a} and {hex_b}"
    # 否则，将两个十进制数相乘，并将结果转换为十六进制字符串
    else:
        dec_prod = dec_a * dec_b
        hex_prod = dec_to_hex(dec_prod)
        # 返回结果
        return hex_prod


# 定义一个函数，实现两个十六进制数的除法（只保留整数部分）
def hex_div(hex_a, hex_b):
    # 将两个十六进制数转换为十进制数
    dec_a = hex_to_dec(hex_a)
    dec_b = hex_to_dec(hex_b)
    # 如果转换出错，返回错误信息
    if isinstance(dec_a, str) or isinstance(dec_b, str):
        return f"Cannot divide {hex_a} by {hex_b}"
    # 如果除数为零，返回错误信息
    elif dec_b == 0:
        return f"Cannot divide by zero"
    # 否则，将两个十进制数相除，并将商（只保留整数部分）转换为十六进制字符串
    else:
        dec_quot = dec_a // dec_b
        hex_quot = dec_to_hex(dec_quot)
        # 返回结果
        return hex_quot


# 定义一个主函数，用于接收用户输入和输出结果
def main():
    # 打印欢迎信息和使用说明
    print("欢迎使用十六进制计算器！")
    print("请输入两个有效的十六进制数字和运算符，中间用空格隔开。")
    print("例如：A1B2 + C3D4")
    print("输入Q或q退出程序。")
    print()

    # 创建一个无限循环，直到用户输入Q或q退出程序
    while True:
        # 获取用户输入，并去除首尾空格并转换为大写字母（方便处理）
        user_input = input("请输入：").strip().upper()

        # 如果用户输入Q或q，退出程序并打印感谢信息
        if user_input == 'Q':
            print("感谢使用十六进制计算器！再见！")
            break
        else:
            # 尝试分割用户输入为三个部分：第一个数字、运算符、第二个数字，并去除各自的首尾空格（方便处理）
            try:
                num1, op, num2 = user_input.split()
                num1 = num1.strip()
                op = op.strip()
                num2 = num2.strip()
                # 根据运算符调用相应的函数，并打印结果（如果有）
                if op == '+':
                    result = hex_add(num1, num2)
                    print(f"{num1} + {num2} = {result}")
                elif op == '-':
                    result = hex_sub(num1, num2)
                    print(f"{num1} - {num2} = {result}")
                elif op == '*':
                    result = hex_mul(num1, num2)
                    print(f"{num1} * {num2} = {result}")
                elif op == '/':
                    result = hex_div(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                else:
                    print("无效的运算符，请输入+ - * /之一。")
            except ValueError:
                print("无效的输入，请按照格式输入。")
            print()

# 调用主函数
main()

# 定义一个函数，将十六进制字符串转换为十进制数
def hex_to_dec(hex_str):
    # 创建一个字典，存储十六进制数字和对应的十进制值
    hex_dict = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
                "8": 8, "9": 9, "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
    # 初始化一个变量，存储结果
    dec_num = 0
    # 遍历十六进制字符串，从右往左
    for i in range(len(hex_str)):
        # 获取当前位的字符
        char = hex_str[-(i+1)]
        # 判断字符是否在字典中，如果不在，返回错误信息
        if char not in hex_dict:
            return "Invalid hexadecimal number"
        # 否则，将字符对应的十进制值乘以16的i次方，并累加到结果中
        else:
            dec_num += hex_dict[char] * (16 ** i)
    # 返回结果
    return dec_num


# 定义一个函数，将十进制数转换为十六进制字符串
def dec_to_hex(dec_num):
    # 创建一个字典，存储十进制值和对应的十六进制数字
    dec_dict = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
                8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
    # 初始化一个空字符串，存储结果
    hex_str = ""
    # 判断十进制数是否为零，如果是，返回"0"
    if dec_num == 0:
        return "0"
    # 否则，循环除以16，直到商为零
    while dec_num > 0:
        # 获取余数，并将其对应的十六进制数字添加到结果字符串的开头
        rem = dec_num % 16
        hex_str = dec_dict[rem] + hex_str
        # 更新商为下一次循环的被除数
        dec_num = dec_num // 16
    # 返回结果
    return hex_str


# 定义一个函数，实现两个十六进制数的加法
def hex_add(hex_a, hex_b):
    # 将两个十六进制数转换为十进制数
    dec_a = hex_to_dec(hex_a)
    dec_b = hex_to_dec(hex_b)

    # 如果转换出错，返回错误信息
    if isinstance(dec_a, str) or isinstance(dec_b, str):
        return f"Cannot add {hex_a} and {hex_b}"