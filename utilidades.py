import pygame
import os
import sys

def dibujar_texto(pantalla, texto, fuente, color, x, y):
    texto_superficie = fuente.render(texto, True, color)
    pantalla.blit(texto_superficie, (x, y))

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