import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_vehiculos, obtener_repuestos, crear_orden_trabajo
from utils.validators import validar_monto

class OrdenesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.repuestos_usados = []
        self.vehiculos_dict = {}
        self.repuestos_dict = {}
        self.create_widgets()
        self.cargar_combos()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Órdenes de Trabajo", font=("Arial", 14, "bold"), bg="#dcdcdc")
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
        self.ent_mecanico = tk.Entry(frame_cab, width=28)
        self.ent_mecanico.insert(0, "Juan Pérez")
        self.ent_mecanico.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        tk.Label(frame_cab, text="Estado Orden:", bg="#dcdcdc").grid(row=1, column=2, sticky="e", padx=5)
        self.cmb_estado = ttk.Combobox(frame_cab, values=["Pendiente", "En Reparación", "Finalizada"], width=20)
        self.cmb_estado.set("En Reparación")
        self.cmb_estado.grid(row=1, column=3, padx=5, pady=4, sticky="w")

        tk.Label(frame_cab, text="Descripción Servicio:", bg="#dcdcdc").grid(row=2, column=0, sticky="e", padx=5)
        self.ent_servicio = tk.Entry(frame_cab, width=32)
        self.ent_servicio.insert(0, "Cambio de pastillas de freno delanteras")
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

        # Tabla Repuestos Usados
        self.tree = ttk.Treeview(frame_rep, columns=("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"), show="headings", height=4)
        for col in ("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"):
            self.tree.heading(col, text=col)
        self.tree.column("Código", width=100)
        self.tree.column("Descripción Repuesto", width=250)
        self.tree.column("Cantidad", width=80, anchor="center")
        self.tree.column("Precio Aplicado", width=120)

        self.tree.grid(row=1, column=0, columnspan=5, sticky="ew", pady=8)
        frame_rep.grid_columnconfigure(1, weight=1)

        # Resumen y Totales
        self.lbl_totales = tk.Label(
            self, text="Mano de Obra: $15.000,00  +  Subtotal Repuestos: $0,00  =  TOTAL: $15.000,00", 
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
        vehiculos = obtener_vehiculos()
        self.vehiculos_dict = {}
        vehiculos_vals = []
        for v in vehiculos:
            dueno = f" ({v['Dueno']})" if v.get('Dueno') else ""
            desc = f"{v['Patente']} - {v['Marca']} {v['Modelo']}{dueno}"
            self.vehiculos_dict[desc] = v['Patente']
            vehiculos_vals.append(desc)
        if vehiculos_vals:
            self.cmb_vehiculo['values'] = vehiculos_vals
            self.cmb_vehiculo.set(vehiculos_vals[0])
        else:
            self.cmb_vehiculo['values'] = ["AB123CD - Gol Trend (Carlos Gómez)"]
            self.cmb_vehiculo.set("AB123CD - Gol Trend (Carlos Gómez)")

        repuestos = obtener_repuestos()
        self.repuestos_dict = {}
        repuestos_vals = []
        for r in repuestos:
            desc = f"{r['Codigo_Repuesto']} - {r['Nombre_Repuesto']} (${r['Precio']})"
            self.repuestos_dict[desc] = r
            repuestos_vals.append(desc)
        if repuestos_vals:
            self.cmb_repuesto['values'] = repuestos_vals
            self.cmb_repuesto.set(repuestos_vals[0])
        else:
            self.cmb_repuesto['values'] = ["R001 - Pastillas de freno ($45000)"]
            self.cmb_repuesto.set("R001 - Pastillas de freno ($45000)")

    def agregar_repuesto(self):
        repuesto_sel = self.cmb_repuesto.get()
        if not repuesto_sel:
            messagebox.showwarning("Atención", "Seleccione un repuesto.")
            return

        try:
            cantidad = int(self.spn_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0.")
            return

        r_data = self.repuestos_dict.get(repuesto_sel)
        if r_data:
            codigo = r_data["Codigo_Repuesto"]
            nombre = r_data["Nombre_Repuesto"]
            precio = float(r_data["Precio"])
        else:
            partes = repuesto_sel.split(" - ")
            codigo = partes[0].strip()
            nombre = partes[1].split(" ($")[0].strip() if len(partes) > 1 else codigo
            precio = 45000.0

        for r in self.repuestos_usados:
            if r["codigo"] == codigo:
                r["cantidad"] += cantidad
                break
        else:
            self.repuestos_usados.append({
                "codigo": codigo,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio_aplicado": precio
            })

        self.actualizar_tabla_repuestos()

    def actualizar_tabla_repuestos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        subtotal_repuestos = 0.0
        for r in self.repuestos_usados:
            subt = r["cantidad"] * r["precio_aplicado"]
            subtotal_repuestos += subt
            self.tree.insert("", "end", values=(
                r["codigo"], r["nombre"], str(r["cantidad"]), f"$ {subt:,.2f}"
            ))

        self.actualizar_totales(subtotal_repuestos)

    def actualizar_totales(self, subtotal_repuestos=None):
        if subtotal_repuestos is None:
            subtotal_repuestos = sum(r["cantidad"] * r["precio_aplicado"] for r in self.repuestos_usados)

        mano_obra_str = self.ent_mano_obra.get().strip()
        try:
            mano_obra = float(mano_obra_str.replace(",", ".")) if mano_obra_str else 0.0
        except ValueError:
            mano_obra = 0.0

        total = mano_obra + subtotal_repuestos
        self.lbl_totales.config(
            text=f"Mano de Obra: ${mano_obra:,.2f}  +  Subtotal Repuestos: ${subtotal_repuestos:,.2f}  =  TOTAL: ${total:,.2f}"
        )

    def guardar_orden(self):
        fecha = self.ent_fecha.get().strip()
        vehiculo_sel = self.cmb_vehiculo.get().strip()
        mecanico = self.ent_mecanico.get().strip()
        servicio = self.ent_servicio.get().strip()
        mano_obra_str = self.ent_mano_obra.get().strip()
        estado = self.cmb_estado.get().strip() or "En Reparación"

        patente = self.vehiculos_dict.get(vehiculo_sel)
        if not patente:
            patente = vehiculo_sel.split(" - ")[0].strip() if vehiculo_sel else ""

        if not patente:
            messagebox.showerror("Error", "Debe seleccionar o indicar la patente de un vehículo.")
            return

        if not servicio:
            messagebox.showerror("Error", "Debe ingresar una descripción del servicio.")
            return

        if not validar_monto(mano_obra_str):
            messagebox.showerror("Error", "El valor de Mano de Obra es inválido.")
            return

        mano_obra = float(mano_obra_str.replace(",", "."))

        exito = crear_orden_trabajo(
            fecha=fecha,
            observacion="",
            descripcion=servicio,
            mano_obra=mano_obra,
            patente=patente,
            mecanico=mecanico,
            repuestos_usados=self.repuestos_usados,
            estado=estado
        )

        if exito:
            messagebox.showinfo("Éxito", "Orden de Trabajo guardada correctamente en la base de datos.")
            self.limpiar()
        else:
            messagebox.showerror("Error", "No se pudo registrar la Orden de Trabajo en la base de datos.")

    def limpiar(self):
        self.ent_servicio.delete(0, tk.END)
        self.repuestos_usados.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.actualizar_totales(0.0)