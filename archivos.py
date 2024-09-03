from io import open
import os
import pygame
import pygame_gui

def creacionComprobacion():
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
        print("la carpeta existe") 
    if not os.path.exists(ruta_nombres):
        nombres=open(ruta_nombres, 'x')
        nombres.close()
        print("nombres fue creado en su respectiva carpeta ")
    else:
        print("El archivo nombres ya existe en la carpeta")    
    if not os.path.exists(ruta_tiempos):
         tiempos=open(ruta_tiempos, 'x')
         tiempos.close()
         print("tiempos fue creado en su respectiva carpeta ")
    else:
         print("timepos ya existe en la carpeta")

def cargaDatos(nombreGuardar,marcaGuardar):
    tiempos_listado=archivosLectores(ruta_tiempos)
    nombres_listado=archivosLectores(ruta_nombres)
    
    if nombreGuardar in nombres_listado:
        parametroGenerales()
        corriendo=True
        ancho_pantalla, alto_pantalla = 400, 400
        ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption("Guardar partida")

        fondo_guardar = pygame.transform.scale(pygame.image.load("img/guardar_partida.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        #print("Dibujar el fondo en la ventana")
        ventana.blit(fondo_guardar, (0, 0))
        pos_x = (150)
        pos_y = (150)
        #print("Dibujar la ventana en la pantalla")
        pantalla.blit(ventana, (pos_x, pos_y))

        while corriendo:
            teclasSubmenu = pygame.key.get_pressed()
            for evento in pygame.event.get():
                if evento.type==teclasSubmenu[pygame.K_s]:
                    modificador(ruta_tiempos,marcaGuardar,nombres_listado,tiempos_listado,nombreGuardar)
                    pygame.quit()
                elif evento.type==teclasSubmenu[pygame.K_n]:
                    corriendo=False
                elif evento.type == pygame.QUIT:
                    pygame.quit()
                    pass
        
    elif not nombreGuardar in nombres_listado:
        tiempos=open(ruta_tiempos,'a')
        nombres=open(ruta_nombres,'a')
        tiempos.write(str(marcaGuardar)+'\n')
        nombres.write(str(nombreGuardar)+'\n')
        print("carga exitosa")
        tiempos.close()
        nombres.close()
        
def parametroGenerales():
        global color_fondo
        global pantalla
        color_fondo                  = (0, 0, 0)
        pygame.init()
        pygame.font.init()
        ancho_pantalla = 850
        alto_pantalla  = 450
        pantalla       = pygame.display.set_mode((ancho_pantalla, alto_pantalla))    
def dibujar_menu():

    pantalla.fill(color_fondo) 
    pygame.display.flip()
    
def mostrarDatos():
    tiemposListado=archivosLectores(ruta_tiempos)
    nombresListado=archivosLectores(ruta_nombres)
    rachas=list(zip(nombresListado,tiemposListado))
    for nombres,tiempos in rachas:
        print(f"{nombres} {tiempos}")

        
def mostrarMejores():
    pass

def modificador(archivo,deseocambiante,nombresRecibidos,marcasRecibidos,nombreJugador):
     archivo=open(archivo,"w")
     posicion=nombresRecibidos.index(nombreJugador)
     print(posicion)
     marcasRecibidos[posicion]=deseocambiante
     for elemento in marcasRecibidos:
         elemento=str(elemento)
         archivo.write(elemento+"\n")
     archivo.close()
 
def archivosLectores(archivo):
    archivo = open(archivo,"r")
    contenido=[linea.strip() for linea in archivo]
    archivo.close()
    return contenido
def dibujar_sobre_escritura():
    pass


def main(nombre,marca):
    print("entro al main de archivos")
    print(nombre)
    print(marca)
    creacionComprobacion()
    print("se comprobaron y se crearon correctamente")
    cargaDatos(nombre,marca)         