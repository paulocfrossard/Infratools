import subprocess


def command_generic(command, target, args):
    print(f"Iniciando {command}...")
    full_command = f"{command} {target} {args}"
    status = subprocess.call(full_command, shell=True)
    return status


def command_output(command, target, args):
    print("Iniciando " + command + "...")
    full_command = f"{command} {target} {args}"
    status = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True)
    return status
