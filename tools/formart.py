import re


def return_format(data):
    data = str(data)
    return_code = re.findall(r'returncode=(\d+)', data)
    return return_code
