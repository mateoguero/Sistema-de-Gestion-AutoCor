import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_repuestos, insertar_repuesto

class RepuestosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.create_widgets()
        self.cargar_tabla()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Repuestos y Stock", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        frame_form = tk.LabelFrame(self, text="Registrar Nuevo Repuesto", font=("Arial", 10), bg="#dcdcdc", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Código:", bg="#dcdcdc").grid(row=0, column=0, sticky="e", padx=5)
        self.ent_codigo = tk.Entry(frame_form, width=15)
        self.ent_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre Repuesto:", bg="#dcdcdc").grid(row=0, column=2, sticky="e", padx=5)
        self.ent_nombre = tk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Precio ($):", bg="#dcdcdc").grid(row=1, column=0, sticky="e", padx=5)
        self.ent_precio = tk.Entry(frame_form, width=15)
        self.ent_precio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Stock Inicial:", bg="#dcdcdc").grid(row=1, column=2, sticky="e", padx=5)
        self.ent_stock = tk.Entry(frame_form, width=15)
        self.ent_stock.grid(row=1, column=3, padx=5, pady=5)

        btn_guardar = tk.Button(frame_form, text="Guardar Repuesto", bg="#e1e1e1", relief="groove", command=self.guardar)
        btn_guardar.grid(row=2, column=3, pady=10, sticky="e")

        self.tree = ttk.Treeview(self, columns=("Código", "Nombre", "Precio", "Stock"), show="headings")
        for c in ("Código", "Nombre", "Precio", "Stock"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def guardar(self):
        cod = self.ent_codigo.get().strip()
        nom = self.ent_nombre.get().strip()
        pre = self.ent_precio.get().strip()
        stk = self.ent_stock.get().strip()

        if insertar_repuesto(cod, nom, pre, stk):
            messagebox.showinfo("Éxito", "Repuesto guardado correctamente")
            self.cargar_tabla()

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in obtener_repuestos():
            self.tree.insert("", "end", values=(r["Codigo_Repuesto"], r["Nombre_Repuesto"], f"${r['Precio']}", r["Stock"]))