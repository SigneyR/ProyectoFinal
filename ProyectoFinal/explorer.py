import tkinter as tk
from tkinter import filedialog, scrolledtext
from styles import BUTTON_STYLE, TERMINAL_STYLE

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
        win.geometry("800x500")


        texto = scrolledtext.ScrolledText(win, wrap=tk.WORD, width=80, height=20, **TERMINAL_STYLE,font=("Consolas", 12))
        texto.insert(tk.END, contenido)
        texto.pack(expand=True, fill="both", padx=10, pady=10)

        # Guardar cambios
        def guardar():
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(texto.get("1.0", tk.END))
        
        btn_guardar = tk.Button(win, text="Guardar", command=guardar,**BUTTON_STYLE,font=("Consolas", 12, "bold"), padx=15,pady=5)
        btn_guardar.pack(pady=10)

        win.mainloop()
