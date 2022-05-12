import uuid

def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")
    return code



"""



Create the referral function here
"""





def getSimplifiedNumber(num):
    if num < 1000:
        return num
    elif num < 1000000:
        num = num / 1000
        num = round(num, 1)
        return f"{num}k"
    elif num < 1000000000:
        num = num / 1000000
        num = round(num, 1)
        return f"{num}M"
    elif num < 1000000000000:
        num = num / 1000000000
        num = round(num, 1)
        return f"{num}B"
    return num




