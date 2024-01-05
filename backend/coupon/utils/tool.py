import secrets
import string

# 生成兑换码
def generate_exchange_code(length):
    # 定义兑换码的字符集，包括数字和大写字母
    characters = string.digits + string.ascii_uppercase
    # 使用 secrets 模块生成随机的 length 长度的兑换码
    exchange_code = ''.join(secrets.choice(characters) for _ in range(length))
    return exchange_code