import subprocess

from tools.cmd_commands import command_exec
from tools.formart import return_format


def ping_tools(ips, dominio):
    ip_status = []
    for ip in ips:
        status = command_exec("ping", ip, "-n 10", 0)
        satus_new = return_format(status)
        status = [satus_new, ip]
        ip_status.append(status)
    dominio_status = command_exec("ping", dominio, "-n 10", 0)
    return ip_status, dominio_status


def ip_refresh():
    ip_release = command_exec("ipconfig", "", "/release", 0)
    ip_renew = command_exec("ipconfig", "", "/renew", 0)
