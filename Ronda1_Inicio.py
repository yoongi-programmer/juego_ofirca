#!/usr/bin/env python, -*- coding: utf-8 -*-
import pygame
import sys
import random
import pygame_gui
from menu_pausa import MenuPausa
from menu_inicio import MenuInicio
import cambiarpersonaje
# Inicialización de Pygame
pygame.init()
pygame.font.init()
##----------------------CLASE JUGADOR----------------------------
class Jugador (pygame.sprite.Sprite):
    def __init__(self, imagen, nombre, posicion_inicial, rapidez,numPersonaje):
        super().__init__()
        rutaImagen=["img/assets/UAIBOT.png","img/assets/bota.png","img/assets/uaibotino.png","img/assets/uaibotina.png"]
        if numPersonaje==1:
            self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/UAIBOT.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
        elif numPersonaje==2:
            self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/bota.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
        elif numPersonaje==3:
            self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/uaibotino.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
        elif numPersonaje==4:
            self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/uaibotina.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
            
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
        self.rect = self.image.get_rect(topleft = posicion_inicial)
        self.nombre = nombre
        self.rapidez = rapidez       

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
    
    def limitar_a_pantalla(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > ancho_pantalla:
            self.rect.right = ancho_pantalla
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > alto_pantalla:
            self.rect.bottom = alto_pantalla
    
    def mover(self, velocidad):
        self.rect.x += velocidad[0]
        self.rect.y += velocidad[1]
##----------------------CLASE CESTOS----------------------------
class Cesto(pygame.sprite.Sprite):
    def __init__(self, imagen, posicion):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 12, pantalla.get_height() // 5))        
        self.rect = self.image.get_rect(topleft = posicion)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
##----------------------CLASE BOLSAS----------------------------
class Bolsa(pygame.sprite.Sprite):
    def __init__(self, imagen, posicion, tipo):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 18, pantalla.get_height() // 7))
        self.rect = self.image.get_rect(topleft = posicion)
        self.tipo = tipo

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)

# Configuración de la pantalla
ancho_pantalla = 1150
alto_pantalla = 640
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
titulo_ventana = "OFIRCA 2024 - Ronda 1 - Inicio"
# Crear instancia del menú de inicio y pausa
menu_inicio = MenuInicio()
opcion_menu_inicio = menu_inicio.bucle_principal()  # Mostrar el menú de inicio y obtener la opción seleccionada
menu_pausa = MenuPausa(pantalla,menu_inicio)
# Definicion de variables del juego
juegoEnEjecucion = True
clock = pygame.time.Clock()
ticksAlComenzar = pygame.time.get_ticks()
juegoPausado = False
# Datos del personaje
nombrePersonaje = 'UAIBOT'
rapidezPersonaje = 7
rutaImagen=["img/assets/UAIBOT.png","img/assets/bota.png","img/assets/uaibotino.png","img/assets/uaibotina.png"]
nombres=['UAIBOT','BOTA','UAIBOTINO','UAIBOTINA']
velocidades=['7','6','8','8']
numRobot=[1,2,3,4]

#________________Funcion que inicializa la ventana del juego_______________
def inicializar_pantalla(titulo_ventana):
    pygame.display.set_caption(titulo_ventana)
    return pygame.display.set_mode((ancho_pantalla, alto_pantalla))
#________________Funcion que incializa los datos de graficos_______________
def inicializar_datos():
    global imgFondo, tipografia, tipografiaGrande, colorVerde, colorAzul, colorBlanco, colorNegro, colorNaranja, colorBordeaux
    pantalla = inicializar_pantalla(titulo_ventana)
    imgFondo = pygame.transform.scale(pygame.image.load("img/fondo.jpg").convert_alpha(), (pantalla.get_width(), pantalla.get_height()))
    tipografiaGrande = pygame.font.SysFont('Oswald', 30)
    tipografia = pygame.font.SysFont('Arial',18)
    colorVerde, colorAzul, colorBlanco, colorNegro, colorNaranja, colorBordeaux = (103, 210, 137), (84, 125, 193), (255, 255, 255), (0, 0, 0), (239, 27, 126), (102, 41, 53)
    return pantalla
