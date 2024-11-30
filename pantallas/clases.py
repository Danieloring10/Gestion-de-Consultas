from datetime import datetime, timedelta

class Usuario:
    def __init__(self, nombre, email, contrasenia):
        self.nombre = nombre
        self.email = email
        self.contrasenia = contrasenia


class Estudiante(Usuario):
    def __init__(self, nombre, email, contrasenia, matricula):
        super().__init__(nombre, email, contrasenia)
        self.matricula = matricula
        self.consultas = []

    #Aquí se requerira que el sistema abra la venta de Horarios (pantalla5) y se le enviaran las clases de "Horarios" de los profesores
    def ver_horarios_disponibles(self, sistema):
        print("Horarios disponibles de todos los profesores:")
        for profesor in sistema.profesores:
            print(f"\nProfesor: {profesor.nombre}")
            if profesor.horarios:
                for horario in profesor.horarios:
                    print(f"  - {horario}")
            else:
                print("  No hay horarios disponibles.")
        print()

    
    # Esto generara una nueva instancia de "Consulta" obteniendo los datos insertados en la pantalla previamente validados
    
    def solicitar_consulta(self, profesor, horario, duracion):
        inicio = horario.rango_inicio
        consulta = Consulta(
            hora_inicio=inicio,
            fecha=horario.fecha,
            duracion_minutos=duracion,
            estado="Pendiente",
            estudiante=self,
            profesor=profesor
        )
        self.consultas.append(consulta)
        profesor.solicitudes.append(consulta)
        print(f"Consulta solicitada para {horario.fecha} a las {inicio} por {duracion} minutos.")

    # Aquí se requiere que el sistema abra la ventana Consultas(Pantalla 4) y muestre todas las consultas asociadas al alumno

    def ver_estado_consultas(self):
        print("Estado de tus consultas:")
        for i, consulta in enumerate(self.consultas):
            print(f"{i + 1}. {consulta}")
        print("¿Deseas eliminar alguna consulta? (s/n)")
        if input().lower() == 's':
            idx = int(input("Número de la consulta a eliminar: ")) - 1
            self.consultas.pop(idx)
            print("Consulta eliminada.")

    # Falto la función cancelarConsulta, dentro de la ventana "Consulta"(Pantalla 5) en donde eliminara la instancia y se actualizaran los horarios

class Profesor(Usuario):
    def __init__(self, nombre, email, contrasenia, id_profesor):
        super().__init__(nombre, email, contrasenia)
        self.id_profesor = id_profesor
        self.horarios = []
        self.solicitudes = []

    # Aquí la ventana GestionarConsultas(Pantalla6) se abrira, mostrara las consultas asociadas al profesor y los 3 botones cambiaran el "estado" de la consulta
    # Dependiendo de la selección dentro de la tabla se mostrara el texto de lado derecho

    def gestionar_solicitudes(self):
        print("Solicitudes de consulta:")
        for i, consulta in enumerate(self.solicitudes):
            print(f"{i + 1}. {consulta}")
        idx = int(input("Número de la consulta a aceptar/rechazar: ")) - 1
        consulta = self.solicitudes[idx]
        print("¿Aceptar (a) o Rechazar (r)?")
        accion = input().lower()
        if accion == 'a':
            consulta.cambiar_estado("Confirmada")
            self.actualizar_disponibilidad(consulta)
            print("Consulta confirmada.")
        elif accion == 'r':
            consulta.cambiar_estado("Rechazada")
            print("Consulta rechazada.")

    # Aquí se mosstrara la pantalla "Disponabilidad"(pantalla7) que muesrta los horarios asociados al profesor
    # El profesor podra eliminar un horario, o crear una nueva instancia, a la hora de eliminar un horario todas las consultas asociadas al horario se pondran automaticamente en estado "negada"

    def actualizar_disponibilidad(self, consulta):
        for horario in self.horarios:
            if horario.fecha == consulta.fecha and horario.rango_inicio <= consulta.hora_inicio < horario.rango_fin:
                horario.modificar_rango(consulta.hora_inicio, consulta.duracion_minutos)


    def agregar_horario(self):
        fecha = input("Fecha del horario disponible (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            rango_inicio = input("Hora de inicio (HH:MM en formato 24 horas): ")
            rango_inicio = datetime.strptime(rango_inicio, "%H:%M").time()
            rango_fin = input("Hora de fin (HH:MM en formato 24 horas): ")
            rango_fin = datetime.strptime(rango_fin, "%H:%M").time()
            if rango_inicio >= rango_fin:
                print("El rango de inicio debe ser menor que el rango de fin.")
                return
            horario = Horario(fecha, rango_inicio, rango_fin)
            self.horarios.append(horario)
            print("Horario agregado correctamente.")
        except ValueError:
            print("Formato incorrecto. Asegúrate de usar los formatos indicados.")


class Horario:
    def __init__(self, fecha, rango_inicio, rango_fin):
        self.fecha = fecha
        self.rango_inicio = rango_inicio
        self.rango_fin = rango_fin

    def modificar_rango(self, hora_inicio, duracion_minutos):
        inicio = (datetime.combine(self.fecha, hora_inicio) + timedelta(minutes=duracion_minutos)).time()
        self.rango_inicio = inicio

    def __str__(self):
        return f"{self.fecha} de {self.rango_inicio} a {self.rango_fin}"


class Consulta:
    def __init__(self, hora_inicio, fecha, duracion_minutos, estado, estudiante, profesor):
        self.hora_inicio = hora_inicio
        self.fecha = fecha
        self.duracion_minutos = duracion_minutos
        self.estado = estado
        self.estudiante = estudiante
        self.profesor = profesor

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return f"{self.fecha} a las {self.hora_inicio}, Duración: {self.duracion_minutos} min, Estado: {self.estado}"


class Sistema:
    def __init__(self):
        self.estudiantes = []
        self.profesores = []

    def agregar_estudiante(self, estudiante):
        self.estudiantes.append(estudiante)

    def agregar_profesor(self, profesor):
        self.profesores.append(profesor)


if __name__ == "__main__":
    sistema = Sistema()

  