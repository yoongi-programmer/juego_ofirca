import time

class cronometro:
    def __init__(self):
        self.tiempoInicio = 0
        self.tiempoTotal = 0
        self.transcurriendo = False
        
    def iniciar(self):
        if not self.transcurriendo:
            # Ajusta el tiempoInicio considerando el tiempo ya transcurrido
            self.tiempoInicio = time.time() - self.tiempoTotal
            self.transcurriendo = True
            
    def detener(self):
        if self.transcurriendo:
            # Calcula el tiempo total transcurrido hasta ahora
            self.tiempoTotal = time.time() - self.tiempoInicio
            self.transcurriendo = False
            
    def actualizar_tiempo(self):
        if self.transcurriendo:
            tiempo_actual = time.time() - self.tiempoInicio
            minutos = int(tiempo_actual // 60)
            segundos = int(tiempo_actual % 60)
            milisegundos = int((tiempo_actual * 100) % 100)
            return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}"
        else:
            # Si el cronómetro está detenido, devuelve el tiempo total acumulado
            minutos = int(self.tiempoTotal // 60)
            segundos = int(self.tiempoTotal % 60)
            milisegundos = int((self.tiempoTotal * 100) % 100)
            return f"{minutos:02}", f"{segundos:02}", f"{milisegundos:02}"
