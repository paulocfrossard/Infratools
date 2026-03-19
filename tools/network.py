import subprocess

from tools.cmd_commands import command_exec
from tools.formart import return_format


def internal_dns_status(ips):
    ip_status = []
    for ip in ips:
        status = command_exec("ping", ip, "-n 10", 0)
        satus_new = return_format(status)
        status = [satus_new, ip]
        ip_status.append(status)
    return ip_status

def internal_domain_status(domain):
    domain_status = command_exec("ping", domain, "-n 10", 0)
    domain_route = return_format(domain_status) # Fazer

def ip_refresh():
    ip_release = command_exec("ipconfig", "", "/release", 0)
    ip_renew = command_exec("ipconfig", "", "/renew", 0)
