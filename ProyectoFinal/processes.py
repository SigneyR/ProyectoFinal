import psutil
import tkinter as tk
from tkinter import ttk, messagebox

def abrir_administrador():
    win = tk.Toplevel()
    win.title("Administrador de Tareas")
    win.geometry("900x550")
    win.configure(bg="#1e1e1e")  # 🎨 Fondo oscuro para toda la ventana

    # === Estilos generales ===
    fuente = ("Times New Roman", 11)

    style = ttk.Style()
    style.theme_use("clam")  # Tema que respeta colores personalizados

    # Labels y textos
    style.configure("TLabel", background="#1e1e1e", foreground="white", font=fuente)

    # Botones
    style.configure("TButton", font=("Times New Roman", 11, "bold"), padding=6)

    # Progressbar
    style.configure("TProgressbar", troughcolor="#2c2c2c", background="#4caf50", thickness=15)

    # Tabla Treeview
    style.configure("Treeview",
                    background="#2c2c2c",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#2c2c2c",
                    font=fuente)
    style.configure("Treeview.Heading",
                    background="#444",
                    foreground="white",
                    font=("Times New Roman", 12, "bold"))
    style.map("Treeview",
              background=[("selected", "#005f73")],
              foreground=[("selected", "white")])

    # === Resumen superior (CPU y Memoria) ===
    frame_top = ttk.Frame(win, padding=10)
    frame_top.pack(fill="x")

    lbl_cpu = ttk.Label(frame_top, text="CPU: --%")
    lbl_cpu.grid(row=0, column=0, sticky="w")
    bar_cpu = ttk.Progressbar(frame_top, length=200, maximum=100, style="TProgressbar")
    bar_cpu.grid(row=0, column=1, padx=10)

    lbl_mem = ttk.Label(frame_top, text="Memoria: -- MB")
    lbl_mem.grid(row=0, column=2, padx=(20,5), sticky="w")
    bar_mem = ttk.Progressbar(frame_top, length=200, maximum=100, style="TProgressbar")
    bar_mem.grid(row=0, column=3, padx=10)

    # === Tabla de procesos ===
    cols = ("PID", "Nombre", "Uso CPU (%)", "Memoria (MB)")
    tabla = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tabla.heading(col, text=col, command=lambda c=col: ordenar(c))
        tabla.column(col, width=150, anchor="center")
    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    # Scrollbar
    vsb = ttk.Scrollbar(tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=vsb.set)
    vsb.pack(side="right", fill="y")

    # === Botones ===
    btn_frame = tk.Frame(win, bg="#1e1e1e")
    btn_frame.pack(pady=5)

    btn_refrescar = ttk.Button(btn_frame, text="🔄 Refrescar", command=lambda: cargar_procesos())
    btn_refrescar.pack(side=tk.LEFT, padx=5)

    btn_finalizar = ttk.Button(btn_frame, text="❌ Finalizar Proceso", command=lambda: finalizar_proceso())
    btn_finalizar.pack(side=tk.LEFT, padx=5)

    # === Funciones internas ===
    procesos = []
    sort_col = "Uso CPU (%)"
    sort_reverse = True

    def cargar_procesos():
        nonlocal procesos
        tabla.delete(*tabla.get_children())
        procesos = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                p = {
                    "PID": proc.info['pid'],
                    "Nombre": proc.info['name'],
                    "Uso CPU (%)": proc.info['cpu_percent'],
                    "Memoria (MB)": round(proc.info['memory_info'].rss / 1024 / 1024, 2)
                }
                procesos.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        mostrar_procesos()

        # Actualizar resumen del sistema
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        lbl_cpu.config(text=f"CPU: {cpu:.1f}%")
        bar_cpu["value"] = cpu
        lbl_mem.config(text=f"Memoria: {mem.used//1024//1024} / {mem.total//1024//1024} MB ({mem.percent}%)")
        bar_mem["value"] = mem.percent

    def mostrar_procesos():
        tabla.delete(*tabla.get_children())
        for p in sorted(procesos, key=lambda x: x[sort_col], reverse=sort_reverse):
            tags = []
            if p["Uso CPU (%)"] > 80:
                tags.append("very_high_cpu")
            elif p["Uso CPU (%)"] > 50:
                tags.append("high_cpu")
            if p["Memoria (MB)"] > 500:
                tags.append("high_mem")
            tabla.insert("", tk.END,
                         values=(p["PID"], p["Nombre"], p["Uso CPU (%)"], p["Memoria (MB)"]),
                         tags=tags)

    def ordenar(col):
        nonlocal sort_col, sort_reverse
        if sort_col == col:
            sort_reverse = not sort_reverse
        else:
            sort_col = col
            sort_reverse = True if col in ("Uso CPU (%)", "Memoria (MB)") else False
        mostrar_procesos()

    def finalizar_proceso():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un proceso para finalizar.")
            return
        pid = tabla.item(seleccionado[0])['values'][0]
        nombre = tabla.item(seleccionado[0])['values'][1]
        if not messagebox.askyesno("Confirmar", f"¿Finalizar el proceso {nombre} (PID {pid})?"):
            return
        try:
            psutil.Process(pid).terminate()
            messagebox.showinfo("Éxito", f"Proceso {pid} terminado.")
            cargar_procesos()
        except psutil.AccessDenied:
            messagebox.showerror("Error", "No tienes permisos para finalizar este proceso.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # === Tags de estilo (resaltado en la tabla) ===
    tabla.tag_configure("high_cpu", foreground="orange")
    tabla.tag_configure("very_high_cpu", foreground="red")
    tabla.tag_configure("high_mem", background="#402020")

    cargar_procesos()
