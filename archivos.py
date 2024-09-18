import pygame
import os
import mejores_tiempos

def creacion_comprobacion():
    global tiempos, nombres 
    global ruta_nombres, ruta_tiempos
    
    carpeta = "archivos"
    nombres_archivo = "nombres.txt"
    tiempos_archivo = "tiempos.txt" 
    ruta_nombres = os.path.join(carpeta, nombres_archivo)
    ruta_tiempos = os.path.join(carpeta, tiempos_archivo) 
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print("La carpeta no existia y fue creada")
    else:
        print("La carpeta existe") 
    if not os.path.exists(ruta_nombres):
        nombres=open(ruta_nombres, 'x')
        nombres.close()
        print("El archivo nombres fue creado en su respectiva carpeta ")
    else:
        print("El archivo nombres ya existe en la carpeta")    
    if not os.path.exists(ruta_tiempos):
         tiempos=open(ruta_tiempos, 'x')
         tiempos.close()
         print("El archivo tiempos fue creado en su respectiva carpeta ")
    else:
         print("El archivo tiempos ya existe en la carpeta")

def carga_datos(nombre_guardar, marca_guardar):
        
    tiempos = open(ruta_tiempos, 'a')
    nombres = open(ruta_nombres, 'a')
    tiempos.write(str(marca_guardar) + '\n')
    nombres.write(str(nombre_guardar) + '\n')
    print("Carga exitosa")
    tiempos.close()
    nombres.close()

def mostrar_datos():
    tiempos_listado = archivos_lectores(ruta_tiempos)
    nombres_listado = archivos_lectores(ruta_nombres)
    rachas = list(zip(nombres_listado, tiempos_listado))
    for nombres, tiempos in rachas:
        print(f"{nombres} {tiempos}")

def modificador(archivo_modificar, nueva_marca, nombres_lista, marcas_lista, nombre_jugador):
    archivo = open(archivo_modificar, "w")
    posicion = nombres_lista.index(nombre_jugador)
    print(posicion)
    marcas_lista[posicion-1] = nueva_marca
    for elemento in marcas_lista:
        archivo.write(str(elemento) + "\n")#reecribir la nueva marca
    archivo.close()

def archivos_lectores(archivo):
    archivo = open(archivo, "r")
    contenido = [linea.strip() for linea in archivo]
    archivo.close()
    return contenido

def main(nombre, marca,pantalla):
    print("Entro al main de archivos")
    print(f"{nombre},{marca}")
    creacion_comprobacion()
    print("Se comprobaron y se crearon correctamente")
    
    nombres_listado = archivos_lectores(ruta_nombres)
    tiempos_listado = archivos_lectores(ruta_tiempos)
    
    
    if nombre in nombres_listado:
        posicion = nombres_listado.index(nombre)
        print("la posicion es: ",posicion)
        tamañoMarcas=len(tiempos_listado)
        print("el tamaño de la lista es de:",tamañoMarcas)
        posicion_marca=tiempos_listado[posicion-1]
        marca_guardada_casteada=mejores_tiempos.convertir_a_segundos(posicion_marca)
        marca_hecha_casteada=mejores_tiempos.convertir_a_segundos(marca)
        
        #print(f'{marca,tiempos_listado[posicion],nombres_listado[posicion]}')
        if marca_hecha_casteada>marca_guardada_casteada:
            print("entro al sobreescribir")
            corriendo = True
            ancho_pantalla, alto_pantalla =874, 521
            ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
            pygame.display.set_caption("Guardar partida")

            fondo_guardar = pygame.transform.scale(pygame.image.load("img/sobre_escribir.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
            ventana.blit(fondo_guardar, (0, 0))
            pos_x = 150
            pos_y = 150
            pantalla.blit(ventana, (pos_x, pos_y))

            while corriendo:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        corriendo = False
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_s:
                            # Aquí agregas lo que quieras hacer cuando se presiona 's'
                            print("Tecla 's' presionada")
                            modificador(ruta_tiempos,marca,nombres_listado,tiempos_listado, nombre)
                            mejores_tiempos.main()
                        elif evento.key == pygame.K_n:
                            # Aquí agregas lo que quieras hacer cuando se presiona 'n'
                            print("Tecla 'n' presionada")
                            mejores_tiempos.main()
                            
                pygame.display.flip()
    else:
        carga_datos(nombre, marca)