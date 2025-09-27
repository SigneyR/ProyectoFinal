import tkinter as tk
from tkinter import filedialog, messagebox

def abrir_editor(archivo=None):
    def abrir_archivo():
        nonlocal archivo
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")]
        )
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                texto.delete(1.0, tk.END)
                texto.insert(tk.END, f.read())
            ventana.title(f"Editor - {archivo}")

    def guardar_archivo():
        nonlocal archivo
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto.get(1.0, tk.END))
            messagebox.showinfo("Guardar", "Archivo guardado con éxito ✅")
        else:
            guardar_como()

    def guardar_como():
        nonlocal archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")]
        )
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto.get(1.0, tk.END))
            ventana.title(f"Editor - {archivo}")
            messagebox.showinfo("Guardar", "Archivo guardado con éxito ✅")

    ventana = tk.Toplevel()
    ventana.title("Editor de Archivos")

    # Área de texto
    texto = tk.Text(ventana, wrap="word")
    texto.pack(expand=True, fill="both")

    # Si se abre desde el administrador con un archivo
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            texto.insert(tk.END, f.read())
        ventana.title(f"Editor - {archivo}")

    # Menú superior
    menu = tk.Menu(ventana)
    ventana.config(menu=menu)

    archivo_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Archivo", menu=archivo_menu)
    archivo_menu.add_command(label="Abrir", command=abrir_archivo)
    archivo_menu.add_command(label="Guardar", command=guardar_archivo)
    archivo_menu.add_command(label="Guardar como", command=guardar_como)
    archivo_menu.add_separator()
    archivo_menu.add_command(label="Salir", command=ventana.destroy)
