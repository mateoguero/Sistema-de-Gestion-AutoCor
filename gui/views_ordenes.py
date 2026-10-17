import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import (
    obtener_vehiculos, obtener_repuestos, crear_orden_trabajo,
    obtener_ordenes_trabajo, eliminar_orden_trabajo, actualizar_estado_orden,
    obtener_repuestos_orden, actualizar_repuestos_orden
)
from utils.validators import validar_monto


class OrdenesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.repuestos_usados = []
        self.vehiculos_dict = {}
        self.repuestos_dict = {}
        self.create_widgets()
        self.cargar_combos()
        self.cargar_tabla_ordenes()


    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Órdenes de Trabajo", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=10)


        # Contenedor principal con pestañas o secciones para organizar (Crear / Listado)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=5)


        # --- PESTAÑA 1: NUEVA ORDEN ---
        self.tab_nueva = tk.Frame(self.notebook, bg="#dcdcdc")
        self.notebook.add(self.tab_nueva, text="Nueva Orden")


        # Datos Principales de la Orden
        frame_cab = tk.LabelFrame(self.tab_nueva, text="Datos Principales de la Orden", font=("Arial", 9), bg="#dcdcdc", padx=10, pady=8)
        frame_cab.pack(fill="x", padx=10, pady=5)


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
        self.cmb_estado = ttk.Combobox(frame_cab, values=["Pendiente", "En Reparación", "Finalizada", "Cancelada"], state="readonly", width=20)
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
        self.ent_mano_obra.bind("<KeyRelease>", lambda e: self.actualizar_totales())


        # Detalle de Repuestos Consumidos
        frame_rep = tk.LabelFrame(self.tab_nueva, text="Detalle de Repuestos Consumidos", font=("Arial", 9), bg="#dcdcdc", padx=10, pady=8)
        frame_rep.pack(fill="x", padx=10, pady=5)


        tk.Label(frame_rep, text="Seleccionar Repuesto:", bg="#dcdcdc").grid(row=0, column=0, sticky="w")
        self.cmb_repuesto = ttk.Combobox(frame_rep, width=32)
        self.cmb_repuesto.grid(row=0, column=1, padx=5, pady=4)


        tk.Label(frame_rep, text="Cant:", bg="#dcdcdc").grid(row=0, column=2, sticky="w")
        self.spn_cantidad = tk.Spinbox(frame_rep, from_=1, to=50, width=5)
        self.spn_cantidad.grid(row=0, column=3, padx=5, pady=4)


        btn_agregar = tk.Button(frame_rep, text="+ Agregar a la Orden", bg="#e1e1e1", relief="groove", command=self.agregar_repuesto)
        btn_agregar.grid(row=0, column=4, padx=10)


        # Tabla Repuestos Usados
        self.tree_repuestos = ttk.Treeview(frame_rep, columns=("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"), show="headings", height=3)
        for col in ("Código", "Descripción Repuesto", "Cantidad", "Precio Aplicado"):
            self.tree_repuestos.heading(col, text=col)
        self.tree_repuestos.column("Código", width=100)
        self.tree_repuestos.column("Descripción Repuesto", width=220)
        self.tree_repuestos.column("Cantidad", width=80, anchor="center")
        self.tree_repuestos.column("Precio Aplicado", width=100)
        self.tree_repuestos.grid(row=1, column=0, columnspan=5, sticky="ew", pady=8)
        frame_rep.grid_columnconfigure(1, weight=1)


        # Resumen y Totales
        self.lbl_totales = tk.Label(
            self.tab_nueva, text="Mano de Obra: $15.000,00 + Subtotal Repuestos: $0,00 = TOTAL: $15.000,00",
            font=("Arial", 10, "bold"), fg="#0066cc", bg="#dcdcdc"
        )
        self.lbl_totales.pack(anchor="e", padx=15, pady=5)


        # Botones Inferiores de la Solapa Nueva
        frame_acc = tk.Frame(self.tab_nueva, bg="#dcdcdc")
        frame_acc.pack(anchor="w", padx=10, pady=5)


        btn_guardar = tk.Button(frame_acc, text="Guardar Orden de Trabajo", bg="#e1e1e1", relief="groove", padx=10, command=self.guardar_orden)
        btn_guardar.pack(side="left", padx=5)


        btn_limpiar = tk.Button(frame_acc, text="Limpiar Campos", bg="#e1e1e1", relief="groove", padx=10, command=self.limpiar)
        btn_limpiar.pack(side="left", padx=5)


        # --- PESTAÑA 2: LISTADO Y ELIMINACIÓN DE ÓRDENES ---
        self.tab_listado = tk.Frame(self.notebook, bg="#dcdcdc")
        self.notebook.add(self.tab_listado, text="Historial / Listado de Órdenes")


        lbl_info_list = tk.Label(self.tab_listado, text="Seleccione una orden para cancelar o eliminar:", font=("Arial", 9), bg="#dcdcdc")
        lbl_info_list.pack(anchor="w", padx=10, pady=10)


        columnas_ordenes = ("ID", "Fecha", "Patente", "Mecánico", "Servicio", "Mano Obra", "Estado")
        self.tree_ordenes = ttk.Treeview(self.tab_listado, columns=columnas_ordenes, show="headings", height=12)
        for col in columnas_ordenes:
            self.tree_ordenes.heading(col, text=col)
            self.tree_ordenes.column(col, width=120)
        self.tree_ordenes.pack(fill="both", expand=True, padx=10, pady=5)


        frame_acc_list = tk.Frame(self.tab_listado, bg="#dcdcdc")
        frame_acc_list.pack(anchor="w", padx=10, pady=10)


        btn_eliminar_orden = tk.Button(frame_acc_list, text="Eliminar Orden Seleccionada", bg="#ffcccc", relief="groove", padx=10, command=self.eliminar_orden)
        btn_eliminar_orden.pack(side="left", padx=5)

        btn_cancelar_orden = tk.Button(frame_acc_list, text="Cancelar Orden", bg="#ffe5b4", relief="groove", padx=10, command=self.cancelar_orden)
        btn_cancelar_orden.pack(side="left", padx=5)

        btn_repuestos_orden = tk.Button(frame_acc_list, text="Editar Repuestos", bg="#e1e1e1", relief="groove", padx=10, command=self.editar_repuestos_orden)
        btn_repuestos_orden.pack(side="left", padx=5)


        btn_actualizar_lista = tk.Button(frame_acc_list, text="Actualizar Tabla", bg="#e1e1e1", relief="groove", padx=10, command=self.cargar_tabla_ordenes)
        btn_actualizar_lista.pack(side="left", padx=5)


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
            return


        for r in self.repuestos_usados:
            if r["codigo"] == codigo:
                r["cantidad"] += cantidad
                self.actualizar_tabla_repuestos()
                return


        self.repuestos_usados.append({
            "codigo": codigo,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_aplicado": precio
        })
        self.actualizar_tabla_repuestos()


    def actualizar_tabla_repuestos(self):
        for item in self.tree_repuestos.get_children():
            self.tree_repuestos.delete(item)
        subtotal_repuestos = 0.0
        for r in self.repuestos_usados:
            subt = r["cantidad"] * r["precio_aplicado"]
            subtotal_repuestos += subt
            self.tree_repuestos.insert("", "end", values=(
                r["codigo"], r["nombre"], str(r["cantidad"]), f"${subt:,.2f}"
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
            text=f"Mano de Obra: ${mano_obra:,.2f} + Subtotal Repuestos: ${subtotal_repuestos:,.2f} = TOTAL: ${total:,.2f}"
        )


    def guardar_orden(self):
        fecha = self.ent_fecha.get().strip()
        vehiculo_sel = self.cmb_vehiculo.get().strip()
        mecanico = self.ent_mecanico.get().strip()
        servicio = self.ent_servicio.get().strip()
        mano_obra_str = self.ent_mano_obra.get().strip()
        estado = self.cmb_estado.get().strip() or "En Reparación"
        if estado not in ("Pendiente", "En Reparación", "Finalizada", "Cancelada"):
            messagebox.showerror("Error", "Seleccione un estado válido para la orden.")
            return
       
        patente = self.vehiculos_dict.get(vehiculo_sel)
        if not patente:
            messagebox.showerror("Error", "Debe seleccionar un vehículo válido.")
            return
        if not servicio:
            messagebox.showerror("Error", "Debe ingresar una descripción del servicio.")
            return
        if not validar_monto(mano_obra_str):
            messagebox.showerror("Error", "El valor de Mano de Obra es inválido.")
            return


        mano_obra = float(mano_obra_str.replace(",", "."))
        exito = crear_orden_trabajo(
            fecha=fecha, observacion="", descripcion=servicio,
            mano_obra=mano_obra, patente=patente, mecanico=mecanico,
            repuestos_usados=self.repuestos_usados, estado=estado
        )


        if exito:
            messagebox.showinfo("Éxito", "Orden de Trabajo guardada correctamente.")
            self.limpiar()
            self.cargar_tabla_ordenes()
        else:
            messagebox.showerror("Error", "No se pudo registrar la Orden de Trabajo.")


    def cargar_tabla_ordenes(self):
        for item in self.tree_ordenes.get_children():
            self.tree_ordenes.delete(item)
        for o in obtener_ordenes_trabajo():
            self.tree_ordenes.insert("", "end", values=(
                o["Id_Orden"], o["Fecha"], o["Patente_Vehiculo"],
                o["Nombre_Mecanico"], o["Descripcion_Servicio"],
                f"${o['Costo_Mano_Obra']:,.2f}", o["Estado"]
            ))


    def eliminar_orden(self):
        seleccion = self.tree_ordenes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor seleccione una orden de trabajo de la tabla para eliminar.")
            return


        item = self.tree_ordenes.item(seleccion)
        id_orden = item['values'][0]
        patente = item['values'][2]


        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar la Orden ID: {id_orden} (Vehículo: {patente})?\nEsto también liberará los repuestos vinculados."
        )


        if confirmacion:
            if eliminar_orden_trabajo(id_orden):
                messagebox.showinfo("Éxito", "Orden de trabajo eliminada correctamente.")
                self.cargar_tabla_ordenes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la orden de trabajo de la base de datos.")


    def cancelar_orden(self):
        seleccion = self.tree_ordenes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una orden para cancelar.")
            return
        valores = self.tree_ordenes.item(seleccion[0], "values")
        id_orden, estado_actual = valores[0], valores[6]
        if estado_actual == "Cancelada":
            messagebox.showinfo("Información", "La orden ya está cancelada.")
            return
        if not messagebox.askyesno("Confirmar cancelación", f"¿Cancelar la orden {id_orden}? Los repuestos asignados volverán al stock."):
            return
        if actualizar_estado_orden(id_orden, "Cancelada"):
            messagebox.showinfo("Éxito", "Orden cancelada y stock reintegrado.")
            self.cargar_tabla_ordenes()
        else:
            messagebox.showerror("Error", "No se pudo cancelar la orden.")

    def editar_repuestos_orden(self):
        seleccion = self.tree_ordenes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una orden para editar sus repuestos.")
            return
        id_orden = self.tree_ordenes.item(seleccion[0], "values")[0]
        actuales = obtener_repuestos_orden(id_orden)
        repuestos = obtener_repuestos()
        ventana = tk.Toplevel(self)
        ventana.title(f"Repuestos de la orden {id_orden}")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        opciones = {}
        valores_combo = []
        for repuesto in repuestos:
            etiqueta = f"{repuesto['Codigo_Repuesto']} - {repuesto['Nombre_Repuesto']}"
            opciones[etiqueta] = repuesto
            valores_combo.append(etiqueta)
        cmb = ttk.Combobox(ventana, values=valores_combo, state="readonly", width=42)
        cmb.grid(row=0, column=0, padx=8, pady=8)
        if valores_combo:
            cmb.current(0)
        cantidad = tk.Spinbox(ventana, from_=1, to=9999, width=7)
        cantidad.grid(row=0, column=1, padx=5)

        tabla = ttk.Treeview(ventana, columns=("Código", "Repuesto", "Cantidad"), show="headings", height=8)
        for columna in ("Código", "Repuesto", "Cantidad"):
            tabla.heading(columna, text=columna)
        tabla.column("Código", width=100)
        tabla.column("Repuesto", width=240)
        tabla.column("Cantidad", width=90, anchor="center")
        tabla.grid(row=1, column=0, columnspan=3, padx=8, pady=5)

        def cargar_actuales():
            for item in tabla.get_children():
                tabla.delete(item)
            for repuesto in actuales:
                tabla.insert("", "end", iid=str(repuesto["codigo"]), values=(
                    repuesto["codigo"], repuesto["nombre"], repuesto["cantidad"]
                ))

        actuales = [{
            "codigo": r["Codigo_Repuesto"], "nombre": r["Nombre_Repuesto"],
            "cantidad": int(r["Cantidad"]), "precio_aplicado": float(r["Precio_aplicado"])
        } for r in actuales]
        cargar_actuales()

        def agregar_o_sumar():
            elegido = opciones.get(cmb.get())
            if not elegido:
                messagebox.showwarning("Atención", "Seleccione un repuesto.", parent=ventana)
                return
            try:
                unidades = int(cantidad.get())
                if unidades < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad entera mayor que cero.", parent=ventana)
                return
            codigo = elegido["Codigo_Repuesto"]
            existente = next((r for r in actuales if str(r["codigo"]) == str(codigo)), None)
            if existente:
                existente["cantidad"] += unidades
            else:
                actuales.append({"codigo": codigo, "nombre": elegido["Nombre_Repuesto"],
                                 "cantidad": unidades, "precio_aplicado": float(elegido["Precio"])})
            cargar_actuales()

        def aplicar_cantidad():
            seleccionado = tabla.selection()
            if not seleccionado:
                messagebox.showwarning("Atención", "Seleccione un repuesto de la lista.", parent=ventana)
                return
            try:
                unidades = int(cantidad.get())
                if unidades < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese una cantidad entera mayor que cero.", parent=ventana)
                return
            codigo = seleccionado[0]
            next(r for r in actuales if str(r["codigo"]) == codigo)["cantidad"] = unidades
            cargar_actuales()

        def quitar_repuesto():
            seleccionado = tabla.selection()
            if not seleccionado:
                messagebox.showwarning("Atención", "Seleccione un repuesto para quitar.", parent=ventana)
                return
            codigo = seleccionado[0]
            actuales[:] = [r for r in actuales if str(r["codigo"]) != codigo]
            cargar_actuales()

        def guardar_cambios():
            if actualizar_repuestos_orden(id_orden, actuales):
                messagebox.showinfo("Éxito", "Repuestos actualizados y stock ajustado.", parent=ventana)
                ventana.destroy()
                self.cargar_combos()
            else:
                messagebox.showerror("Error", "No se pudieron actualizar los repuestos. Verifique que haya stock suficiente.", parent=ventana)

        tk.Button(ventana, text="Agregar", command=agregar_o_sumar).grid(row=0, column=2, padx=5)
        tk.Button(ventana, text="Aplicar cantidad", command=aplicar_cantidad).grid(row=2, column=0, padx=5, pady=8, sticky="w")
        tk.Button(ventana, text="Quitar repuesto", command=quitar_repuesto).grid(row=2, column=1, padx=5, pady=8)
        tk.Button(ventana, text="Guardar cambios", command=guardar_cambios).grid(row=2, column=2, padx=5, pady=8)

    def limpiar(self):
        self.ent_servicio.delete(0, tk.END)
        self.repuestos_usados.clear()
        for item in self.tree_repuestos.get_children():
            self.tree_repuestos.delete(item)
        self.actualizar_totales(0.0)
