import socket
import re
import uuid


def get_network_devices():
    ip = socket.gethostbyname(socket.gethostname())
    mac = str(':'.join(re.findall('..', '%012x' % uuid.getnode())))
    return ip, mac
