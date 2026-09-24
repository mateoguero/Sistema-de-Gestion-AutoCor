import tkinter as tk

class ReportesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#dcdcdc")
        lbl_titulo = tk.Label(self, text="Consultas y Reportes", font=("Arial", 14, "bold"), bg="#dcdcdc")
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        lbl_info = tk.Label(
            self,
            text="Módulo de reportes estadísticos, análisis de rentabilidad y control de inventario.",
            font=("Arial", 10),
            bg="#dcdcdc"
        )
        lbl_info.pack(anchor="w", padx=20, pady=5)