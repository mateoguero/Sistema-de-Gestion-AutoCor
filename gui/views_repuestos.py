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

        frame_table=tk.Frame(self)
        frame_table.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(frame_table, columns=("Código", "Nombre", "Precio", "Stock"), show="headings")
        for c in ("Código", "Nombre", "Precio", "Stock"):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar=ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")


        self.ent_codigo.bind("<Return>", lambda e:self.ent_nombre.focus_set())
        self.ent_nombre.bind("<Return>", lambda e:self.ent_precio.focus_set())
        self.ent_precio.bind("<Return>", lambda e:self.ent_stock.focus_set())
        self.ent_stock.bind("<Return>", lambda e:self.guardar())

    def guardar(self):
        cod = self.ent_codigo.get().strip()
        nom = self.ent_nombre.get().strip()
        pre = self.ent_precio.get().strip()
        stk = self.ent_stock.get().strip()

        if not cod or not nom:
            messagebox.showerror("Error", "El código y el nombre del repuesto son obligatorios.")
            return

        try:
            precio = float(pre.replace(",", "."))
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido mayor o igual a 0.")
            return

        try:
            stock = int(stk)
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un número entero mayor o igual a 0.")
            return

        if insertar_repuesto(cod, nom, precio, stock):
            messagebox.showinfo("Éxito", "Repuesto guardado correctamente")
            self.ent_codigo.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_precio.delete(0, tk.END)
            self.ent_stock.delete(0, tk.END)
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar el repuesto (verifique que el código no exista).")

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in obtener_repuestos():
            self.tree.insert("", "end", values=(r["Codigo_Repuesto"], r["Nombre_Repuesto"], f"${r['Precio']}", r["Stock"]))
    def refrescar(self):
        self.cargar_tabla()