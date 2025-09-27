import tkinter as tk
from tkinter import filedialog, scrolledtext

def abrir_explorador():
    # Ventana de selección de archivos
    root = tk.Tk()
    root.withdraw()  # Oculta ventana principal

    archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Ventana para mostrar el archivo
        win = tk.Toplevel()
        win.title(f"Editor - {archivo}")

        texto = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=80, height=20)
        texto.insert(tk.END, contenido)
        texto.pack(expand=True, fill="both")

        # Guardar cambios
        def guardar():
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto.get("1.0", tk.END))
        
        btn_guardar = tk.Button(win, text="Guardar", command=guardar)
        btn_guardar.pack(pady=5)

        win.mainloop()

