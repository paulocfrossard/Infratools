import re

from tools.cmd_commands import command_exec
from tools.formart import return_format


def os_recovery():
    sfc = command_exec("sfc", "", "/scannow", 0)
    chkdsk = command_exec("echo s | chkdsk C: /f", "", "", 2)
    dism_check = command_exec("dism", "", "/online /cleanup-image /CheckHealth", 1)
    dism_restore = command_exec("dism", "", "/online /cleanup-image /restorehealth", 1)
    chkdsk = return_format(chkdsk)
    sfc = return_format(sfc)
    dism_check = return_format(dism_check)
    dism_restore = return_format(dism_restore)
    return [0], [3], [0], [0]
