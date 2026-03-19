import requests

def get_public_ip():
    r = requests.get('https://ifconfig.me')
    return r.text