#_______________Funcion que incializa los objetos del juego________________
def inicializar_juego():
    global jugador, cesto_verde, cesto_negro, bolsas, cestos
    global posBot1
    # Posiciones random
    posBolsaGris1 = [random.randint(250, 900), random.randint(200, 210)]
    posBolsaGris2 = [random.randint(250, 900), random.randint(400, 460)]
    posBolsaGris3 = [random.randint(750, 800), random.randint(200, 450)]
    posBolsaVerde1 = [random.randint(50, 270), random.randint(90, 120)]
    posBolsaVerde2 = [random.randint(250, 900), random.randint(400, 460)]
    posBot1 = [random.randint(50, 700), random.randint(50, 400)]
    # Incializar instancias de las clases
    jugador = Jugador("img/assets/uaibotino.png", nombrePersonaje, posBot1, rapidezPersonaje,numRobot[0])
    cesto_verde = Cesto("img/assets/cestoverder.png", (1000, 170))
    cesto_negro = Cesto("img/assets/cestogriss.png", (1000, 430))
    bolsa_verde_1 = Bolsa("img/assets/BolsaVerde.png", posBolsaVerde1, "verde")
    bolsa_verde_2 = Bolsa("img/assets/BolsaVerde.png", posBolsaVerde2, "verde")
    bolsa_negra_1 = Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris1, "gris")
    bolsa_negra_2 = Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris2, "gris")
    bolsa_negra_3 = Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris3, "gris")
    # Guardar las instancias en listas
    bolsas = [bolsa_verde_1, bolsa_verde_2, bolsa_negra_1, bolsa_negra_2, bolsa_negra_3]
    cestos = [cesto_verde, cesto_negro]    
#_________________Funcion que dibuja los textos para el juego______________
def dibujar_texto(texto, tipografia, color_texto, ancho_recuadro, alto_recuadro, color_recuadro, pos_x, pos_y):
    textoReglas = tipografia.render(texto, False, color_texto)
    pygame.draw.rect(pantalla, color_recuadro, (pos_x, pos_y, ancho_recuadro, alto_recuadro))
    pantalla.blit(textoReglas, (pos_x + 5, pos_y + 5, ancho_recuadro, alto_recuadro))

#____________Funcion que dibuja la interfaz del juego completa_____________
def dibujar_ui(contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas,minutos,segundos,milisegundos):
    #Variables de los contadores y contenedores del texto para marcador
    texto = 'Elige a tu personaje con la tecla C y muévelo con las flechas para recolectar residuos y llevarlos a sus cestos correspondientes.'
    marcador_bolsasv = ' Bolsas Verdes: ' + str(contador_bolsas_v)
    marcador_bolsasg = ' Bolsas Grises: ' + str(contador_bolsas_g)
    txt_marcador = marcador_bolsasv + marcador_bolsasg
    cuenta_regresiva = " Bolsas restantes: " + str(total_bolsas)
    cestos_v_contador = " Cesto verde: " + str(bolsas_v_depositadas)
    cestos_n_contador = " Cesto negro: " + str(bolsas_g_depositadas)
    cestos_msj = cestos_v_contador + cestos_n_contador
    textoCronometro=str(minutos)+":"+str(segundos)+":"+str(milisegundos)
    #Variables para las coordenadas y el tamaño de los recuadros
    ancho_recuadro = [400, 820, 300, 290]
    alto_recuadro = [40, 30, 40, 40]
    pos_x = [70, 15, 500, 830,840]
    pos_y = [15, 600, 15, 15,580]
    pantalla.blit(imgFondo, (0, 0)) #Dibujar el fondo en la pantalla
    dibujar_texto(txt_marcador, tipografiaGrande, colorBlanco, ancho_recuadro[0], alto_recuadro[0], colorAzul, pos_x[0], pos_y[0])
    dibujar_texto(texto, tipografia, colorBlanco, ancho_recuadro[1], alto_recuadro[1], colorBordeaux, pos_x[1], pos_y[1])
    dibujar_texto(cuenta_regresiva, tipografiaGrande, colorBlanco, ancho_recuadro[2], alto_recuadro[2], colorVerde, pos_x[2], pos_y[2])
    dibujar_texto(cestos_msj, tipografiaGrande, colorBlanco, ancho_recuadro[3], alto_recuadro[3], colorNaranja, pos_x[3], pos_y[3])
    dibujar_texto(textoCronometro  , tipografiaGrande, colorBlanco, ancho_recuadro[3], alto_recuadro[3] , colorNaranja  , pos_x[4], pos_y[4])
