import pygame
from utilidades import dibujar_texto, cargar_gif_fondo
pygame.init()

class MenuInicio:
    def __init__(self):
        print("Dibujando pantalla de menu inicio")
        self.pantalla = pygame.display.set_mode((1150, 640))
        pygame.display.set_caption("Pantalla de Inicio del Juego")

        # Variables para los botones
        self.boton_empezar = pygame.Rect(190, 247, 300, 50)
        self.boton_informacion = pygame.Rect(190, 349, 300, 50)
        self.boton_salir = pygame.Rect(190, 449, 300, 50)
        # Cargar frames del GIF
        self.frames = cargar_gif_fondo("img/menu_inicio/gif0.png")
        self.frame_actual = 0
        # Fuentes y colores
        self.fuente_title = pygame.font.Font("fonts/steiner2/Steiner.otf", 80)
        self.fuente = pygame.font.Font("fonts/monocode/Monocode.ttf", 36)
        self.color_blanco = (255, 255, 255)
        self.pos_title = (125, 100)
        self.pos_btn1 = (285, 255)
        self.pos_btn2 = (220, 357)
        self.pos_btn3 = (285, 457)

    def bucle_principal(self):
        reloj = pygame.time.Clock()
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_empezar.collidepoint(evento.pos):
                        return "jugar"  # Indicamos que el jugador quiere empezar
                    elif self.boton_informacion.collidepoint(evento.pos):
                        self.mostrar_informacion()
                    elif self.boton_salir.collidepoint(evento.pos):
                        return "salir"  # Indicamos que el jugador quiere salir

            self.pantalla.fill((0, 0, 0))
            # Actualizar frame del GIF
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.pantalla.blit(self.frames[self.frame_actual], (0, 0))

            # Dibujar texto y botones
            dibujar_texto(self.pantalla, "START GAME", self.fuente_title, self.color_blanco, self.pos_title[0], self.pos_title[1])
            pygame.draw.rect(self.pantalla, self.color_blanco, self.boton_empezar, width=3)
            pygame.draw.rect(self.pantalla, self.color_blanco, self.boton_informacion, width=3)
            pygame.draw.rect(self.pantalla, self.color_blanco, self.boton_salir, width=3)
            dibujar_texto(self.pantalla, "Jugar", self.fuente, self.color_blanco, self.pos_btn1[0], self.pos_btn1[1])
            dibujar_texto(self.pantalla, "Informacion", self.fuente, self.color_blanco, self.pos_btn2[0], self.pos_btn2[1])
            dibujar_texto(self.pantalla, "Salir", self.fuente, self.color_blanco, self.pos_btn3[0], self.pos_btn3[1])

            pygame.display.flip()
            reloj.tick(10)
        pygame.quit()
        return "salir"

    def mostrar_informacion(self):
        # Cargar frames del GIF
        frames_info = cargar_gif_fondo("img/instrucciones/frame0.png")
        frame_actual = 0
        self.fuente_title = pygame.font.Font("fonts/steiner2/Steiner.otf", 75)

        # Dibujar las instrucciones
        titulo = "Instrucciones"
        boton_volver = pygame.Rect(200, 570, 200, 50)

        corriendo = True
        reloj = pygame.time.Clock()
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        corriendo = False  # Volver al menú principal

            # Actualizar frame del GIF
            frame_actual = (frame_actual + 1) % len(frames_info)
            # Dibujar fondo, título y el boton para volver
            self.pantalla.blit(frames_info[frame_actual], (0, 0))
            dibujar_texto(self.pantalla, titulo, self.fuente_title, self.color_blanco, 300, 15)
            pygame.draw.rect(self.pantalla, self.color_blanco, boton_volver, width=3)
            dibujar_texto(self.pantalla, "Volver", self.fuente, self.color_blanco, 235, 580)

            pygame.display.flip()
            reloj.tick(0.5)  # Ajustar la velocidad de animación