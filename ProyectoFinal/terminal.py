import subprocess #sirve para ejecutar comandos del sistema Operativo desde py
import time
import platform
import psutil

# Función para ejecutar comandos en el sistema o internos
def ejecutar_comando(comando: str) -> str:
    comando = comando.strip().lower()


    # Comandos internos personalizados

    if comando == "clear":
        return "[TERMINAL LIMPIADA]"

    elif comando == "help":
        return """ 
Comandos internos disponibles:
- clear : limpia la terminal
- help  : muestra este menú de ayuda
- info  : información del sistema

--------------------------------------

Comandos de Windows más comunes:
- dir          : lista archivos y carpetas
- cd [carpeta] : cambia de directorio
- mkdir [nom]  : crea una carpeta
- rmdir [nom]  : elimina una carpeta vacía
- del [nom]    : elimina un archivo
- copy origen destino : copia archivos
- move origen destino : mueve archivos
- ipconfig     : información de red
- ping [host]  : prueba de conexión
- tasklist     : lista procesos en ejecución
- exit         : cierra la terminal real (no esta)

Recuerda que estos son los principales, también puedes probar cualquier comando de CMD aquí.

"""
    elif comando == "info":
        return f"""ℹ️ Información del sistema:
        Sistema   : {platform.system()}
        Versión   : {platform.version()}
        Procesador: {platform.processor()}
        Núcleos   : {psutil.cpu_count(logical=True)}
        RAM Total : {round(psutil.virtual_memory().total / (1024**3), 2)} GB
        """
    
    # Comandos reales del sistema
    inicio = time.time()

    try:
        resultado = subprocess.check_output(
            comando, shell=True, #permite ejecutar comandos del intérprete cmd,
            text=True, #convierte la salida en texto (string), no en bytes.
            stderr=subprocess.STDOUT #si hay errores, los redirige a la misma salida, así también se ven en pantalla.
        )
        duracion = round(time.time() - inicio, 2)
         # Guardar en log
        with open("terminal.log", "a", encoding="utf-8") as log:
            log.write(f"COMANDO: {comando}\n{resultado}\n---\n")

        return f"{resultado}\n[⏱ Tiempo de ejecución: {duracion} seg]"

    except subprocess.CalledProcessError as e:
        return f"[❌ ERROR] Código {e.returncode}\n{e.output}"

    except FileNotFoundError:
        return "[❌ ERROR] Comando no encontrado"