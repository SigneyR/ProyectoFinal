import tkinter as tk
from tkinter import ttk
from terminal import ejecutar_comando
from explorer import abrir_explorador
from processes import abrir_administrador


def main():
    root = tk.Tk()
    root.title("Mini SO en Python")
    root.geometry("900x650")

    # Contenedor de pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # ---------------------------
    # Terminal
    # ---------------------------
    terminal_frame = ttk.Frame(notebook)
    notebook.add(terminal_frame, text="Terminal")

    entrada = tk.Entry(terminal_frame, width=80)
    entrada.pack(pady=5)

    salida = tk.Text(terminal_frame, wrap=tk.WORD, height=25, width=100)
    salida.pack(expand=True, fill="both")

    def run_comando():
        comando = entrada.get()
        if comando.strip().lower() == "clear":  # comando para limpiar pantalla
            salida.delete("1.0", tk.END)
            entrada.delete(0, tk.END)
            return
        resultado = ejecutar_comando(comando)
        salida.insert(tk.END, f"> {comando}\n{resultado}\n")
        salida.see(tk.END)
        entrada.delete(0, tk.END)

    boton = tk.Button(terminal_frame, text="Ejecutar", command=run_comando)
    boton.pack(pady=5)

    # ---------------------------
    # Explorador / Editor
    # ---------------------------
    explorer_frame = ttk.Frame(notebook)
    notebook.add(explorer_frame, text="Explorador")

    label = tk.Label(explorer_frame, text="Abrir y editar archivos desde aquí")
    label.pack(pady=10)

    btn_explorer = tk.Button(
        explorer_frame,
        text="Abrir archivo",
        command=abrir_explorador
    )
    btn_explorer.pack(pady=20)

    # ---------------------------
    # Administrador de Tareas
    # ---------------------------
    process_frame = ttk.Frame(notebook)
    notebook.add(process_frame, text="Administrador de Tareas")

    label_proc = tk.Label(process_frame, text="Ver y administrar procesos del sistema")
    label_proc.pack(pady=10)

    btn_process = tk.Button(
        process_frame,
        text="Abrir Administrador",
        command=abrir_administrador
    )
    btn_process.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
