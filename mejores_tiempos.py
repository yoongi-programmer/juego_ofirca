import pygame
import os
from utilidades import dibujar_texto,dibujar_texto_borde
def convertir_a_segundos(tiempo_str):
    #Convierte un string en formato HH:MM:SS a segundos.
    partes = tiempo_str.split(':')  # Divide la cadena en horas, minutos y segundos
    horas = int(partes[0])
    minutos = int(partes[1])
    segundos = int(partes[2])
    
    # Convertir todo a segundos
    total_segundos = horas * 3600 + minutos * 60 + segundos
    return total_segundos

def extraer_mejores_marcas(ruta_nombres, ruta_tiempos, num_mejores=10):
    #Extrae las mejores marcas desde los archivos y las devuelve ordenadas.
    nombres = archivos_lectores(ruta_nombres)
    tiempos = archivos_lectores(ruta_tiempos)
    
    # Crear una lista de tuplas (nombre, tiempo en segundos)
    marcas = []
    for nombre, tiempo in zip(nombres, tiempos):
        try:
            tiempo_segundos = convertir_a_segundos(tiempo)  # Convertir HH:MM:SS a segundos
            marcas.append((nombre, tiempo_segundos))
        except ValueError:
            print(f"Advertencia: No se pudo convertir '{tiempo}' a segundos. Se omitirá.")
    
    # Ordenar por tiempo en segundos (ascendente)
    marcas_ordenadas = sorted(marcas, key=lambda x: x[1],reverse=True)

    # Devolver las mejores 10 marcas (o las que estén disponibles)
    return marcas_ordenadas[:num_mejores]

def mostrar_mejores_marcas(pantalla, mejores_marcas):
    #Muestra las mejores marcas en una ventana de Pygame.
    fuente_title = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 55)
    fuente = pygame.font.Font("fonts/depixel/DePixelBreit.ttf", 20)
    fondo = pygame.transform.scale(pygame.image.load("img/fondo_puntaje.png").convert_alpha(),(pantalla.get_width(),pantalla.get_height()))
    global boton_volver
    boton_volver = pygame.transform.scale(pygame.image.load('img/boton.png').convert_alpha(), (220, 85))
    pantalla.blit(fondo,(0,0))
    pantalla.blit(boton_volver,(500,540))
    # Título
    dibujar_texto_borde("Mejores marcas",fuente_title,(255,255,255),330,12,pantalla)
    dibujar_texto(pantalla,"Ranking",fuente,(197,57,178),210,130)
    dibujar_texto(pantalla,"Nombre",fuente,(112,251,251),380,130)
    dibujar_texto(pantalla,"Tiempo",fuente,(50,202,68),590,130)
    dibujar_texto(pantalla,"Puntaje",fuente,(255,252,164),800,130)
    #  Mostrar las mejores marcas
    for i, (nombre, tiempo) in enumerate(mejores_marcas):
        # Convertir de nuevo a formato HH:MM:SS para mostrarlo
        horas = int(tiempo // 3600)
        minutos = int((tiempo % 3600) // 60)
        segundos = int(tiempo % 60)
        print(f"{horas}, {minutos},{segundos}")
        tiempo_formateado = f"{horas:02}:{minutos:02}:{segundos:02}"
        texto = f"{i + 1:<16} {nombre:<20} {tiempo_formateado:<15}"
        texto_renderizado = fuente.render(texto, True, (255, 255, 255))
        pantalla.blit(texto_renderizado, (210, 180 + i * 35))

    pygame.display.flip()  # Actualizar pantalla

def main():
    pygame.init()
    pygame.font.init()
    print("main de mostrar  mejores marcas")

    # Ruta de los archivos
    carpeta = "archivos"
    ruta_nombres = os.path.join(carpeta, "nombres.txt")
    ruta_tiempos = os.path.join(carpeta, "tiempos.txt")
    
    # Crear la ventana
    pantalla = pygame.display.set_mode((1150, 640))
    pygame.display.set_caption("Mejores Marcas")

    # Obtener las mejores marcas (máximo 10)
    mejores_marcas = extraer_mejores_marcas(ruta_nombres, ruta_tiempos, num_mejores=10)
    
    # Mostrar las mejores marcas en la ventana
    mostrar_mejores_marcas(pantalla, mejores_marcas)

    # Mantener la ventana abierta
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(event.pos):
                    corriendo = False
                    return "volver"


    pygame.quit()

def archivos_lectores(archivo):
    #Lee un archivo de texto y devuelve su contenido como una lista de líneas.
    with open(archivo, "r") as f:
        contenido = [linea.strip() for linea in f]
    return contenido