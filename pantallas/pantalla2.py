from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Pantalla2(Frame): 
    def __init__(self, parent, controller, sistema): 
        Frame.__init__(self, parent)
        self.controller = controller
        self.sistema = sistema 
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
            text="Menu",
            fill="#FFFFFF",
            font=("Libre Franklin Bold", 64 * -1)
        )

        self.canvas.create_rectangle(
            707.0,
            163.0,
            1214.0,
            413.0,
            fill="#D9D9D9",
            outline="")

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla1"),
            relief="flat"
        )
        self.button_1.place(
            x=993.0,
            y=28.0,
            width=275.0,
            height=78.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla7"),
            relief="flat"
        )
        self.button_2.place(
            x=48.0,
            y=164.0,
            width=550.0,
            height=92.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.mostrar_pantalla("Pantalla6"),
            relief="flat"
        )
        self.button_3.place(
            x=48.0,
            y=290.0,
            width=550.0,
            height=92.0
        )

        self.canvas.create_text(
            741.0,
            181.0,
            anchor="nw",
            text="Profesor",
            fill="#000000",
            font=("Libre Franklin Bold", 64 * -1)
        ) 
        self.text_usuario = self.canvas.create_text(
                735.0,
                268.0,
                anchor="nw",
                text="",
                fill="#000000",
                font=("Libre Franklin Bold", 36 * -1)
            )
        
            
    def actualizar(self): 
        print("Actualizando Datos")
        usuario = self.controller.usuario_actual 
        if usuario: 
            self.canvas.itemconfig(self.text_usuario, text=f"{usuario.nombre}")