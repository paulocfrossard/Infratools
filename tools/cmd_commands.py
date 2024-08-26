import subprocess


def command_exec(command, target, args, type):
    print('\n'+('-'*7)+'Iniciando'+('-'*7))
    full_command = f"{command} {target} {args}"
    print(f" {full_command}...")
    # 0 generic, 1 verbose, 2 simple
    if type == 0:
        print(f"Type {type}")
        status = subprocess.run(full_command, shell=True)
    elif type == 1:
        print(f"Type {type}")
        status = subprocess.run(full_command, shell=True, capture_output=True, text=True, check=True)
    else:
        print(f"Type {type}")
        status = subprocess.run(command, shell=True)
    print('\n'+('-'*7)+'Finalizado'+('-'*7))
    return status
