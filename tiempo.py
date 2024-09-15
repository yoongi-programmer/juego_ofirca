import time
        
class Temporizador:
    def __init__(self):
        self.duracion_inicial = 70  # 75 segundos
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
                return "00", "00", "00","0"
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