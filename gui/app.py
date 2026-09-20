
import tkinter as tk
from config import APP_TITLE, APP_GEOMETRY
from gui.views_clientes import ClientesView

class AutocorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        # Contenedor Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menú Lateral
        self.frame_sidebar = tk.Frame(self, bg="#1e293b", width=200)
        self.frame_sidebar.grid(row=0, column=0, sticky="nsew")

        # Área de Contenido
        self.frame_container = tk.Frame(self, bg="#ffffff")
        self.frame_container.grid(row=0, column=1, sticky="nsew")
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

        self.views = {}
        self.init_sidebar()
        self.show_view("clientes")

    def init_sidebar(self):
        lbl_logo = tk.Label(self.frame_sidebar, text="AUTOCOR", font=("Arial", 14, "bold"), fg="white", bg="#1e293b")
        lbl_logo.pack(pady=20)

        btn_clientes = tk.Button(self.frame_sidebar, text="Clientes", bg="#334155", fg="white", relief="flat",
                                 command=lambda: self.show_view("clientes"))
        btn_clientes.pack(fill="x", padx=10, pady=5)

    def show_view(self, view_name):
        if view_name == "clientes" and "clientes" not in self.views:
            self.views["clientes"] = ClientesView(self.frame_container)
            self.views["clientes"].grid(row=0, column=0, sticky="nsew")

        frame = self.views[view_name]
        frame.tkraise() 