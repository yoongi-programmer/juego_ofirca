import pygame

class barra_carga_decremental:
    def __init__(self, pantalla, posicion, tamano, color, tiempo_total):
        #inicia la barra de carga
        self.pantalla = pantalla            #param pantalla: Superficie de pygame donde se dibujará la barra de carga.
        self.posicion = posicion            #param posicion: (x, y) posición inicial de la barra en la ventana.
        self.tamano = tamano                # tamaño de la barra.
        self.color = color                  #olor de la barra.
        self.tiempo_total = tiempo_total    #tiempo total en segundos para que la barra se vacíe.
        self.tiempo_restante = tiempo_total
        self.tiempo_inicial = pygame.time.get_ticks()
        self.ancho_inicial = tamano[0]

    def actualizar(self):
        #actualiza el tiempo
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicial) / 1000.0  # Convierte a segundos
        self.tiempo_restante = max(0, self.tiempo_total - tiempo_transcurrido)

        # Calcula el ancho de la barra basado en el tiempo restante
        nuevo_ancho = int(self.ancho_inicial * (self.tiempo_restante / self.tiempo_total))
        self.tamano = (nuevo_ancho, self.tamano[1])

    def dibujar(self):
        pygame.draw.rect(self.pantalla, self.color, (*self.posicion, *self.tamano)) #Dibuja la barra de carga en la pantalla.

    def ha_terminado(self):
        return self.tiempo_restante <= 0 #Verifica si la barra de carga ha terminado.
