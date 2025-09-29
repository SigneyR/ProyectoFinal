import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

# Librerías externas necesarias para leer Word y PDF
from docx import Document
import PyPDF2

def abrir_explorador():
    # Abrir un cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[
            ("Archivos de texto", "*.txt;*.py;*.md;*.csv"),
            ("Archivos Word", "*.docx"),
            ("Archivos PDF", "*.pdf"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:  # Si el usuario seleccionó un archivo
        extension = os.path.splitext(archivo)[1].lower()  # Obtener extensión del archivo
        contenido = ""  # Variable donde se guarda el texto a mostrar

        try:
            # Lectura de archivos de texto (son editables)
            if extension in [".txt", ".py", ".md", ".csv"]:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
            
            # Lectura de archivos Word (solo lectura)
            elif extension == ".docx":
                doc = Document(archivo)
                contenido = "\n".join([p.text for p in doc.paragraphs])

            # Lectura de archivos PDF (solo lectura)
            elif extension == ".pdf":
                with open(archivo, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        contenido += page.extract_text() + "\n"

            # Si el formato no está soportado
            else:
                contenido = "[Formato no soportado para vista previa]"

        except Exception as e:
            # Si ocurre un error al abrir el archivo, se muestra el error en pantalla
            contenido = f"[Error al abrir archivo: {e}]"

        # Crear una nueva ventana para mostrar el contenido
        editor = tk.Toplevel()
        editor.title(f"Explorador - {archivo}")
        editor.geometry("800x600")
        editor.configure(bg="#8A56B7")  # Fondo morado oscuro

        # Área de texto con scroll para visualizar el contenido
        text_area = scrolledtext.ScrolledText(
            editor, wrap="word", font=("Consolas", 11),
            bg="#EDE7F6", fg="black"  # Fondo lavanda, texto negro
        )
        text_area.insert("1.0", contenido)

        # Los archivos de texto son editables, los demás solo lectura
        text_area.config(
            state="normal" if extension in [".txt", ".py", ".md", ".csv"] else "disabled"
        )
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

        #Botón "Guardar" → solo disponible para archivos de texto
        if extension in [".txt", ".py", ".md", ".csv"]:
            def guardar():
                try:
                    # Guardar el contenido actual en el archivo
                    with open(archivo, "w", encoding="utf-8") as f:
                        f.write(text_area.get("1.0", tk.END))
                    
                    # Mostrar confirmación de guardado
                    messagebox.showinfo("Éxito", "Archivo guardado correctamente")
                    
                    #Cerrar automáticamente la ventana después de guardar
                    editor.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar: {e}")

            # Botón guardar en la ventana
            btn_guardar = tk.Button(
                editor, text="Guardar", command=guardar,
                bg="#3C2255", fg="white", font=("Arial", 11, "bold")
            )
            btn_guardar.pack(pady=5)
            

