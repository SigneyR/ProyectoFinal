import tkinter as tk
from tkinter import ttk
from terminal import ejecutar_comando
from explorer import abrir_explorador
from processes import abrir_administrador

from styles import TERMINAL_STYLE, ENTRY_STYLE, BUTTON_STYLE


def main():
    root = tk.Tk()
    root.title("Mini SO en Python")
    root.geometry("900x650")

     # 🎨 Estilos de Notebook (barra de pestañas)
    style = ttk.Style()
    style.theme_use("default")

    style.configure("TNotebook.Tab",
                    background="black",
                    foreground="#f5f5dc",
                    padding=[10, 5])

    style.map("TNotebook.Tab",
              background=[("selected", "#f5f5dc")],   # pestaña activa → Beige
              foreground=[("selected", "black")])     # texto de pestaña activa → negro

    # Contenedor de pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # ---------------------------
    # Terminal
    # ---------------------------
    terminal_frame = ttk.Frame(notebook)
    notebook.add(terminal_frame, text="Terminal") #creamos la pestaña de Terminal

    entrada = tk.Entry(terminal_frame, width=80,**ENTRY_STYLE) #campo de texto, para escribir el comando
    entrada.pack(pady=5)
    # Ejecutar comando con la tecla Enter
    entrada.bind("<Return>", lambda event: run_comando())


    salida = tk.Text(terminal_frame, wrap=tk.WORD, height=25, width=100,**TERMINAL_STYLE) #resultado de los comandos que se ejecutan
    salida.pack(expand=True, fill="both")

    def run_comando(): #funcion que ejecuta los comandos
        comando = entrada.get()
        if comando.strip().lower() == "clear":  # comando para limpiar pantalla
            salida.delete("1.0", tk.END)
            entrada.delete(0, tk.END)
            return
        resultado = ejecutar_comando(comando) #funcion importada terminal.py que se encarga de correr los comandos
        salida.insert(tk.END, f"> {comando}\n{resultado}\n")
        salida.see(tk.END)
        entrada.delete(0, tk.END)
    
    
    boton_frame = tk.Frame(terminal_frame, bg="#f5f5dc")
    boton_frame.pack(pady=5)
    boton = tk.Button(boton_frame, text="Ejecutar", command=run_comando,**BUTTON_STYLE) #botón para ejecutar
    boton.pack()

    # ---------------------------
    # Explorador / Editor
    # ---------------------------
    explorer_frame = tk.Frame(notebook, bg="#f5f5dc")
    notebook.add(explorer_frame, text="Explorador")

    label = tk.Label(explorer_frame, text="Abrir y editar archivos desde aquí",bg="#f5f5dc", fg="black", font=("Arial", 12, "bold"))
    label.pack(pady=10)

    btn_explorer = tk.Button(
        explorer_frame,
        text="Abrir archivo",
        command=abrir_explorador,
         **BUTTON_STYLE 
    )
    btn_explorer.pack(pady=15)

    # ---------------------------
    # Administrador de Tareas
    # ---------------------------
    process_frame = tk.Frame(notebook, bg="#f5f5dc")
    notebook.add(process_frame, text="Administrador de Tareas")

    label_proc = tk.Label(process_frame, text="Ver y administrar procesos del sistema",bg="#f5f5dc", fg="black", font=("Arial", 12, "bold"))
    label_proc.pack(pady=10)

    btn_process = tk.Button(
        process_frame,
        text="Abrir Administrador",
        command=abrir_administrador,
         **BUTTON_STYLE 
    )
    btn_process.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
