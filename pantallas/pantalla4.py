from pathlib import Path
from tkinter import ttk
from tkinter import Canvas, Entry, Text, Button, PhotoImage, Frame
import datetime
from pantallas.clases import Estudiante

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Pantalla4(Frame): 
    def __init__(self, parent, controller, sistema): 
        Frame.__init__(self, parent)
        self.controller = controller 
        self.configure(bg="#333333")
        self.canvas = Canvas(
            self,
            bg = "#333333",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            1280.0,
            128.0,
            fill="#7F7F7F",
            outline="")

        self.canvas.create_text(
            47.0,
            28.0,
            anchor="nw",
            text="Consultas",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 64 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla3"),
            relief="flat"
        )
        self.button_1.place(
            x=1049.0,
            y=28.0,
            width=155.0,
            height=78.0
        )
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Libre Franklin Bold", 20, "bold")) 
        self.style.configure("Treeview", background="#1E1E1E", foreground="lightgray", fieldbackground="#1E1E1E", font=("Libre Franklin Bold", 20)) 
        self.style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
        self.table = ttk.Treeview(self, 
            columns=("Profesor", "Fecha", "Horario", "Duracion", "Estado"), 
            show="headings"
        )
        self.table.heading("Profesor", text="Profesor")
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Horario", text="Horario")
        self.table.heading("Duracion", text="Duración")
        self.table.heading("Estado", text="Estado")

        # Establecer el ancho de las columnas
        self.table.column("Profesor", width=100)
        self.table.column("Fecha", width=100)
        self.table.column("Horario", width=100)
        self.table.column("Duracion", width=100)
        self.table.column("Estado", width=100)

        self.style.configure("Treeview", rowheight=50) # Adjust the row height as needed 
        self.table.place(x=40, y=150, width=1200, height=450)
        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command = self.eliminar_consulta,
            relief="flat"
        )
        self.button_2.place(
            x=850.0,
            y=620.0,
            width=350.0,
            height=60.0
        )
    def actualizar(self): 
        self.actualizar_tabla()
        print("Actualizando Datos")
    def actualizar_tabla(self): 
        usuario = self.controller.usuario_actual
        if isinstance(usuario, Estudiante):
            self.table.delete(*self.table.get_children())  # Limpiar la tabla antes de llenarla
            # Recorrer las consultas del estudiante y agregarlas a la tabla
            for idx, consulta in enumerate(usuario.consultas):
                self.table.insert("", "end", values=(
                    consulta.profesor.nombre,  # Profesor
                    consulta.fecha,  # Fecha de la consulta
                    consulta.hora_inicio,  # Hora de inicio
                    consulta.duracion_minutos,
                    consulta.estado  # Estado de la consulta
                ), tags=(idx,))

    def eliminar_consulta(self):
        seleccion = self.table.selection()
        if not seleccion:
            print("Seleccione una consulta para eliminar.")
            return

        # Obtener el índice de la fila seleccionada
        idx = self.table.item(seleccion[0])['tags'][0]  # Obtener el índice de la consulta desde 'tags'
        usuario = self.controller.usuario_actual
        
        # Acceder a la consulta usando el índice
        consulta = usuario.consultas[idx]

        # Eliminar la consulta de las listas del estudiante y del profesor
        profesor = consulta.profesor
        usuario.consultas.remove(consulta)
        profesor.solicitudes.remove(consulta)

        # Cambiar el estado de la consulta a "Negada"
        consulta.cambiar_estado("Negada")
        print(f"Consulta eliminada: {consulta}")

        # Actualizar la tabla después de la eliminación
        self.actualizar_tabla()
