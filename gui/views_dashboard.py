import tkinter as tk
from database.queries import obtener_metricas_dashboard

class DashboardView(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#dcdcdc")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl_titulo = tk.Label(self, text="Panel de Control General", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        frame_cards = tk.Frame(self, bg="#dcdcdc")
        frame_cards.pack(fill="x", padx=20, pady=10)

        metricas = obtener_metricas_dashboard()

        self.crear_tarjeta(frame_cards, "Órdenes Activas", str(metricas.get("activas", 6)), "#0078d7", 0)
        self.crear_tarjeta(frame_cards, "En Reparación", str(metricas.get("en_reparacion", 2)), "#d86900", 1)
        self.crear_tarjeta(frame_cards, "Vehículos en Taller", str(metricas.get("vehiculos", 4)), "#107c41", 2)
        self.crear_tarjeta(frame_cards, "Stock Crítico", f"{metricas.get('stock_critico', 1)} Alerta", "#d13438", 3)

        frame_acciones = tk.LabelFrame(self, text="Acciones Rápidas", font=("Arial", 10, "bold"), bg="#dcdcdc", padx=15, pady=15)
        frame_acciones.pack(fill="x", padx=20, pady=20)

        btn_nueva_orden = tk.Button(
            frame_acciones, text="+ Crear Nueva Orden de Trabajo", font=("Arial", 9),
            bg="#e1e1e1", relief="groove", padx=10, pady=5, cursor="hand2",
            command=lambda: self.controller.show_view("ordenes") if self.controller else None
        )
        btn_nueva_orden.pack(side="left", padx=10)

        btn_nuevo_cliente = tk.Button(
            frame_acciones, text="+ Registrar Nuevo Cliente", font=("Arial", 9),
            bg="#e1e1e1", relief="groove", padx=10, pady=5, cursor="hand2",
            command=lambda: self.controller.show_view("clientes") if self.controller else None
        )
        btn_nuevo_cliente.pack(side="left", padx=10)

        btn_ver_stock = tk.Button(
            frame_acciones, text="Verificar Stock de Repuestos", font=("Arial", 9),
            bg="#e1e1e1", relief="groove", padx=10, pady=5, cursor="hand2",
            command=lambda: self.controller.show_view("repuestos") if self.controller else None
        )
        btn_ver_stock.pack(side="left", padx=10)

    def crear_tarjeta(self, parent, titulo, valor, color_val, col):
        card = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1, padx=15, pady=15)
        card.grid(row=0, column=col, padx=8, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        lbl_t = tk.Label(card, text=titulo, font=("Arial", 9), fg="#555555", bg="#ffffff")
        lbl_t.pack(anchor="w")

        lbl_v = tk.Label(card, text=valor, font=("Arial", 16, "bold"), fg=color_val, bg="#ffffff")
        lbl_v.pack(anchor="w", pady=(10, 0))