#_________________Funcion que dibuja las bolsas y cestos___________________
def dibujar_bolsas_y_cestos(pantalla):
    for bolsa in bolsas:
        bolsa.dibujar(pantalla)
    for cesto in cestos:
        cesto.dibujar(pantalla)
    jugador.dibujar(pantalla)
#_______Funcion que maneja la lógica de colisiones con bolsas y cestos______
def logica_bolsa_cestos(jugador,juegoEnEjecucion, bolsas, cesto_verde, cesto_negro, contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas):
    for bolsa in bolsas[:]:
        if jugador.rect.colliderect(bolsa.rect):
            if bolsa.tipo == "verde" and contador_bolsas_v < 2:
                contador_bolsas_v += 1
                print(contador_bolsas_v)
                bolsas.remove(bolsa)
            elif bolsa.tipo == "gris" and contador_bolsas_g < 2:
                contador_bolsas_g += 1
                print(contador_bolsas_g)
                bolsas.remove(bolsa)

    # Depositar bolsas si se colisiona con un cesto
    if contador_bolsas_v > 0 and jugador.rect.colliderect(cesto_verde.rect):
        total_bolsas -= contador_bolsas_v
        bolsas_v_depositadas += contador_bolsas_v
        contador_bolsas_v = 0
        
    if contador_bolsas_g > 0 and jugador.rect.colliderect(cesto_negro.rect):
        total_bolsas -= contador_bolsas_g
        bolsas_g_depositadas += contador_bolsas_g
        contador_bolsas_g = 0

    if total_bolsas == 0:
       juegoEnEjecucion = False

    return juegoEnEjecucion,contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas

def reiniciar_valores():
    contador_bolsas_v = 0
    contador_bolsas_g = 0
    bolsas_v_depositadas = 0
    bolsas_g_depositadas = 0   
    total_bolsas = len(bolsas)

    return contador_bolsas_v,contador_bolsas_g,bolsas_g_depositadas,bolsas_v_depositadas,total_bolsas

def guardar_partida(pantalla):
    ancho_pantalla = 874
    alto_pantalla = 521
    titulo_ventana = "Guardar partida"
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption(titulo_ventana)

    fondo_guardar = pygame.transform.scale(pygame.image.load("img/guardar_partida.png").convert_alpha(), (pantalla.get_width(), pantalla.get_height()))
    pantalla.blit(fondo_guardar, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Guardar partida
                    return "guardar"

                elif event.key == pygame.K_n:  # No guardar
                    return "no_guardar"
                elif event.key == pygame.K_q:  # Salir del juego
                    pygame.quit()
                    sys.exit()

def entrada_texto():
    ancho_pantalla = 874
    alto_pantalla = 521
    titulo_ventana = "Guardar datos"
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    pygame.display.set_caption(titulo_ventana)

    fondo_ingresar = pygame.transform.scale(pygame.image.load("img/ingresar.png").convert_alpha(), (pantalla.get_width(), pantalla.get_height()))
    pantalla.blit(fondo_ingresar, (0, 0))
    manager = pygame_gui.UIManager((874, 521))

    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((180, 220), (500, 50)), manager=manager,object_id='#main_text_entry')
    pygame.display.flip()

    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                otra_partida(event.text)
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(pantalla)
        ancho = 100
        alto = 40
        pos_x = 400
        pos_y = 480
        
        dibujar_texto(tiempoHecho,tipografia,colorBlanco,ancho,alto,colorNegro,pos_x,pos_y)
        pygame.display.update()

