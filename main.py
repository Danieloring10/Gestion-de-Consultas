from gestor import GestorPantallas
from pantallas.clases import Estudiante, Horario, Profesor, Consulta
import datetime

class Sistema:
    def __init__(self):
        self.estudiantes = []
        self.profesores = []
        self.inicializar_datos()

    def agregar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def agregar_profesor(self, profesor):
        self.profesores.append(profesor)

    def autenticar_usuario(self, identificador, rol):
        if rol == "E":
            for estudiante in self.estudiantes:
                if estudiante.matricula == identificador:
                    return estudiante
        elif rol == "P":
            for profesor in self.profesores:
                if profesor.id_profesor == identificador:
                    return profesor
        return None
    def inicializar_datos(self):
   
    
    # Crear instancias de Profesores
        profesor1 = Profesor(
            nombre="Dr. Luis García",
            email="luis.garcia@uni.edu",
            contrasenia="1234",
            id_profesor=101456
        )
        profesor2 = Profesor(
            nombre="Dra. Marta Sánchez",
            email="marta.sanchez@uni.edu",
            contrasenia="5678",
            id_profesor=102456
        )

        # Crear instancias de Alumnos
        alumno1 = Estudiante(
            nombre="Juan Pérez",
            email="juan.perez@uni.edu",
            contrasenia="1234",
            matricula=202345
        )
        alumno2 = Estudiante(
            nombre="Ana López",
            email="ana.lopez@uni.edu",
            contrasenia="5678",
            matricula=202346
        )

        # Agregar los profesores y alumnos al sistema
        self.agregar_profesor(profesor1)
        self.agregar_profesor(profesor2)
        self.agregar_estudiante(alumno1)
        self.agregar_estudiante(alumno2)

        # Crear instancias de Horarios para los profesores
        horario1 = Horario(fecha=datetime.date(2024, 12, 1), rango_inicio=datetime.time(9, 0), rango_fin=datetime.time(11, 0))
        horario2 = Horario(fecha=datetime.date(2024, 12, 1), rango_inicio=datetime.time(11, 0), rango_fin=datetime.time(13, 0))
        horario3 = Horario(fecha=datetime.date(2024, 12, 2), rango_inicio=datetime.time(10, 0), rango_fin=datetime.time(12, 0))

        # Asignar horarios a los profesores
        profesor1.horarios.extend([horario1, horario2])
        profesor2.horarios.append(horario3)

        # Crear instancias de Consultas
        consulta1 = Consulta(
            hora_inicio=datetime.time(9, 0),
            fecha=datetime.date(2024, 12, 1),
            duracion_minutos=30,
            estado="En espera",
            estudiante=alumno1,
            profesor=profesor1
        )
        consulta2 = Consulta(
            hora_inicio=datetime.time(10, 0),
            fecha=datetime.date(2024, 12, 1),
            duracion_minutos=30,
            estado="En espera",
            estudiante=alumno2,
            profesor=profesor1
        )
        consulta3 = Consulta(
            hora_inicio=datetime.time(11, 0),
            fecha=datetime.date(2024, 12, 2),
            duracion_minutos=30,
            estado="En espera",
            estudiante=alumno1,
            profesor=profesor2
        )

        # Asignar consultas a estudiantes y profesores
        alumno1.consultas.extend([consulta1, consulta3])
        alumno2.consultas.append(consulta2)
        profesor1.solicitudes.extend([consulta1, consulta2])
        profesor2.solicitudes.append(consulta3)

        print("Datos inicializados con éxito.")


if __name__ == "__main__":
    sistema = Sistema()

    app = GestorPantallas(sistema)
    app.mainloop()
