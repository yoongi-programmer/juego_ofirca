import pygame
import sys
from utilidades import dibujar_texto, cargar_gif_fondo
from menu_inicio import MenuInicio

class MenuPausa:
    def __init__(self, pantalla, menu_inicio):
        self.pantalla = pantalla
        self.frames = cargar_gif_fondo("img/menu_pausa/frame_0.png")
        self.frame_actual = 0
        self.retraso_animacion = 5  # Milisegundos entre frames
        self.ultimo_cambio = pygame.time.get_ticks()
        self.menu_inicio = menu_inicio  # Guardar referencia de la instancia del menú de inicio

    def mostrar_menu(self):
        fuente_title = pygame.font.Font("fonts/steiner2/Steiner.otf", 80)
        fuente = pygame.font.Font("fonts/monocode/Monocode.ttf", 32)
        color_blanco = (255, 255, 255)
        pos_title = (440, 100)
        pos_btn1 = (455, 280)
        pos_btn2 = (495, 357)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Salir del menú y reanudar el juego
                    if event.key == pygame.K_q:
                        # Volver al menú de inicio
                        self.menu_inicio.bucle_principal()  # Llama al menú de inicio
                        return  # Salir del menú de pausa

            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_cambio > self.retraso_animacion:
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                self.ultimo_cambio = ahora

            self.pantalla.blit(self.frames[self.frame_actual], (0, 0))

            # Dibujar los botones
            rect_reanudar = pygame.Rect(430, 270, 370, 50)  ## x, y, ancho, alto
            rect_salir = pygame.Rect(430, 345, 370, 50)
            pygame.draw.rect(self.pantalla, color_blanco, rect_reanudar, width=3)
            pygame.draw.rect(self.pantalla, color_blanco, rect_salir, width=3)
            dibujar_texto(self.pantalla, "PAUSA", fuente_title, color_blanco, pos_title[0], pos_title[1])
            dibujar_texto(self.pantalla, "ESC para reanudar", fuente, color_blanco, pos_btn1[0], pos_btn1[1])
            dibujar_texto(self.pantalla, "Q para volver al menú", fuente, color_blanco, pos_btn2[0], pos_btn2[1])
            pygame.display.flip()