def otra_partida():
    inicializar_juego()
    bucle_juego(pantalla)

    
#__________Funcion que maneja toda la logica del juego en bucle_____________
def bucle_juego(pantalla):
    global juegoEnEjecucion, juegoPausado
    global jugador
    global tiempoHecho

    import tiempo
    miCronometro=tiempo.cronometro()
    miCronometro.iniciar()
    contador_bolsas_v,contador_bolsas_g,bolsas_g_depositadas,bolsas_v_depositadas,total_bolsas=reiniciar_valores()

    while juegoEnEjecucion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    miCronometro.detener()
                    juegoPausado = not juegoPausado
                    if juegoPausado:
                        menu_pausa.mostrar_menu(pantalla)  # Mostrar el menú de pausa
                        juegoPausado = False  
                        pygame.time.delay(100)  # Evitar registrar múltiples pulsaciones rápidas de ESC
        
        if not juegoPausado:
            miCronometro.iniciar()
            minuts,seconds,miliseconds=miCronometro.actualizar_tiempo()
            keys = pygame.key.get_pressed()
            velocidad = [0, 0]
            if keys[pygame.K_LEFT]:
                velocidad[0] = -jugador.rapidez
            if keys[pygame.K_RIGHT]:
                velocidad[0] = jugador.rapidez
            if keys[pygame.K_UP]:
                velocidad[1] = -jugador.rapidez
            if keys[pygame.K_DOWN]:
                velocidad[1] = jugador.rapidez
            if keys[pygame.K_c]: 
                
                miCronometro.detener()
                personajeElegido=cambiarpersonaje.main()
                if personajeElegido<=4:
                    if personajeElegido==1:
                        jugador=Jugador(rutaImagen[0],nombres[0],posBot1,velocidades[0],personajeElegido)
                    elif personajeElegido==2:
                        jugador=Jugador(rutaImagen[1],nombres[1],posBot1,velocidades[1],personajeElegido)
                    elif personajeElegido==3:
                        jugador=Jugador(rutaImagen[2],nombres[2],posBot1,velocidades[2],personajeElegido)
                    elif personajeElegido==4:
                        jugador=Jugador(rutaImagen[3],nombres[3],posBot1,velocidades[3],personajeElegido)
                elif personajeElegido>5:
                    pass
                pygame.display.set_caption("Inicio")
                
        tiempoHecho=str(minuts)+":"+str(seconds)+":"+str(miliseconds)
        jugador.mover(velocidad)
        jugador.limitar_a_pantalla()
        juegoEnEjecucion,contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas = logica_bolsa_cestos(jugador,juegoEnEjecucion, bolsas, cesto_verde, cesto_negro, contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas)
        dibujar_ui(contador_bolsas_v, contador_bolsas_g, total_bolsas, bolsas_v_depositadas, bolsas_g_depositadas,minuts,seconds,miliseconds)
        dibujar_bolsas_y_cestos(pantalla)
        pygame.display.update()
        clock.tick(60)
    # Ejecutar estas funciones cuando termine la partida 
    decision = guardar_partida(pantalla)
    if decision == "guardar":
        entrada_texto()
    elif decision == "no_guardar":
        main()
    reiniciar_valores()

#___________________Funcion que incia el juego en un main___________________
def main():
    pygame.init()
    pygame.font.init()
    
    pantalla = inicializar_datos()
    menu_inicio = MenuInicio()
    opcion_menu_inicio = menu_inicio.bucle_principal()

    if opcion_menu_inicio == "salir":
        reiniciar_valores
        pygame.quit()
        sys.exit()

    if opcion_menu_inicio == "jugar":
        inicializar_juego()
        bucle_juego(pantalla)

if __name__ == "__main__":
    main()