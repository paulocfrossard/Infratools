import os
import subprocess


def os_recovery():
    def generic_command(command):
        print("Iniciando " + command + "...")
        status = subprocess.call(command, shell=True)
        return status

    sfc = generic_command("sfc /scannow ")
    chkdsk = generic_command("echo s | chkdsk C: /f")
    generic_command("cls")
    return sfc, chkdsk
