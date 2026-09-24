"""Módulo de la ventana principal y navegación de la aplicación AUTOCOR."""

import tkinter as tk
from config import APP_TITLE, APP_GEOMETRY
from gui.views_dashboard import DashboardView
from gui.views_clientes import ClientesView
from gui.views_vehiculo import VehiculosView
from gui.views_mecanicos import MecanicosView
from gui.views_repuestos import RepuestosView
from gui.views_ordenes import OrdenesView
from gui.views_reportes import ReportesView


class AutocorApp(tk.Tk):
    """Clase principal de la interfaz gráfica."""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.configure(bg="#2c384e")

        self.views = {}
        self.sidebar_buttons = {}

        self.create_header()
        self.create_body()
        self.show_view("dashboard")

    def create_header(self):
        frame_header = tk.Frame(self, bg="#2c384e", height=38)
        frame_header.pack(fill="x", side="top", padx=10, pady=4)

        lbl_logo = tk.Label(
            frame_header, text="AUTOCOR | Taller & Repuestera",
            font=("Arial", 11, "bold"), fg="white", bg="#2c384e"
        )
        lbl_logo.pack(side="left")

        lbl_status = tk.Label(
            frame_header,
            text="Operador: Recepción / Administración  |  Estado: Conectado BDD",
            font=("Arial", 9), fg="#94a3b8", bg="#2c384e"
        )
        lbl_status.pack(side="right")

    def create_body(self):
        frame_main = tk.Frame(self, bg="#dcdcdc")
        frame_main.pack(fill="both", expand=True)

        self.frame_sidebar = tk.Frame(frame_main, bg="#1e2638", width=190)
        self.frame_sidebar.pack(side="left", fill="y")
        self.frame_sidebar.pack_propagate(False)

        lbl_menu_title = tk.Label(
            self.frame_sidebar, text="MENÚ PRINCIPAL",
            font=("Arial", 8, "bold"), fg="#94a3b8", bg="#1e2638"
        )
        lbl_menu_title.pack(anchor="w", padx=12, pady=(15, 10))

        opciones = [
            ("Inicio / Dashboard", "dashboard"),
            ("Clientes", "clientes"),
            ("Vehículos", "vehiculos"),
            ("Mecánicos", "mecanicos"),
            ("Repuestos / Stock", "repuestos"),
            ("Órdenes de Trabajo", "ordenes"),
            ("Consultas y Reportes", "reportes")
        ]

        for texto, clave in opciones:
            btn = tk.Button(
                self.frame_sidebar, text=f"  {texto}", font=("Arial", 9, "bold"),
                bg="#1e2638", fg="white", activebackground="#0084c7", activeforeground="white",
                bd=0, anchor="w", cursor="hand2",
                command=lambda k=clave: self.show_view(k)
            )
            btn.pack(fill="x", pady=2, ipady=6)
            self.sidebar_buttons[clave] = btn

        self.frame_container = tk.Frame(frame_main, bg="#dcdcdc")
        self.frame_container.pack(side="right", fill="both", expand=True)
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)

    def show_view(self, view_name):
        for k, btn in self.sidebar_buttons.items():
            if k == view_name:
                btn.config(bg="#0084c7", fg="white")
            else:
                btn.config(bg="#1e2638", fg="white")

        try:
            if view_name not in self.views:
                if view_name == "dashboard":
                    self.views["dashboard"] = DashboardView(self.frame_container, controller=self)
                elif view_name == "clientes":
                    self.views["clientes"] = ClientesView(self.frame_container)
                elif view_name == "vehiculos":
                    self.views["vehiculos"] = VehiculosView(self.frame_container)
                elif view_name == "mecanicos":
                    self.views["mecanicos"] = MecanicosView(self.frame_container)
                elif view_name == "repuestos":
                    self.views["repuestos"] = RepuestosView(self.frame_container)
                elif view_name == "ordenes":
                    self.views["ordenes"] = OrdenesView(self.frame_container)
                elif view_name == "reportes":
                    self.views["reportes"] = ReportesView(self.frame_container)

                self.views[view_name].grid(row=0, column=0, sticky="nsew")

            frame = self.views[view_name]
            frame.tkraise()
        except Exception as e:
            print(f"Error al cambiar a la vista {view_name}: {e}")