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
    

# Parses a duration in seconds from a string that looks like: 1w3d10h30m20s. 
# String can also have duplicate values for each type or just be a time in seconds value as an integer
def parse_duration(s):
    if is_number(s):
        return s
    else:
        values = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
        nums = []
        tempnums = []
        for char in s:
            if char.isdigit():
                tempnums.append(char)
            else:
                multiple = values.get(char)
                num = int("".join(tempnums))
                tempnums.clear()
                nums.append(num * multiple)
        return sum(nums)
