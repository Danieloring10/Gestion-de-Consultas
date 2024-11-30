import tkinter as tk
from pantallas.pantalla1 import Pantalla1
from pantallas.pantalla2 import Pantalla2
from pantallas.pantalla3 import Pantalla3
from pantallas.pantalla4 import Pantalla4
from pantallas.pantalla5 import Pantalla5
from pantallas.pantalla6 import Pantalla6
from pantallas.pantalla7 import Pantalla7

class GestorPantallas(tk.Tk):
    def __init__(self, sistema):
        tk.Tk.__init__(self)
        self.title("Sistema de Gestión de Pantallas")
        self.geometry("1280x720")
        self.sistema = sistema
        self.usuario_actual = None
        self.pantallas = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for P in (Pantalla1, Pantalla2, Pantalla3, Pantalla4, Pantalla5, Pantalla6, Pantalla7):
            page_name = P.__name__
            frame = P(parent=container,controller=self, sistema=sistema)
            self.pantallas[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_pantalla("Pantalla1")

    def mostrar_pantalla(self, page_name):
        frame = self.pantallas[page_name]
        if hasattr(frame, "actualizar"):
            frame.actualizar()
        frame.tkraise()