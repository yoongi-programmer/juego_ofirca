#!/usr/bin/env python -*- coding: utf-8 -*-
import pygame

pygame.init()
pygame.font.init()
def establecerParametrosGenerales():
    # establecer parametross de la pantalla
    global ancho_pantalla 
    global alto_pantalla
    global pantalla
    global colorFondo
    global anchoBoton, altoBoton
    global anchoBotonuai, altoBotonuai
    global uaibotinoBoton, uaibotinaBoton, uaibotBoton,botaBoton
    global rect_boton1, rect_boton2, rect_boton3, rect_boton4
    
    ancho_pantalla = 1150
    alto_pantalla  = 650
    pantalla       = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    
    pygame.display.set_caption("cambiar de personaje")
    colorFondo                  = (0, 0, 0)  
    anchoBoton, altoBoton       = 100 ,150
    anchoBotonuai, altoBotonuai = 70 ,110
    # Carga las imagenes para los botnoes
    uaibotinoBoton = pygame.image.load("img/assets/UAIBOT.png").convert_alpha()
    uaibotinaBoton = pygame.image.load("img/assets/bota.png").convert_alpha()
    uaibotBoton    = pygame.image.load("img/assets/uaibotino.png").convert_alpha()
    botaBoton      = pygame.image.load("img/assets/uaibotina.png").convert_alpha()
    #redimensiona los botones
    uaibotinoBoton = pygame.transform.scale(uaibotinoBoton, (anchoBoton, altoBoton))
    uaibotinaBoton = pygame.transform.scale(uaibotinaBoton, (anchoBoton, altoBoton))
    uaibotBoton    = pygame.transform.scale(uaibotBoton, (anchoBotonuai, altoBotonuai))
    botaBoton      = pygame.transform.scale(botaBoton, (anchoBoton, altoBoton))
    # Crear espacio pra los botones
    rect_boton1 = uaibotinoBoton.get_rect(topleft=(100, 50))
    rect_boton2 = uaibotinaBoton.get_rect(topleft=(100, 150))
    rect_boton3 = uaibotBoton   .get_rect(topleft=(115, 270))
    rect_boton4 = botaBoton     .get_rect(topleft=(100, 350))

def dibujar_menu():
    pantalla.fill(colorFondo) 
    # Dibujar los botones en la pantalla
    pantalla.blit(uaibotinoBoton, rect_boton1)
    pantalla.blit(uaibotinaBoton, rect_boton2)
    pantalla.blit(uaibotBoton,    rect_boton3)
    pantalla.blit(botaBoton,      rect_boton4)
    pygame.display.flip()

def manejar_clicks(pos):
    global robotElegido
    robotElegido= None
    if rect_boton1.collidepoint(pos):
        print("uaibot papa ")
        robotElegido=1
        return robotElegido
    elif rect_boton2.collidepoint(pos):
        print("bota mama")
        robotElegido=2
        return robotElegido
    elif rect_boton3.collidepoint(pos):
        print("uaibotino hijo ")
        robotElegido=3
        return robotElegido
    elif rect_boton4.collidepoint(pos):
        print("uaibotina hija")
        robotElegido=4
        return robotElegido
    else:
        robotElegido=5
        return robotElegido

def bucle_menu():
    corriendo=True
    while corriendo:
        teclasSubmenu = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                retornoEleccion=manejar_clicks(evento.pos)
                if retornoEleccion <5:
                    # corriendo=False
                    return retornoEleccion
                elif retornoEleccion==5:
                    pass
            elif teclasSubmenu[pygame.K_v]:
                robotElegido = 6
                # corriendo=False
                return robotElegido
        dibujar_menu()
                                 
#        return retornoEleccion
def main():
    establecerParametrosGenerales()
    robotSeleccionado=bucle_menu()

    return robotSeleccionado