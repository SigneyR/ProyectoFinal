import psutil
import tkinter as tk
from tkinter import ttk, messagebox

def abrir_administrador():
    win = tk.Toplevel()
    win.title("Administrador de Tareas")
    win.geometry("700x400")

    cols = ("PID", "Nombre", "Uso CPU (%)", "Memoria (MB)")
    tabla = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(expand=True, fill="both")

    def cargar_procesos():
        for row in tabla.get_children():
            tabla.delete(row)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                tabla.insert("", tk.END, values=(
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['cpu_percent'],
                    round(proc.info['memory_info'].rss / 1024 / 1024, 2)
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

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

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=5)

    btn_refrescar = tk.Button(btn_frame, text="Refrescar", command=cargar_procesos)
    btn_refrescar.pack(side=tk.LEFT, padx=5)

    btn_finalizar = tk.Button(btn_frame, text="Finalizar Proceso", command=finalizar_proceso)
    btn_finalizar.pack(side=tk.LEFT, padx=5)

    cargar_procesos()
