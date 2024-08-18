import time

class cronometro:
    def __init__(self):
        self.tiempoInicio   =0
        self.tiempoTotal    =0
        self.transcurriendo =False
        
    def iniciar(self):
        if not self.transcurriendo:
            self.tiempoInicio = time.time() - self.tiempoTotal
            self.transcurriendo = True
    def detener(self):
        if self.transcurriendo:
            self.tiempoInicio = time.time() - self.tiempoInicio
            self.transcurriendo = False
    def actualizar_tiempo(self):
        if self.transcurriendo:
            tiempo_actual = time.time() - self.tiempoInicio
            minutos = int(tiempo_actual // 60)
            segundos = int(tiempo_actual % 60)
            milisegundos = int((tiempo_actual * 100) % 100)
            return minutos, segundos, milisegundos
        return 0,0,0
    
def main():
    
    miCronometro=cronometro()
    miCronometro.iniciar()   
    try:         
        while True:
            minuts,seconds,miliseconds=miCronometro.actualizar_tiempo()
            print(f"\r{minuts:02}:{seconds:02}:{miliseconds:02}",end="")
            if seconds==10:
                tiempoTotal=[minuts,seconds,miliseconds]
                miCronometro.detener()
                print('\nEl tiempo fue de',tiempoTotal[0],':',tiempoTotal[1],':',tiempoTotal[2])
                exit()
    except KeyboardInterrupt:
        print("se detuvo")
main()
                