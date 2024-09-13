import pygame
import os

def extraer_mejores_marcas(ruta_nombres, ruta_tiempos, num_mejores=5):
    """
    Extrae las mejores marcas desde los archivos y las devuelve ordenadas.
    """
    # Leer los archivos
    nombres = archivosLectores(ruta_nombres)
    tiempos = archivosLectores(ruta_tiempos)
    
    # Crear una lista de tuplas (nombre, tiempo) y ordenar por tiempo (convertido a float)
    marcas = list(zip(nombres, map(float, tiempos)))
    marcas_ordenadas = sorted(marcas, key=lambda x: x[1])  # Ordenar por tiempo ascendente

    # Devolver las mejores marcas
    return marcas_ordenadas[:num_mejores]

def mostrar_mejores_marcas(pantalla, mejores_marcas):
    """
    Muestra las mejores marcas en una ventana de Pygame.
    """
    ancho_pantalla, alto_pantalla = 400, 400
    fuente = pygame.font.SysFont('Arial', 24)
    pantalla.fill((0, 0, 0))  # Fondo negro

    # Título
    titulo_texto = fuente.render("Mejores Marcas", True, (255, 255, 255))
    pantalla.blit(titulo_texto, (ancho_pantalla // 2 - titulo_texto.get_width() // 2, 20))

    # Mostrar las mejores marcas
    for i, (nombre, tiempo) in enumerate(mejores_marcas):
        texto = f"{i + 1}. {nombre}: {tiempo:.2f}s"
        texto_renderizado = fuente.render(texto, True, (255, 255, 255))
        pantalla.blit(texto_renderizado, (20, 60 + i * 30))

    pygame.display.flip()  # Actualizar pantalla

def main():
    pygame.init()
    pygame.font.init()

    # Ruta de los archivos
    carpeta = "archivos"
    ruta_nombres = os.path.join(carpeta, "nombres.txt")
    ruta_tiempos = os.path.join(carpeta, "tiempos.txt")
    
    # Crear la ventana
    pantalla = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Mejores Marcas")

    # Obtener las mejores marcas
    mejores_marcas = extraer_mejores_marcas(ruta_nombres, ruta_tiempos)
    
    # Mostrar las mejores marcas en la ventana
    mostrar_mejores_marcas(pantalla, mejores_marcas)

    # Mantener la ventana abierta
    corriendo = True
    while corriendo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

    pygame.quit()

def archivosLectores(archivo):
    archivo = open(archivo,"r")
    contenido=[linea.strip() for linea in archivo]
    archivo.close()
    return contenido

main()
