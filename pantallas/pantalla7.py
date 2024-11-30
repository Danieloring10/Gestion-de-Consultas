from pathlib import Path
from datetime import datetime
from tkinter import  Canvas, Entry, Button, PhotoImage, Frame, Label
from tkcalendar import Calendar
from tkinter import ttk
from pantallas.clases import Profesor, Horario

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame6")
current_date_time = datetime.now()

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Pantalla7(Frame): 
    
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

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.crear_horario(),
            relief="flat"
        )
        self.button_1.place(
            x=671.0,
            y=626.0,
            width=581.0,
            height=67.0
        )

        self.canvas.create_text(
            47.0,
            28.0,
            anchor="nw",
            text="Disponibilidad",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 56 * -1)
        )
        self.cal = Calendar(self, 
            selectmode='day', 
            year=current_date_time.year, 
            month=current_date_time.month, 
            day=current_date_time.day,
            mindate = current_date_time)
        self.cal.place(x=700, 
                y=200,
                width = 500,
                height = 300
                )
        self.canvas.create_text(
            670.0,
            139.0,
            anchor="nw",
            text="Nueva disponibilidad",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 36 * -1)
        )

        self.canvas.create_rectangle(
            633.0,
            128.0,
            646.0,
            749.0,
            fill="#D9D9D9",
            outline="")

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla2"),
            relief="flat"
        )
        self.button_2.place(
            x=1018.0,
            y=28.0,
            width=203.0,
            height=78.0
        )

        self.canvas.create_text(
            700.0,
            507.0,
            anchor="nw",
            text="Hora Inicio",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 36 * -1)
        )

        self.canvas.create_text(
            1061.0,
            507.0,
            anchor="nw",
            text="Hora Fin",
            fill="#FFFFFF",
        font=("Libre Franklin Bold", 36 * -1)
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            792.5,
            580.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 36 * -1)
        )
        self.entry_1.place(
            x=675.0,
            y=556.0,
            width=235.0,
            height=47.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            1134.5,
            580.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 36 * -1)
        )
        self.entry_2.place(
            x=1017.0,
            y=556.0,
            width=235.0,
            height=47.0
        )
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview.Heading", background="darkblue", foreground="white", font=("Libre Franklin Bold", 20, "bold")) 
        self.style.configure("Treeview", background="#1E1E1E", foreground="lightgray", fieldbackground="#1E1E1E", font=("Helvetica", 10)) 
        self.style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
        # Tabla para mostrar horarios
        self.table = ttk.Treeview(self, 
            columns=("Fecha", "Inicio", "Fin"), 
            show="headings"
        )
        self.table.heading("Fecha", text="Fecha")
        self.table.heading("Inicio", text="Hora Inicio")
        self.table.heading("Fin", text="Hora Fin")
        self.table.place(x=20, y=150, width=600, height=550)

        self.style.configure("Treeview", rowheight=30) # Adjust the row height as needed 
        self.table.configure(selectmode="browse")
        self.table.place(x=20, y=150, width=600, height=450)
        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.eliminar_horario,
            relief="flat"
        )
        self.button_3.place(
            x=380.0,
            y=620.0,
            width=210.0,
            height=60.0
        )
        self.label_error = Label(
            self,
            text="",
            bg="#333333",
            fg="red",
            font=("Libre Franklin Bold", 12)
        )
        self.label_error.place(x=10, y=680, width=550, height=30)
    def actualizar(self):
        self.label_error.config(text="", fg="red")
        print("Actualizando Datos")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        """Actualiza la tabla con los horarios del profesor actual."""
        self.table.delete(*self.table.get_children())
        usuario = self.controller.usuario_actual
        if isinstance(usuario, Profesor):
            for horario in usuario.horarios:
                self.table.insert("", "end", values=(horario.fecha, horario.rango_inicio, horario.rango_fin))

    def crear_horario(self):
    
        usuario = self.controller.usuario_actual
        if not isinstance(usuario, Profesor):
            self.label_error.config(text="Solo los profesores pueden crear horarios.", fg="red")
            return

        # Obtener datos del calendario y entradas
        print(self.cal.get_date())
        fecha = datetime.strptime(self.cal.get_date(), "%m/%d/%y").date()
        inicio = self.entry_1.get().strip()
        fin = self.entry_2.get().strip()

        try:
            # Validar formato de las horas
            rango_inicio = datetime.strptime(inicio, "%H%M").time()
            rango_fin = datetime.strptime(fin, "%H%M").time()

            if rango_inicio >= rango_fin:
                self.label_error.config(text="El horario de inicio debe ser menor que el horario de fin.", fg="red")
                return

            # Verificar si hay solapamiento con horarios existentes
            for horario in usuario.horarios:
                if horario.fecha == fecha:
                    if (rango_inicio < horario.rango_fin and rango_fin > horario.rango_inicio):
                        self.label_error.config(text="El nuevo horario se solapa con un horario existente.", fg="red")
                        return

            # Crear instancia de Horario
            nuevo_horario = Horario(fecha, rango_inicio, rango_fin)
            usuario.horarios.append(nuevo_horario)

            # Actualizar tabla
            self.actualizar_tabla()
        except ValueError:
            self.label_error.config(text="Formato de hora inválido. Use HHMM (ejemplo: 1200 para las 12:00).", fg="red")


    def eliminar_horario(self):
        usuario = self.controller.usuario_actual


        seleccion = self.table.selection()
        if not seleccion:
            self.label_error.config(text="Seleccione un horario para eliminar.", fg="red")
            return

        # Obtener el horario seleccionado
        item = self.table.item(seleccion[0])["values"]
        fecha = datetime.strptime(item[0], "%Y-%m-%d").date()
        inicio = datetime.strptime(item[1], "%H:%M:%S").time()  # Ajustar formato según la tabla

        # Encontrar y eliminar el horario
        horario_eliminado = None
        for horario in usuario.horarios:
            if horario.fecha == fecha and horario.rango_inicio == inicio:
                horario_eliminado = horario
                usuario.horarios.remove(horario)
                break

        
        print(f"Horario eliminado: {horario_eliminado}")

        # Actualizar consultas asociadas
        for consulta in usuario.solicitudes:
            if consulta.fecha == fecha and horario_eliminado.rango_inicio <= consulta.hora_inicio < horario_eliminado.rango_fin:
                consulta.cambiar_estado("Negada")

        # Actualizar tabla
        self.actualizar_tabla()
        

   
    
