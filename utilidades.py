import pygame
import os
import sys

def dibujar_texto(pantalla, texto, fuente, color, x, y):
    texto_superficie = fuente.render(texto, True, color)
    pantalla.blit(texto_superficie, (x, y))

def dibujar_texto_borde(texto, tipografia, color_texto, pos_x, pos_y,pantalla):
        texto_renderizado = tipografia.render(texto, True, color_texto)
        texto_borde = tipografia.render(texto, True, (0, 0, 0))  # Negro para el borde
        # Dibujar el borde del texto en las posiciones ligeramente desplazadas
        pantalla.blit(texto_borde, (pos_x - 1, pos_y))  # Izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y))  # Derecha
        pantalla.blit(texto_borde, (pos_x, pos_y - 1))  # Arriba
        pantalla.blit(texto_borde, (pos_x, pos_y + 1))  # Abajo
        pantalla.blit(texto_borde, (pos_x - 1, pos_y - 1))  # Esquina superior izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y - 1))  # Esquina superior derecha
        pantalla.blit(texto_borde, (pos_x - 1, pos_y + 1))  # Esquina inferior izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y + 1))  # Esquina inferior derecha
        # Dibujar el texto principal sobre el borde
        pantalla.blit(texto_renderizado, (pos_x, pos_y))

def cargar_gif_fondo(ruta_gif,i,restar_caracter,final):
    frames = []
    try:
        #i = 1
        while True:
            ruta_frame = f"{ruta_gif[:-restar_caracter]}{i}{final}" #ejemplo : rutagif1.png(:-5){i}.png
            if os.path.exists(ruta_frame):
                frame = pygame.image.load(ruta_frame).convert()
                frames.append(frame)
                i += 1
            else:
                break
    except Exception as e:
        print(f"No se pudo cargar el GIF: {e}")
        pygame.quit()
        sys.exit()
    return frames