#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys

pygame.init()

# Configuración de la pantalla

ancho_pantalla = 800
alto_pantalla = 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Ventana con Botones Clickeables")


colorFondo = (0, 0, 0)  
anchoBoton, altoBoton= 100 ,150
anchoBotonuai, altoBotonuai= 70 ,110

# Carga las imagenes para los botnoes
uaibotinoBoton = pygame.image.load("uaibotino.png").convert_alpha()
uaibotinaBoton = pygame.image.load("uaibotina.png").convert_alpha()
uaibotBoton = pygame.image.load("UAIBOT.png").convert_alpha()
botaBoton = pygame.image.load("bota.png").convert_alpha()

#redimensiona los botones
uaibotinoBoton = pygame.transform.scale(uaibotinoBoton, (anchoBoton, altoBoton))
uaibotinaBoton = pygame.transform.scale(uaibotinaBoton, (anchoBoton, altoBoton))
uaibotBoton = pygame.transform.scale(uaibotBoton, (anchoBotonuai, altoBotonuai))
botaBoton = pygame.transform.scale(botaBoton, (anchoBoton, altoBoton))

# Crear espacio pra los botones
rect_boton1 = uaibotinoBoton.get_rect(topleft=(100, 50))
rect_boton2 = uaibotinaBoton.get_rect(topleft=(100, 150))
rect_boton3 = uaibotBoton   .get_rect(topleft=(100, 270))
rect_boton4 = botaBoton     .get_rect(topleft=(100, 350))

def dibujar_menu():
    pantalla.fill(colorFondo)  # Rellena el fondo con color negro

    # Dibujar los botones en la pantalla
    pantalla.blit(uaibotinoBoton, rect_boton1)
    pantalla.blit(uaibotinaBoton, rect_boton2)
    pantalla.blit(uaibotBoton,    rect_boton3)
    pantalla.blit(botaBoton,      rect_boton4)

    pygame.display.flip()

def manejar_clicks(pos):
    if rect_boton1.collidepoint(pos):
        print("Botón 1 clickeado")
        return 1
    elif rect_boton2.collidepoint(pos):
        print("Botón 2 clickeado")
        return 2
    elif rect_boton3.collidepoint(pos):
        print("Botón 3 clickeado")
        return 3
    elif rect_boton4.collidepoint(pos):
        print("Botón 4 clickeado")
        return 4

# Bucle principal
def bucle_menu():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                manejar_clicks(evento.pos)

        dibujar_menu()
        pygame.time.Clock().tick(60)  # Limita a 60 FPS

bucle_menu()
