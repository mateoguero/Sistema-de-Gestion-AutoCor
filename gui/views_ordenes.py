import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_vehiculos, obtener_mecanicos, obtener_repuestos, crear_orden_trabajo
from utils.validators import validar_monto

class OrdenesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.repuestos_usados = []
        self.mecanicos_dict = {}
        self.vehiculos_dict = {}
        self.repuestos_dict = {}
        self.create_widgets()
        self.cargar_combos()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Órdenes de Trabajo N° 101", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=10)

        # Datos Principales de la Orden
        frame_cab = tk.LabelFrame(self, text="Datos Principales de la Orden", font=("Arial", 9), bg="#dcdcdc", padx=10, pady=8)
        frame_cab.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_cab, text="Fecha Ingreso:", bg="#dcdcdc").grid(row=0, column=0, sticky="e", padx=5)
        self.ent_fecha = tk.Entry(frame_cab, width=15)
        self.ent_fecha.insert(0, "19/09/2026")
        self.ent_fecha.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        tk.Label(frame_cab, text="Vehículo (Patente):", bg="#dcdcdc").grid(row=0, column=2, sticky="e", padx=5)
        self.cmb_vehiculo = ttk.Combobox(frame_cab, width=32)
        self.cmb_vehiculo.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(frame_cab, text="Mecánico Resp.:", bg="#dcdcdc").grid(row=1, column=0, sticky="e", padx=5)
        self.cmb_mecanico = ttk.Combobox(frame_cab, width=28)
        self.cmb_mecanico.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(frame_cab, text="Estado Orden:", bg="#dcdcdc").grid(row=1, column=2, sticky="e", padx=5)
        self.cmb_estado = ttk.Combobox(frame_cab, values=["Pendiente", "En Reparación", "Finalizada"], width=20)
        self.cmb_estado.set("En Reparación")
        self.cmb_estado.grid(row=1, column=3, padx=5, pady=4, sticky="w")

        tk.Label(frame_cab, text="Descripción Servicio:", bg="#dcdcdc").grid(row=2, column=0, sticky="e", padx=5)
        self.ent_servicio = tk.Entry(frame_cab, width=32)
        self.ent_servicio.insert(0, "Cambio de pastillas de freno delan")
        self.ent_servicio.grid(row=2, column=1, padx=5, pady=4, sticky="w")

        tk.Label(frame_cab, text="Mano de Obra ($):", bg="#dcdcdc").grid(row=2, column=2, sticky="e", padx=5)
        self.ent_mano_obra = tk.Entry(frame_cab, width=15)
        self.ent_mano_obra.insert(0, "15000.00")
        self.ent_mano_obra.grid(row=2, column=3, padx=5, pady=4, sticky="w")

        # Detalle de Repuestos Consumidos
        frame_rep = tk.LabelFrame(self, text="Detalle de Repuestos Consumidos", font=("Arial", 9), bg="#dcdcdc", padx=10, pady=8)
        frame_rep.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_rep, text="Seleccionar Repuesto:", bg="#dcdcdc").grid(row=0, column=0, sticky="w")
        self.cmb_repuesto = ttk.Combobox(frame_rep, width=32)
        self.cmb_repuesto.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(frame_rep, text="Cant:", bg="#dcdcdc").grid(row=0, column=2, sticky="w")
        self.spn_cantidad = tk.Spinbox(frame_rep, from_=1, to=50, width=5)
        self.spn_cantidad.grid(row=0, column=3, padx=5, pady=4)

        btn_agregar = tk.Button(frame_rep, text="+ Agregar a la Orden", bg="#e1e1e1", relief="groove", command=self.agregar_repuesto)
        btn_agregar.grid(row=0, column=4, padx=10)

        # Tabla Repuestos Usados (usando .grid para no entrar en conflicto con el resto de frame_rep)
        self.tree = ttk.Treeview(frame_rep, columns=("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"), show="headings", height=4)
        for col in ("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"):
            self.tree.heading(col, text=col)
        self.tree.column("Código", width=100)
        self.tree.column("Descripción Repuesto", width=250)
        self.tree.column("Cantidad", width=80, anchor="center")
        self.tree.column("Precio Aplicado", width=120)

        self.tree.grid(row=1, column=0, columnspan=5, sticky="ew", pady=8)
        frame_rep.grid_columnconfigure(1, weight=1)

        # Muestra visual igual al boceto
        self.tree.insert("", "end", values=("R001", "Pastillas de freno delanteras", "2", "$ 45000.00"))

        # Resumen y Totales
        self.lbl_totales = tk.Label(
            self, text="Mano de Obra: $15.000,00  +  Subtotal Repuestos: $90.000,00  =  TOTAL: $105.000,00", 
            font=("Arial", 11, "bold"), fg="#0066cc", bg="#dcdcdc"
        )
        self.lbl_totales.pack(anchor="e", padx=25, pady=10)

        # Botones Inferiores
        frame_acc = tk.Frame(self, bg="#dcdcdc")
        frame_acc.pack(anchor="w", padx=20, pady=5)

        btn_guardar = tk.Button(frame_acc, text="Guardar Orden de Trabajo", bg="#e1e1e1", relief="groove", padx=10, command=self.guardar_orden)
        btn_guardar.pack(side="left", padx=5)

        btn_imprimir = tk.Button(frame_acc, text="Imprimir Comprobante de Cobro", bg="#e1e1e1", relief="groove", padx=10)
        btn_imprimir.pack(side="left", padx=5)

    def cargar_combos(self):
        self.cmb_vehiculo['values'] = ["AB123CD - Gol Trend (Carlos Gómez)"]
        self.cmb_vehiculo.set("AB123CD - Gol Trend (Carlos Gómez)")

        self.cmb_mecanico['values'] = ["Juan Pérez (Frenos y Motor)"]
        self.cmb_mecanico.set("Juan Pérez (Frenos y Motor)")

        self.cmb_repuesto['values'] = ["R001 - Pastillas de freno ($45000)"]
        self.cmb_repuesto.set("R001 - Pastillas de freno ($45000)")

    def agregar_repuesto(self):
        pass

    def guardar_orden(self):
        messagebox.showinfo("Éxito", "Orden de Trabajo guardada correctamente")