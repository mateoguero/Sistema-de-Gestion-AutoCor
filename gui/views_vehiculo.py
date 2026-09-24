import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_vehiculos, insertar_vehiculo, obtener_clientes
from utils.validators import validar_patente

class VehiculosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.clientes_dict = {}
        self.create_widgets()
        self.cargar_clientes_combo()
        self.cargar_tabla()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Vehículos", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=10)

        frame_form = tk.LabelFrame(self, text="Datos del Vehículo", font=("Arial", 10), bg="#dcdcdc", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Patente:", bg="#dcdcdc").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_patente = tk.Entry(frame_form, width=20)
        self.ent_patente.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Marca:", bg="#dcdcdc").grid(row=0, column=2, sticky="w", pady=4)
        self.ent_marca = tk.Entry(frame_form, width=25)
        self.ent_marca.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Modelo:", bg="#dcdcdc").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_modelo = tk.Entry(frame_form, width=20)
        self.ent_modelo.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_form, text="Año:", bg="#dcdcdc").grid(row=1, column=2, sticky="w", pady=4)
        self.ent_anio = tk.Entry(frame_form, width=15)
        self.ent_anio.grid(row=1, column=3, padx=5, pady=4)

        tk.Label(frame_form, text="Dueño (Cliente):", bg="#dcdcdc").grid(row=2, column=0, sticky="w", pady=4)
        self.cmb_dueno = ttk.Combobox(frame_form, state="readonly", width=35)
        self.cmb_dueno.grid(row=2, column=1, columnspan=2, padx=5, pady=4, sticky="w")

        frame_btn = tk.Frame(frame_form, bg="#dcdcdc")
        frame_btn.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

        btn_guardar = tk.Button(frame_btn, text="Guardar Vehículo", bg="#e1e1e1", relief="groove", padx=10, command=self.guardar)
        btn_guardar.pack(side="left", padx=5)

        btn_modificar = tk.Button(frame_btn, text="Modificar", bg="#e1e1e1", relief="groove", padx=10)
        btn_modificar.pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("Patente", "Marca", "Modelo", "Año", "Dueño"), show="headings")
        for col in ("Patente", "Marca", "Modelo", "Año", "Dueño"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def cargar_clientes_combo(self):
        clientes = obtener_clientes()
        self.clientes_dict = {f"{c['Nombre']} {c['Apellido']} ({c['Documento']})": c['Documento'] for c in clientes}
        self.cmb_dueno['values'] = list(self.clientes_dict.keys())

    def guardar(self):
        patente = self.ent_patente.get().strip()
        marca = self.ent_marca.get().strip()
        modelo = self.ent_modelo.get().strip()
        anio = self.ent_anio.get().strip()
        dueno_sel = self.cmb_dueno.get()

        if not validar_patente(patente):
            messagebox.showerror("Error", "Formato de patente inválido (ej: AB123CD o ABC123)")
            return
        if not (marca and modelo and anio and dueno_sel):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        doc_cliente = self.clientes_dict[dueno_sel]
        if insertar_vehiculo(patente, marca, modelo, anio, doc_cliente):
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente")
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo registrar el vehículo")

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for v in obtener_vehiculos():
            self.tree.insert("", "end", values=(v['Patente'], v['Marca'], v['Modelo'], v['Anio'], v['Dueno']))