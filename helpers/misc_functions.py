

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