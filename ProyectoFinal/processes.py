import psutil
import tkinter as tk
from tkinter import ttk, messagebox
from styles import BUTTON_STYLE

def abrir_administrador():
    win = tk.Toplevel()
    win.title("Administrador de Tareas")
    win.geometry("700x400")

    # 🎨 Estilo para la tabla
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background="#f5f5dc",
        foreground="black",
        rowheight=25,
        fieldbackground="#f5f5dc",
        font=("Consolas", 11)
    )
    style.configure("Treeview.Heading", font=("Consolas", 12, "bold"), background="black", foreground="white")
    style.map("Treeview", background=[("selected", "#c0c0c0")])
   
      #Tabla de procesos
    cols = ("PID", "Nombre", "Uso CPU (%)", "Memoria (MB)")
    tabla = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, width=150, anchor="center")
    tabla.pack(expand=True, fill="both", side=tk.LEFT)

    # Scroll vertical
    scroll = ttk.Scrollbar(win, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    #Funciones
    def cargar_procesos():
        for row in tabla.get_children():
            tabla.delete(row)
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                    cpu = proc.cpu_percent(interval=0.1) 
                    memoria = round(proc.info['memory_info'].rss / 1024 / 1024, 2)
                    tabla.insert("", tk.END, values=(proc.info['pid'], proc.info['name'], cpu, memoria))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Programar actualización automática cada segundo       
        win.after(1000, cargar_procesos)


    def finalizar_proceso():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un proceso para finalizar.")
            return
        pid = tabla.item(seleccionado[0])['values'][0]
        try:
            psutil.Process(pid).terminate()
            messagebox.showinfo("Éxito", f"Proceso {pid} terminado.")
            cargar_procesos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    #Botones
    
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=5)

    btn_refrescar = tk.Button(btn_frame, text="Refrescar", command=cargar_procesos, **BUTTON_STYLE)
    btn_refrescar.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

    btn_finalizar = tk.Button(btn_frame, text="Finalizar Proceso", command=finalizar_proceso, **BUTTON_STYLE)
    btn_finalizar.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

    cargar_procesos()
