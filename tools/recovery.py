import os
import subprocess


def os_recovery():
    def generic_command(command):
        print("Iniciando " + command + "...")
        status = subprocess.call(command, shell=True)
        return status

    a = generic_command("sfc /scannow ")
    b = generic_command("echo yes | chkdsk C: /f")
    generic_command("cls")
    print(a, b)