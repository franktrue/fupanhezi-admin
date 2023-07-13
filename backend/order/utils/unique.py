import datetime
import random

# 生成订单号
def generate_order_number(n):
    current_time = datetime.datetime.now().strftime("%y%m%d%H%M%S")
    random_number = ''.join(random.choices('0123456789', k=n))
    order_number = current_time + random_number
    return order_number