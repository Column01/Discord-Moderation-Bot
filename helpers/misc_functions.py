import re


# Check if the string is a number
def is_number(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


# Check if the duration is a positive number
def is_valid_duration(duration):
    if is_number(duration):
        if int(duration) > 0:
            return True
        else:
            return False
    else:
        return False
    

# Parses a duration in seconds from a string that looks like: 1w3d10h30m20s
def parse_duration(s):
    if is_number(s):
        return int(s)
    ret = list(map(int, re.split('[wdhms]', s)[:-1]))
    if len(ret) == 5:
        return ret[0] * 604800 + ret[1] * 86400 + ret[2] * 3600 + ret[3] * 60 + ret[4]
    if len(ret) == 4:
        return ret[0] * 86400 + ret[1] * 3600 + ret[2] * 60 + ret[3]
    if len(ret) == 3:
        return ret[0] * 3600 + ret[1] * 60 + ret[2]
    elif len(ret) == 2:
        return ret[0] * 60 + ret[1]
    else:
        return ret[0]