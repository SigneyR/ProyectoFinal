import subprocess

def ejecutar_comando(comando):
    try:
        resultado = subprocess.check_output(
            comando, shell=True, text=True, stderr=subprocess.STDOUT
        )
        return resultado
    except subprocess.CalledProcessError as e:
        return f"Error:\n{e.output}"
