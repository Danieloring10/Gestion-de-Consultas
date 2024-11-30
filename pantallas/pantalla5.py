from pathlib import Path
from tkinter import ttk
from tkinter import Canvas, Entry, Text, Button, PhotoImage, Frame, Label, END
from pantallas.clases import Estudiante, Consulta
import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame4")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Pantalla5(Frame): 
    def __init__(self, parent, controller, sistema): 
        Frame.__init__(self, parent)
        self.controller = controller 
        self.configure(bg="#333333")
        self.sistema = sistema
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
            text="Horarios",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 64 * -1)
        )

        self.canvas.create_rectangle(
            714.0,
            533.0,
            1221.0,
            677.0,
            fill="#D9D9D9",
            outline="")

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
            command=lambda: controller.mostrar_pantalla("Pantalla3"),
            relief="flat"
        )
        self.button_1.place(
            x=1018.0,
            y=28.0,
            width=203.0,
            height=78.0
        )

        self.canvas.create_text(
            734.0,
            544.0,
            anchor="nw",
            text="Ingresa la duración\nde la consulta (minutos):",
            fill="#000000",
            font=("Libre Franklin Bold", 24 * -1)
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            871.5,
            634.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 40 * -1)
        )
        self.entry_1.place(
            x=734.0,
            y=610.0,
            width=275.0,
            height=47.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command= self.crear_consulta,
            relief="flat"
        )
        self.button_2.place(
            x=1051.0,
            y=544.0,
            width=155.0,
            height=115.0
        )
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", background="darkblue", foreground="white", font=("Libre Franklin Bold", 12, "bold")) 
        self.style.configure("Treeview", background="#1E1E1E", foreground="lightgray", fieldbackground="#1E1E1E", font=("Libre Franklin Bold", 10)) 
        self.style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
        self.table = ttk.Treeview(self, 
            columns=("Profesor", "Fecha", "Hora Inicio", "Hora Fin"), 
            show="headings"
        )
        self.table.heading("Profesor", text="Profesor")
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Hora Inicio", text="Hora Inicio")
        self.table.heading("Hora Fin", text="Hora Fin")

        # Establecer el ancho de las columnas
        self.table.column("Profesor", width=200)
        self.table.column("Fecha", width=100)
        self.table.column("Hora Inicio", width=100)
        self.table.column("Hora Fin", width=100)

        # Mostrar la tabla en la interfaz
        self.table.place(x=20, y=150, width=600, height=450)
        self.label_error = Label(
            self,
            text="",
            bg="#333333",
            fg="red",
            font=("Libre Franklin Bold", 20)
        )
        self.label_error.place(x=15, y=650, width=580, height=30)
    def actualizar(self): 
        self.label_error.config(text="", fg="red")
        self.actualizar_tabla(self.sistema)
        self.entry_1.delete(0,END)
        print("Actualizando Datos")

    def actualizar_tabla(self, sistema):
        """Llena la tabla con los horarios disponibles de todos los profesores."""
        self.table.delete(*self.table.get_children())
        for profesor in sistema.profesores:
            for horario in profesor.horarios:
                self.table.insert("", "end", values=(
                    profesor.nombre,
                    horario.fecha,
                    horario.rango_inicio,
                    horario.rango_fin
                ))

    def crear_consulta(self):

        usuario = self.controller.usuario_actual
        seleccion = self.table.selection()
        if not seleccion:
            self.label_error.config(text="Seleccione un horario para crear la consulta.", fg="red")
            return

        # Obtener los datos del horario seleccionado
        item = self.table.item(seleccion[0])["values"]
        profesor_nombre = item[0]
        #fecha = datetime.datetime.strptime(item[1], "%Y-%m-%d").date()
        fecha = item[1]
        inicio_str = item[2]
        fin_str = item[3]

        rango_inicio = datetime.datetime.strptime(inicio_str, "%H:%M:%S").time()
        rango_fin = datetime.datetime.strptime(fin_str, "%H:%M:%S").time()

        # Buscar al profesor y el horario
        profesor = next((p for p in self.controller.sistema.profesores if p.nombre == profesor_nombre), None)

        horario = next((h for h in profesor.horarios if h.fecha == datetime.datetime.strptime(fecha, "%Y-%m-%d").date() and h.rango_inicio == rango_inicio), None)


        # Validar duración
        try:
            duracion = int(self.entry_1.get().strip())
            if duracion <= 0:
                self.label_error.config(text="La duración debe ser un número positivo.", fg="red")
                return

            # Validar que la duración no exceda el rango de tiempo del horario
            tiempo_restante = (datetime.datetime.combine(datetime.date.today(), rango_fin) -
                            datetime.datetime.combine(datetime.date.today(), rango_inicio)).seconds // 60
            if duracion > tiempo_restante:
                self.label_error.config(text="La duración excede el rango disponible.", fg="red")
                return
        except ValueError:
            self.label_error.config(text="Duración inválida. Ingrese un número entero.", fg="red")
            return

        # Crear la consulta
        consulta = Consulta(
            hora_inicio=rango_inicio,
            fecha= datetime.datetime.strptime(fecha, "%Y-%m-%d").date(),
            duracion_minutos=duracion,
            estado="En espera",
            estudiante=usuario,
            profesor=profesor
        )
        usuario.consultas.append(consulta)
        profesor.solicitudes.append(consulta)
        print(f"Consulta creada: {consulta}")
        self.label_error.config(text=f"Consulta creada", fg="green")

        # Actualizar el horario
        horario.modificar_rango(rango_inicio, duracion)
        print(f"Horario actualizado: {horario}")

        # Actualizar la tabla
        self.actualizar_tabla(self.controller.sistema)
    