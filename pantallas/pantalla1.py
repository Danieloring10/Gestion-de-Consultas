from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, Label, Frame, END
from pantallas.clases import Estudiante,Profesor

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def validar_datos(self, controller, rol):
        matricula = self.entry_1.get().strip()
        contrasena = self.entry_2.get().strip()
        nombre = self.entry_3.get().strip()
        # Validar formato de matrícula y contraseña
        if not matricula.isdigit() or len(matricula) != 6:
            self.label_error.config(text="La matrícula debe ser un número de 6 dígitos.", fg="red")
            return

        if not contrasena:
            self.label_error.config(text="La contraseña no puede estar vacía.", fg="red")
            return

        sistema = controller.sistema

        usuario = sistema.autenticar_usuario(int(matricula), rol)
        if usuario:
            if(usuario.contrasenia != contrasena):
                self.label_error.config(text="Contraseña incorrecta", fg="red")
                return
            # Autenticar usuario si la matrícula y contraseña coinciden
            self.label_error.config(text="", fg="green")
            controller.usuario_actual = usuario
            if rol == "E":
                controller.mostrar_pantalla("Pantalla3")  # Menú del alumno
            elif rol == "P":
                controller.mostrar_pantalla("Pantalla2")  # Menú del profesor
        else:
            # Si la matrícula no existe, validar que el nombre esté completo
            if not nombre:
                self.label_error.config(text="Debe ingresar un nombre para registrarse.")
                return

            # Crear una nueva instancia
            if rol == "E":
                nuevo_usuario = Estudiante(
                    nombre=nombre,
                    email=f"{matricula}@uni.edu",  # Generar email genérico
                    contrasenia=contrasena,
                    matricula=int(matricula)
                )
                sistema.agregar_estudiante(nuevo_usuario)
                controller.usuario_actual = nuevo_usuario
                self.label_error.config(text="Nuevo alumno registrado.", fg="green")
                controller.mostrar_pantalla("Pantalla3")
            elif rol == "P":
                nuevo_usuario = Profesor(
                    nombre=nombre,
                    email=f"profesor{matricula}@uni.edu",  # Generar email genérico
                    contrasenia=contrasena,
                    id_profesor=int(matricula)
                )
                sistema.agregar_profesor(nuevo_usuario)
                controller.usuario_actual = nuevo_usuario
                self.label_error.config(text="Nuevo profesor registrado.", fg="green")
                controller.mostrar_pantalla("Pantalla2")

class Pantalla1(Frame): 
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
            text="Inicio de sesión ",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 64 * -1)
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            641.0,
            200.5,
            image=self.entry_image_3
        )
        self.entry_3 = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 22 * -1)
        )
        self.entry_3.place(
            x=488.0,
            y=175.0,
            width=306.0,
            height=49.0
        )
        self.canvas.create_text(
            488.0,
            130.0,
            anchor="nw",
            text="Nombre",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 32 * -1)
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            641.0,
            300.5,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 22 * -1)
        )
        self.entry_1.place(
            x=488.0,
            y=280.0,
            width=306.0,
            height=49.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            641.0,
            390.5,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Libre Franklin Bold", 22 * -1)
        )
        self.entry_2.place(
            x=488.0,
            y=370.0,
            width=306.0,
            height=49.0
        )

        self.canvas.create_text(
            488.0,
            235.0,
            anchor="nw",
            text="Matrícula",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 32 * -1)
        )

        self.canvas.create_text(
            488.0,
            320.0,
            anchor="nw",
            text="Contraseña",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 32 * -1)
        )

        self.canvas.create_text(
            488.0,
            445.0,
            anchor="nw",
            text="Ingresar como",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 32 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: validar_datos(self, controller, "P"),
            relief="flat"
        )
        self.button_1.place(
            x=486.0,
            y=600.0,
            width=306.0,
            height=66.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: validar_datos(self, controller, "E"),
            relief="flat"
        )
        self.button_2.place(
            x=488.0,
            y=515.0,
            width=306.0,
            height=66.0
        )
        self.label_error = Label(
            self,
            text="",
            bg="#333333",
            fg="red",
            font=("Libre Franklin Bold", 16)
        )
        self.label_error.place(x=800, y=150, width=500, height=30)

    def actualizar(self):
        self.label_error.config(text="", fg="red")
        self.entry_1.delete(0,END)
        self.entry_2.delete(0,END)
        self.entry_3.delete(0,END)
        print("Actualizando Datos")
