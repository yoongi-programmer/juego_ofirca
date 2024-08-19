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
            self.transcurriendo = True
            
    def detener(self):
        if self.transcurriendo:
            # Calcula el tiempo total transcurrido hasta ahora
            self.tiempo_total = time.time() - self.tiempo_inicio
            self.transcurriendo = False
            
    def actualizar_tiempo(self):
        if self.transcurriendo:
            tiempo_actual = time.time() - self.tiempo_inicio
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