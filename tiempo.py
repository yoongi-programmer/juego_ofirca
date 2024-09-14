import time

class Cronometro:
    def __init__(self):
        self.tiempo_inicio = 0
        self.tiempo_total = 0
        self.transcurriendo = False
        
    def iniciar(self):
        if not self.transcurriendo:
            # Ajusta el tiempoInicio considerando el tiempo ya transcurrido
            self.tiempo_inicio = time.time() - self.tiempo_total
            print(f"tiempo inicio: {self.tiempo_inicio}")
            self.transcurriendo = True
            
    def detener(self):
        if self.transcurriendo:
            # Calcula el tiempo total transcurrido hasta ahora
            self.tiempo_total = time.time() - self.tiempo_inicio
            print(f"tiempo total: {self.tiempo_total}")
            self.transcurriendo = False
            
    def actualizar_tiempo(self):
        if self.transcurriendo:
            tiempo_actual = time.time() - self.tiempo_inicio
            #print(f"tiempo actual: {tiempo_actual}")
            minutos = int(tiempo_actual // 60)
            segundos = int(tiempo_actual % 60)
            milisegundos = int((tiempo_actual * 100) % 100)
            return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}"
        else:
            # Si el cronómetro está detenido, devuelve el tiempo total acumulado
            minutos = int(self.tiempo_total // 60)
            segundos = int(self.tiempo_total % 60)
            milisegundos = int((self.tiempo_total * 100) % 100)
            return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}"
        
class Temporizador:
    def __init__(self):
        self.duracion_inicial = 10  # 75 segundos
        self.tiempo_restante = self.duracion_inicial
        self.tiempo_inicio = 0
        self.tiempo_actual = 0
        self.tiempo_pasado = 0
        self.tiempo_transcurriendo = False
        
    def iniciar(self):
        if not self.tiempo_transcurriendo:
            # Establece el tiempo de inicio considerando el tiempo restante
            self.tiempo_inicio = time.time()
            self.tiempo_transcurriendo = True
            
    def detener(self):
        if self.tiempo_transcurriendo:
            # Calcula el tiempo restante
            tiempo_pasado = time.time() - self.tiempo_inicio
            self.tiempo_restante -= tiempo_pasado
            self.tiempo_transcurriendo = False
            
    def restar_tiempo(self):
        if self.tiempo_transcurriendo:
            # Calcula el tiempo restante durante la cuenta regresiva
            self.tiempo_pasado = time.time() - self.tiempo_inicio
            self.tiempo_actual = self.tiempo_restante - self.tiempo_pasado

            # Si el tiempo llega a 0 o menos, el temporizador se detiene
            if self.tiempo_actual <= 0:
                self.tiempo_restante = 0
                self.tiempo_transcurriendo = False
                return "00", "00", "00"
            else:
                minutos = int(self.tiempo_actual // 60)
                segundos = int(self.tiempo_actual % 60)
                milisegundos = int((self.tiempo_actual * 100) % 100)
                porcentaje= (self.tiempo_actual/self.duracion_inicial)*100

                return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}",f"{int(porcentaje)}"
        else:
            # Devuelve el tiempo restante si el temporizador está detenido
            minutos = int(self.tiempo_restante // 60)
            segundos = int(self.tiempo_restante % 60)
            milisegundos = int((self.tiempo_restante * 100) % 100)
            porcentaje= (self.tiempo_actual/self.duracion_inicial)*100
            return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}",f"{porcentaje:.2f}"

    def reiniciar(self):
        # Restablecer el tiempo a la duración inicial y detener el temporizador
        self.tiempo_restante = self.duracion_inicial
        self.tiempo_transcurriendo = False