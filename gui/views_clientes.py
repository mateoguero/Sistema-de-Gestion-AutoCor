import tkinter as tk
from tkinter import ttk, messagebox

from database.queries import obtener_clientes, insertar_cliente
from utils.validators import validar_documento, validar_email


class ClientesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")
        self.create_widgets()
        self.cargar_tabla()

    def create_widgets(self):
        # Título
        lbl_titulo = tk.Label(
            self,
            text="Gestión de Clientes",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
        )
        lbl_titulo.pack(anchor="w", padx=20, pady=10)

        # Formulario de registro
        frame_form = tk.LabelFrame(
            self, text="Registrar / Editar Cliente", padx=10, pady=10
        )
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="DNI/CUIT:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.ent_doc = tk.Entry(frame_form)
        self.ent_doc.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Nombre:").grid(
            row=0, column=2, sticky="w", pady=2
        )
        self.ent_nombre = tk.Entry(frame_form)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Apellido:").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.ent_apellido = tk.Entry(frame_form)
        self.ent_apellido.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Teléfono:").grid(
            row=1, column=2, sticky="w", pady=2
        )
        self.ent_telefono = tk.Entry(frame_form)
        self.ent_telefono.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Email:").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.ent_email = tk.Entry(frame_form)
        self.ent_email.grid(row=2, column=1, padx=5, pady=2)

        btn_guardar = tk.Button(
            frame_form, text="Guardar Cliente", command=self.guardar
        )
        btn_guardar.grid(row=2, column=3, pady=5, sticky="e")

        # Tabla de clientes
        columnas = ("Doc", "Nombre", "Apellido", "Teléfono", "Email")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=120)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def guardar(self):
        doc = self.ent_doc.get()
        nom = self.ent_nombre.get()
        ape = self.ent_apellido.get()
        tel = self.ent_telefono.get()
        email = self.ent_email.get()

        if not validar_documento(doc):
            messagebox.showerror("Error", "Documento inválido")
            return

        if not validar_email(email):
            messagebox.showerror("Error", "Email inválido")
            return

        if insertar_cliente(doc, nom, ape, tel, email):
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in obtener_clientes():
            self.tree.insert(
                "",
                "end",
                values=(
                    cliente["Documento"],
                    cliente["Nombre"],
                    cliente["Apellido"],
                    cliente["Telefono"],
                    cliente["Email"],
                ),
            )
