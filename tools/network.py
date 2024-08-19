import subprocess

from tools.cmd_commands import command_generic, command_output


def ping_tools(ips, dominio):
    ip_status = []
    for ip in ips:
        status = command_generic("ping", ip, "-n 10")
        status = [status, ip]
        ip_status.append(status)
    print(ip_status)
    dominio_status = command_generic("ping", dominio, "-n 4")
    return ip_status, dominio_status


def ip_refresh():
    ip_release = command_generic("ipconfig ", "", "/release")
    ip_renew = command_generic("ipconfig ", "", "/renew")


def tracert_interno():
    print('')