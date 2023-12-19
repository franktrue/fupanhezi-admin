# 用户标识转UserID
def identifierToUserId(s):
    num = int(s)
    return str(int((num-10000)/9))