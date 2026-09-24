import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_mecanicos, insertar_mecanico

class MecanicosView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.create_widgets()
        self.cargar_tabla()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Nómina de Personal Técnico (Mecánicos)", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        frame_form = tk.LabelFrame(self, text="Registro de Mecánico", font=("Arial", 10), bg="#dcdcdc", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="DNI:", bg="#dcdcdc").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ent_dni = tk.Entry(frame_form, width=20)
        self.ent_dni.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:", bg="#dcdcdc").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.ent_nombre = tk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Apellido:", bg="#dcdcdc").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.ent_apellido = tk.Entry(frame_form, width=20)
        self.ent_apellido.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Especialidad:", bg="#dcdcdc").grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.cmb_especialidad = ttk.Combobox(
            frame_form,
            values=["Frenos y Motor", "Inyección Electrónica", "Frenos y Suspensión", "Electricidad"],
            width=22
        )
        self.cmb_especialidad.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Teléfono:", bg="#dcdcdc").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.ent_telefono = tk.Entry(frame_form, width=20)
        self.ent_telefono.grid(row=2, column=1, padx=5, pady=5)

        frame_btn = tk.Frame(self, bg="#dcdcdc")
        frame_btn.pack(fill="x", padx=20, pady=10)

        btn_agregar = tk.Button(frame_btn, text="Agregar Mecánico", bg="#e1e1e1", relief="groove", padx=10, command=self.guardar)
        btn_agregar.pack(side="left", padx=5)

        btn_editar = tk.Button(frame_btn, text="Editar", bg="#e1e1e1", relief="groove", padx=15)
        btn_editar.pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "DNI", "Nombre", "Apellido"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("DNI", width=150)
        self.tree.column("Nombre", width=200)
        self.tree.column("Apellido", width=200)

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def guardar(self):
        dni = self.ent_dni.get().strip()
        nom = self.ent_nombre.get().strip()
        ape = self.ent_apellido.get().strip()
        esp = self.cmb_especialidad.get().strip()
        tel = self.ent_telefono.get().strip()

        if not (dni and nom and ape and esp):
            messagebox.showerror("Error", "Por favor complete DNI, Nombre, Apellido y Especialidad")
            return

        if insertar_mecanico(dni, nom, ape, esp, tel):
            messagebox.showinfo("Éxito", "Mecánico agregado correctamente")
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo registrar el mecánico")

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in obtener_mecanicos():
            dni_val = m.get("DNI", "30123456")
            self.tree.insert("", "end", values=(m["Id_Mecanico"], dni_val, m["Nombre"], m["Apellido"]))