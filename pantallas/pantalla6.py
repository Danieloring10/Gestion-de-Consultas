from pathlib import Path
import datetime
from tkinter import Canvas, Button, PhotoImage, Frame
from tkinter import ttk
from pantallas.clases import Profesor
import re
current_date_time = datetime.datetime.now()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame5")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Pantalla6(Frame): 
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

        self.canvas.create_rectangle(
            671.0,
            552.0,
            1252.0,
            693.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_text(
            47.0,
            20.0,
            anchor="nw",
            text="Gestionar Consultas",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 64 * -1)
        )

        self.canvas.create_rectangle(
            633.0,
            128.0,
            646.0,
            749.0,
            fill="#D9D9D9",
            outline="")
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla2"),
            relief="flat"
        )
        self.button_1.place(
            x=1018.0,
            y=28.0,
            width=203.0,
            height=78.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command= self.aceptar_consulta,
            relief="flat"
        )
        self.button_2.place(
            x=693.0,
            y=565.0,
            width=155.0,
            height=115.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.negar_consulta,
            relief="flat"
        )
        self.button_3.place(
            x=884.0,
            y=565.0,
            width=155.0,
            height=115.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.en_espera_consulta,
            relief="flat"
        )
        self.button_4.place(
            x=1075.0,
            y=565.0,
            width=155.0,
            height=115.0
        )
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Libre Franklin Bold", 20, "bold")) 
        self.style.configure("Treeview", background="#1E1E1E", foreground="lightgray", fieldbackground="#1E1E1E", font=("Libre Franklin Bold", 12)) 
        self.style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
        self.table = ttk.Treeview(self, 
            columns=("Alumno", "Fecha", "Hora", "Duracion"), 
            show="headings"
        )
        self.table.heading("Alumno", text="Alumno")
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Hora", text="Hora Inicio")
        self.table.heading("Duracion", text="Duración")

        # Establecer el ancho de las columnas
        self.table.column("Alumno", width=100)
        self.table.column("Fecha", width=100)
        self.table.column("Hora", width=100)
        self.table.column("Duracion", width=100)

        self.style.configure("Treeview", rowheight=30)
        self.table.configure(selectmode="browse")
        self.table.place(x=20, y=150, width=600, height=550)

         # Asignar evento de selección en la tabla
        #self.table.bind("<<TreeviewSelect>>", self.on_table_select)
    def actualizar(self):
        """Actualizar la tabla con las consultas 'En espera' asociadas al profesor."""
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Llena la tabla con las consultas 'En espera' asociadas al profesor."""
        usuario = self.controller.usuario_actual
        if isinstance(usuario, Profesor):
            self.table.delete(*self.table.get_children())
            for consulta in usuario.solicitudes:
                if consulta.estado == "En espera":
                    self.table.insert("", "end", values=(
                        consulta.estudiante.nombre,
                        consulta.fecha,
                        consulta.hora_inicio.strftime("%H:%M"),
                        consulta.duracion_minutos
                    ))

    def obtener_consulta_seleccionada(self):
        """Obtiene la consulta seleccionada usando el índice de la fila."""
        seleccion = self.table.selection()
        if not seleccion:
            print("Seleccione una consulta.")
            return None

        index = self.table.index(seleccion[0])  # Índice de la fila seleccionada
        usuario = self.controller.usuario_actual
        return usuario.solicitudes[index]

    def aceptar_consulta(self):
        """Aceptar la consulta seleccionada."""
        consulta = self.obtener_consulta_seleccionada()
        if consulta:
            consulta.cambiar_estado("Confirmada")
            #consulta.profesor.actualizar_disponibilidad(consulta)
            print(f"Consulta aceptada: {consulta}")
            self.actualizar_tabla()

    def negar_consulta(self):
        """Negar la consulta seleccionada."""
        consulta = self.obtener_consulta_seleccionada()
        if consulta:
            consulta.cambiar_estado("Rechazada")
            print(f"Consulta negada: {consulta}")
            self.actualizar_tabla()

    def en_espera_consulta(self):
        """Mover la consulta seleccionada al final de la lista."""
        consulta = self.obtener_consulta_seleccionada()
        if consulta:
            profesor = consulta.profesor
            profesor.solicitudes.remove(consulta)
            profesor.solicitudes.append(consulta)
            print(f"Consulta movida a 'En espera': {consulta}")
            self.actualizar_tabla()

    def actualizar_calendario(self):
        """Actualizar el calendario con la fecha de la consulta seleccionada."""
        consulta = self.obtener_consulta_seleccionada()
        if consulta:
            if isinstance(consulta.fecha, datetime.date):  # Asegurarnos de que es un objeto datetime.date
                self.cal.selection_set(consulta.fecha)  # Establecer la fecha seleccionada en el calendario
                self.cal.see(consulta.fecha)  # Asegurarnos de que la fecha seleccionada sea visible
                print(f"Calendario actualizado a la fecha: {consulta.fecha}")
            else:
                print(f"Formato de fecha incorrecto: {consulta.fecha}")

