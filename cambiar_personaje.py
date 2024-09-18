#!/usr/bin/env python -*- coding: utf-8 -*-
import pygame
pygame.init()
pygame.font.init()

def parametros_generales():
    global ancho_pantalla, alto_pantalla, pantalla, img_fondo
    global bot_btn, bota_btn, botino_btn, botina_btn
    global rect_boton1, rect_boton2, rect_boton3, rect_boton4
    
    ancho_pantalla = 1150
    alto_pantalla = 640
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption("Cambiar de personaje")

    img_fondo = pygame.transform.scale(pygame.image.load("img/fondo_cambiarpersonaje.png").convert_alpha(), (pantalla.get_width(), pantalla.get_height()))

    ancho_btn, alto_btn = 150, 200
    ancho_btn2, alto_btn2 = 200, 250
    ancho_btn3, alto_btn3 = 130, 150
    ancho_btn4, alto_btn4 = 120, 140

    uai_bot_btn = pygame.image.load("img/assets/UAIBOT.png").convert_alpha()
    uai_bota_btn = pygame.image.load("img/assets/bota.png").convert_alpha()
    uai_botino_btn = pygame.image.load("img/assets/uaibotino.png").convert_alpha()
    uai_botina_btn = pygame.image.load("img/assets/uaibotina.png").convert_alpha()

    bot_btn = pygame.transform.scale(uai_bot_btn, (ancho_btn, alto_btn))
    bota_btn = pygame.transform.scale(uai_bota_btn, (ancho_btn2, alto_btn2))
    botino_btn = pygame.transform.scale(uai_botino_btn, (ancho_btn3, alto_btn3))
    botina_btn = pygame.transform.scale(uai_botina_btn, (ancho_btn4, alto_btn4))

    rect_boton1 = bot_btn.get_rect(topleft=(110, 130))
    rect_boton2 = bota_btn.get_rect(topleft=(340, 120))
    rect_boton3 = botino_btn.get_rect(topleft=(635, 180))
    rect_boton4 = botina_btn.get_rect(topleft=(900, 190))

def dibujar_menu():
    pantalla.blit(img_fondo, (0, 0))
    pantalla.blit(bot_btn, rect_boton1)
    pantalla.blit(bota_btn, rect_boton2)
    pantalla.blit(botino_btn, rect_boton3)
    pantalla.blit(botina_btn, rect_boton4)
    pygame.display.flip()

def manejar_clicks(pos):
    # Checkea si el click ocurrió en un botón
    if rect_boton1.collidepoint(pos):
        return 1
    elif rect_boton2.collidepoint(pos):
        return 2
    elif rect_boton3.collidepoint(pos):
        return 3
    elif rect_boton4.collidepoint(pos):
        return 4
    return None  # Si no se hizo clic en ningún botón, retorna None

def manejar_teclas(evento):
    # Detectar la tecla presionada
    if evento.key == pygame.K_1:
        return 1
    elif evento.key == pygame.K_2:
        return 2
    elif evento.key == pygame.K_3:
        return 3
    elif evento.key == pygame.K_4:
        return 4
    return None  # Si no se presionó ninguna tecla válida, retorna None

def bucle_menu():
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None 
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                retorno_eleccion = manejar_clicks(evento.pos)
                if retorno_eleccion is not None:
                    return retorno_eleccion  # Retornar el robot elegido
            elif evento.type == pygame.KEYDOWN:
                retorno_tecla = manejar_teclas(evento)
                if retorno_tecla is not None:
                    return retorno_tecla  # Retornar el robot elegido por la tecla
        
        dibujar_menu()

def main():
    parametros_generales()
    robot_seleccionado = bucle_menu()
    return robot_seleccionado