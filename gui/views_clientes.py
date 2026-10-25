import tkinter as tk
from tkinter import ttk, messagebox
from database.queries import obtener_clientes, insertar_cliente, actualizar_cliente
from utils.validators import validar_documento, validar_email


class ClientesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        self.create_widgets()
        self.cargar_tabla()


    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Gestión de Clientes", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=10)


        frame_form = tk.LabelFrame(self, text="Registrar / Editar Cliente", font=("Arial", 10), bg="#dcdcdc", padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)


        tk.Label(frame_form, text="DNI / CUIT:", bg="#dcdcdc").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_doc = tk.Entry(frame_form, width=20)
        self.ent_doc.grid(row=0, column=1, padx=5, pady=4)


        tk.Label(frame_form, text="Nombre:", bg="#dcdcdc").grid(row=0, column=2, sticky="w", pady=4)
        self.ent_nombre = tk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=4)


        tk.Label(frame_form, text="Apellido:", bg="#dcdcdc").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_apellido = tk.Entry(frame_form, width=20)
        self.ent_apellido.grid(row=1, column=1, padx=5, pady=4)


        tk.Label(frame_form, text="Teléfono:", bg="#dcdcdc").grid(row=1, column=2, sticky="w", pady=4)
        self.ent_telefono = tk.Entry(frame_form, width=25)
        self.ent_telefono.grid(row=1, column=3, padx=5, pady=4)


        tk.Label(frame_form, text="Email:", bg="#dcdcdc").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_email = tk.Entry(frame_form, width=20)
        self.ent_email.grid(row=2, column=1, padx=5, pady=4)


        frame_btn = tk.Frame(frame_form, bg="#dcdcdc")
        frame_btn.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")


        self.btn_guardar = tk.Button(frame_btn, text="Guardar Cliente", bg="#e1e1e1", relief="groove", padx=10, command=self.guardar)
        self.btn_guardar.pack(side="left", padx=5)


        btn_modificar = tk.Button(frame_btn, text="Modificar", bg="#e1e1e1", relief="groove", padx=10)
        btn_modificar.config(command=self.modificar)
        btn_modificar.pack(side="left", padx=5)



        btn_limpiar = tk.Button(frame_btn, text="Limpiar Campos", bg="#e1e1e1", relief="groove", padx=10, command=self.limpiar)
        btn_limpiar.pack(side="left", padx=5)

        frame_table=tk.Frame(self)

        columnas = ("Doc", "Nombre", "Apellido", "Teléfono", "Email")
        self.tree = ttk.Treeview(frame_table, columns=columnas, show="headings")
        for columna in columnas:
            self.tree.heading(columna, text=columna)
            self.tree.column(columna, width=120)
        self.tree.pack(fill="both", expand=True, side="left")

        frame_table.pack(fill="both", expand=True, padx=20, pady=10)
        scrollbar=ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
       
        # Vincular el evento de selección de la tabla para cargar los datos en el formulario
        self.tree.bind("<<TreeviewSelect>>", self.cargar_seleccion)

        self.ent_doc.bind("<Return>", lambda e:self.ent_nombre.focus_set())
        self.ent_nombre.bind("<Return>", lambda e:self.ent_apellido.focus_set())
        self.ent_apellido.bind("<Return>", lambda e:self.ent_telefono.focus_set())
        self.ent_telefono.bind("<Return>", lambda e:self.ent_email.focus_set())
        self.ent_email.bind("<Return>", lambda e:self.guardar())

    def guardar(self):
        # Si hay una fila seleccionada, Guardar aplica los cambios a ese cliente.
        if self.tree.selection():
            self.modificar()
            return

        doc = self.ent_doc.get().strip()
        nom = self.ent_nombre.get().strip()
        ape = self.ent_apellido.get().strip()
        tel = self.ent_telefono.get().strip()
        email = self.ent_email.get().strip()


        if not validar_documento(doc):
            messagebox.showerror("Error", "Documento/CUIT inválido (debe contener entre 7 y 11 dígitos)")
            return


        if not nom or not ape:
            messagebox.showerror("Error", "Nombre y apellido son obligatorios.")
            return


        if not validar_email(email):
            messagebox.showerror("Error", "Formato de Email inválido")
            return


        if insertar_cliente(doc, nom, ape, tel, email):
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
            self.limpiar()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo guardar el cliente en la base de datos (verifique si el DNI ya existe)")


    def modificar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atencion", "Seleccione un cliente de la tabla para modificar.")
            return

        documento_original = str(self.tree.item(seleccion[0], "values")[0])
        doc = self.ent_doc.get().strip()
        nom = self.ent_nombre.get().strip()
        ape = self.ent_apellido.get().strip()
        tel = self.ent_telefono.get().strip()
        email = self.ent_email.get().strip()

        if not validar_documento(doc):
            messagebox.showerror("Error", "Documento/CUIT inválido (debe contener entre 7 y 11 dígitos)")
            return
        if not nom or not ape:
            messagebox.showerror("Error", "Nombre y apellido son obligatorios.")
            return
        if not validar_email(email):
            messagebox.showerror("Error", "Formato de Email inválido")
            return

        if actualizar_cliente(documento_original, doc, nom, ape, tel, email):
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
            self.limpiar()
            self.cargar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el cliente. Verifique que el documento no esté usado por otro cliente.")


    def cargar_seleccion(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion)
            valores = item['values']
            if valores:
                # 1. Limpiar manualmente los campos sin borrar la selección de la tabla
                self.ent_doc.config(state="normal") # Por si se deshabilita en edición
                self.ent_doc.delete(0, tk.END)
                self.ent_nombre.delete(0, tk.END)
                self.ent_apellido.delete(0, tk.END)
                self.ent_telefono.delete(0, tk.END)
                self.ent_email.delete(0, tk.END)

                # 2. Insertar los nuevos valores
                self.ent_doc.insert(0, valores[0])
                self.ent_nombre.insert(0, valores[1])
                self.ent_apellido.insert(0, valores[2])
                self.ent_telefono.insert(0, valores[3] if valores[3] else "")
                self.ent_email.insert(0, valores[4] if valores[4] else "")
                self.btn_guardar.config(text="Actualizar Cliente")

    def limpiar(self):
        self.btn_guardar.config(text="Guardar Cliente")
        self.ent_doc.config(state="normal")
        self.ent_doc.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_apellido.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())


    def cargar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for cliente in obtener_clientes():
            self.tree.insert("", "end", values=(
                cliente["Documento"], cliente["Nombre"],
                cliente["Apellido"], cliente["Telefono"], cliente["Email"]
            ))

    def refrescar(self):
        self.cargar_tabla()