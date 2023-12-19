# 用户标识转UserID
def identifierToUserId(s):
    num = int(s)
    d = (num-10000)/9
    if d.is_integer:
        return str(int(d))
    return None