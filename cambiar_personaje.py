#!/usr/bin/env python -*- coding: utf-8 -*-
import pygame
pygame.init()
pygame.font.init()

def parametros_generales():
    # establecer parametross de la pantalla
    global ancho_pantalla 
    global alto_pantalla
    global pantalla
    global img_fondo
    global bot_btn, bota_btn, botino_btn,botina_btn
    global rect_boton1, rect_boton2, rect_boton3, rect_boton4
    
    ancho_pantalla = 1150
    alto_pantalla  = 640
    pantalla       = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    
    pygame.display.set_caption("cambiar de personaje")
    img_fondo = pygame.transform.scale(pygame.image.load("img/fondo_cambiarpersonaje.png").convert_alpha(), (pantalla.get_width(), pantalla.get_height()))
    ancho_btn, alto_btn = 150 ,200
    ancho_btn2, alto_btn2 = 200,250
    ancho_btn3, alto_btn3 = 130,150
    ancho_btn4, alto_btn4 = 120,140

    # Carga las imagenes para los botnoes
    uai_bot_btn = pygame.image.load("img/assets/UAIBOT.png").convert_alpha()
    uai_bota_btn = pygame.image.load("img/assets/bota.png").convert_alpha()
    uai_botino_btn = pygame.image.load("img/assets/uaibotino.png").convert_alpha()
    uai_botina_btn = pygame.image.load("img/assets/uaibotina.png").convert_alpha()
    #redimensiona los botones
    bot_btn    = pygame.transform.scale(uai_bot_btn, (ancho_btn, alto_btn))
    bota_btn      = pygame.transform.scale(uai_bota_btn, (ancho_btn2, alto_btn2))
    botino_btn = pygame.transform.scale(uai_botino_btn, (ancho_btn3, alto_btn3))
    botina_btn = pygame.transform.scale(uai_botina_btn, (ancho_btn4, alto_btn4))    
    # Crear espacio pra los botones
    rect_boton1 = bot_btn.get_rect(topleft=(110, 130))
    rect_boton2 = bota_btn.get_rect(topleft=(340, 120))
    rect_boton3 = botino_btn.get_rect(topleft=(635, 180))
    rect_boton4 = botina_btn.get_rect(topleft=(900, 190))

def dibujar_menu():
    pantalla.blit(img_fondo,(0,0))
    # Dibujar los botones en la pantalla
    pantalla.blit(bot_btn, rect_boton1)
    pantalla.blit(bota_btn, rect_boton2)
    pantalla.blit(botino_btn, rect_boton3)
    pantalla.blit(botina_btn, rect_boton4)
    pygame.display.flip()

def manejar_clicks(pos):
    global robot_elegido
    robot_elegido = None
    if rect_boton1.collidepoint(pos):
        print("uaibot papa ")
        robot_elegido=1
        return robot_elegido
    elif rect_boton2.collidepoint(pos):
        print("bota mama")
        robot_elegido=2
        return robot_elegido
    elif rect_boton3.collidepoint(pos):
        print("uaibotino hijo ")
        robot_elegido=3
        return robot_elegido
    elif rect_boton4.collidepoint(pos):
        print("uaibotina hija")
        robot_elegido=4
        return robot_elegido
    else:
        robot_elegido=5
        return robot_elegido

def bucle_menu():
    corriendo=True
    while corriendo:
        teclas_submenu = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                retorno_eleccion=manejar_clicks(evento.pos)
                if retorno_eleccion <5:
                    return retorno_eleccion
                elif retorno_eleccion==5:
                    pass
            elif teclas_submenu[pygame.K_v]:
                robot_elegido = 6
                return robot_elegido
        dibujar_menu()

def main():
    parametros_generales()
    robot_seleccionado=bucle_menu()
    return robot_seleccionado