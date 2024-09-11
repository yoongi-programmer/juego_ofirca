#!/usr/bin/env python, -*- coding: utf-8 -*-
import pygame #bajar la libreria desde la terminal
import pygame_gui #bajar la libreria desde la terminal
import sys
import random
import time
from menu_pausa import MenuPausa
from menu_inicio import MenuInicio
from tiempo import Cronometro
from tiempo import Temporizador
import cambiar_personaje
# Inicialización de Pygame
pygame.init()
pygame.font.init()

class Estado:
    INICIO = 1
    JUGANDO = 2
    PAUSA = 3
    SALIR = 4

class Juego:
    def __init__(self, pantalla):
        self.estado = Estado.INICIO
        self.pantalla = pantalla
        self.menu_inicio = MenuInicio()
        self.menu_pausa = MenuPausa(self.pantalla, self.menu_inicio)
        self.musica_inicio = self.Musica("img/assets/menu_inicio.mp3",-1,0.9)
        self.musica_pausa = self.Musica("img/assets/pausa.mp3",-1,0.4)
        self.musica_jugar = self.Musica("img/assets/jugar.mp3",-1,0.1)
        self.musica_ganar = self.Musica("img/assets/musica_ganar.mp3",1,0.9)
        self.sonido_bolsa = self.Musica("img/assets/sonido_bolsa.mp3",1,0.3)
        self.sonido_reloj = self.Musica("img/assets/sonido_bolsa.mp3",-1,0.05)
        self.ancho_pantalla = 1150
        self.alto_pantalla = 640
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("OFIRCA 2024 - Ronda 1 - Inicio")
        self.reloj = pygame.time.Clock()
        self.juego_ejecutado = True
        self.juego_pausado = False
        self.nombre_jugador = ""
        self.ingresando_nombre = True
        self.temporizador= Temporizador()
        self.cronometro = Cronometro()
        self.tiempo_total = "0:00:00"
        self.menu_pausa = MenuPausa(pantalla, self.menu_inicio)

        # Datos del personaje
        self.nombre_personaje = 'UAIBOT'
        self.ruta_imagen = ["img/assets/UAIBOT.png", "img/assets/bota.png", "img/assets/uaibotino.png", "img/assets/uaibotina.png"]
        self.nombres = ['UAIBOT', 'BOTA', 'UAIBOTINO', 'UAIBOTINA']
        self.velocidades = [7, 7, 10.15, 10.15]#10.15 es el 45% mas que 7
        self.num_robot = [1, 2, 3, 4]
        # Inicializar el juego
        self.inicializar_datos()

    def inicializar_objetos(self):    
        # Inicializar listas para bolsas verdes y negras
        bolsas_verdes = []
        bolsas_grises = []
        self.obstaculos = []
        obstaculos_img = ["img/assets/arbol1.png","img/assets/arbol2.png","img/assets/roca.png","img/assets/tronco.png"]
        ancho = [50,60]
        alto = [50,60]        
        for _ in range(4):
            imagen = random.choice(obstaculos_img)
            posicion = self.generar_posicion_aleatoria(ancho[0],alto[0],self.zonas_obstaculos)
            self.obstaculos.append(self.Obstaculos(imagen,posicion,self.pantalla))
        # Generar al menos 4 bolsas verdes y 4 bolsas grises
        for _ in range(4):
            pos_bolsa_verde = self.generar_posicion_aleatoria(ancho[0],alto[0],self.zonas_seguras)
            bolsas_verdes.append(self.Bolsa("img/assets/BolsaVerde.png", pos_bolsa_verde, "verde", self.pantalla))    
            pos_bolsa_gris = self.generar_posicion_aleatoria(ancho[0],alto[0],self.zonas_seguras)
            bolsas_grises.append(self.Bolsa("img/assets/BolsaGrisOscuro.png", pos_bolsa_gris, "gris", self.pantalla))

        # Generar las bolsas restantes (pueden ser verdes o grises)
        for _ in range(2):
            if random.choice([True, False]):
                pos_bolsa_verde = self.generar_posicion_aleatoria(ancho[0],alto[0],self.zonas_seguras)
                bolsas_verdes.append(self.Bolsa("img/assets/BolsaVerde.png", pos_bolsa_verde, "verde", self.pantalla))
            else:
                pos_bolsa_gris = self.generar_posicion_aleatoria(ancho[0],alto[0],self.zonas_seguras)
                bolsas_grises.append(self.Bolsa("img/assets/BolsaGrisOscuro.png", pos_bolsa_gris, "gris", self.pantalla))

        # Extender la lista de bolsas con las generadas
        self.bolsas.extend(bolsas_verdes + bolsas_grises)
    #___________________CLASE JUGADOR___________________
    class Jugador(pygame.sprite.Sprite):
        def __init__(self, imagen, nombre, posicion_inicial, rapidez, num_personaje, pantalla, ):
            super().__init__()
            self.carga_maxima = 1
            if num_personaje == 1:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/UAIBOT.png").convert_alpha(), (pantalla.get_width() // 15, pantalla.get_height() // 12))
                self.carga_maxima = 2
            elif num_personaje == 2:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/bota.png").convert_alpha(), (pantalla.get_width() // 15, pantalla.get_height() // 12))
                self.carga_maxima = 3
            elif num_personaje == 3:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/uaibotino.png").convert_alpha(), (pantalla.get_width() // 15, pantalla.get_height() // 12))
                self.carga_maxima = 1
            elif num_personaje == 4:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/uaibotina.png").convert_alpha(), (pantalla.get_width() // 15, pantalla.get_height() // 12))
                self.carga_maxima = 1

            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 22, pantalla.get_height() // 10))
            self.rect = self.image.get_rect(topleft=posicion_inicial)
            self.nombre = nombre
            self.rapidez = int(rapidez)

        def dibujar(self, pantalla):
            pantalla.blit(self.image, self.rect)
        
        def limitar_a_pantalla(self, ancho_pantalla, alto_pantalla):
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
    #___________________CLASE CESTO___________________
    class Cesto(pygame.sprite.Sprite):
        def __init__(self, imagen, posicion, pantalla):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 20, pantalla.get_height() // 8))        
            self.rect = self.image.get_rect(topleft=posicion)
        
        def dibujar(self, pantalla):
            pantalla.blit(self.image, self.rect)
    #___________________CLASE BOLSA___________________
    class Bolsa(pygame.sprite.Sprite):
        def __init__(self, imagen, posicion, tipo, pantalla):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 22, pantalla.get_height() // 10))
            self.rect = self.image.get_rect(topleft=posicion)
            self.tipo = tipo

        def dibujar(self, pantalla):
            pantalla.blit(self.image, self.rect)
    #___________________CLASE OBSTACULOS___________________
    class Obstaculos(pygame.sprite.Sprite):
        def __init__(self, imagen, posicion, pantalla):
            super().__init__()
            self.image =  pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 18, pantalla.get_height() // 8))
            self.rect = self.image.get_rect(topleft=posicion)
        
        def dibujar (self, pantalla):
            pantalla.blit(self.image, self.rect)
    #___________________CLASE COLISIONES___________________
    class Colisiones:
        def __init__(self, x, y, ancho, alto):
            self.rect = pygame.Rect(x, y, ancho, alto)

        def colisiona_con(self, otro_rect):
            return self.rect.colliderect(otro_rect)
    #___________________CLASE MUSICA_______________________
    class Musica:
        def __init__(self,sonido,duracion,volumen):
            self.sonido = pygame.mixer.Sound(sonido)
            self.duracion = duracion
            self.volumen = volumen
        
        def reproducir(self):
            self.sonido.set_volume(self.volumen)
            self.sonido.play()

        def reproducir_loop(self):
            self.sonido.set_volume(self.volumen)
            self.sonido.play(self.duracion)

        def detener(self):
            self.sonido.stop()
    #______________________________FUNCIONES DEL JUEGO________________________
    #Funcion que incializa los datos de graficos
    def inicializar_datos(self):
        self.img_fondo = pygame.transform.scale(pygame.image.load("img/fondo.jpg").convert_alpha(), (self.pantalla.get_width(), self.pantalla.get_height()))
        # Cargar imágenes
        self.img_recuadro_gris = pygame.transform.scale(pygame.image.load('img/recuadro_contador_gris.png').convert_alpha(), (50, 50))
        self.img_recuadro_verde = pygame.transform.scale(pygame.image.load('img/recuadro_contador_verde.png').convert_alpha(), (50, 50))
        self.img_cargar_bolsas = pygame.transform.scale(pygame.image.load('img/bolsas_cargadas.png').convert_alpha(), (100, 150))
        self.img_cont_bolsas = pygame.transform.scale(pygame.image.load('img/contador_bolsas.png').convert_alpha(), (150, 170))
        # Cargar fuentes
        self.fuente_grande = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 60)
        self.fuente_mediana = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 35)
        self.fuente_pequeña = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 17)  
        self.color_blanco, self.color_negro, = (255, 255, 255), (0, 0, 0)
        
    #Funcion que genera posiciones aleatorias en zonas seguras
    def generar_posicion_aleatoria(self,ancho,alto,zonas):
        zona_seleccionada = random.choice(zonas) # Seleccionar una zona segura aleatoria    
        # Generar una posición aleatoria dentro de la zona segura seleccionada
        posicion_valida = False
        while not posicion_valida:
            # Asegurarse de que la bolsa esté completamente dentro de los límites de la zona segura
            pos_x = random.randint(zona_seleccionada.left, zona_seleccionada.right - ancho)
            pos_y = random.randint(zona_seleccionada.top, zona_seleccionada.bottom - alto)
            nueva_posicion = pygame.Rect(pos_x, pos_y, ancho, alto)
            # Verificar que la nueva posición no colisione con otras bolsas o el jugador
            colisiona_con_bolsa = any(bolsa.rect.colliderect(nueva_posicion) for bolsa in self.bolsas)
            colisiona_con_jugador = self.jugador.rect.colliderect(nueva_posicion)
            colisiona_con_obstaculo = any(obstaculo.rect.colliderect(nueva_posicion) for obstaculo in self.obstaculos)

            # Verificar si la bolsa está dentro de la zona segura y no colisiona con otro objeto
            if zona_seleccionada.contains(nueva_posicion) and not colisiona_con_bolsa and not colisiona_con_jugador and not colisiona_con_obstaculo:
                posicion_valida = True
        return (pos_x, pos_y)
    #Funcion que incializa las estructuras de datos necesarias para el juego
    def inicializar_juego(self):
        self.bolsas = []
        self.cestos = []
        print("inicializando juego")
        # Posiciones random
        self.zona_colision = [
                self.Colisiones(0, 0, 550, 65), #colision arriba
                self.Colisiones(700, 0, 450, 65), #colision arriba lado 2
                self.Colisiones(0, 190, 169, 600),#colision izquierda
                self.Colisiones(745, 196, 400, 184),#colision derecha
                self.Colisiones(299, 190, 150, 130),#colision casa central
                self.Colisiones(460, 200, 40, 50),#colision arbol central
                self.Colisiones(580, 200, 40, 50)#colision arbol 2 central
        ]
        self.zonas_seguras = [
        pygame.Rect(20, 85, 950, 105),     # Zona segura 1 #left, top, width, height
        pygame.Rect(170, 520, 800, 100),   # Zona segura 2 #horizontal abajo
        pygame.Rect(800, 400, 300, 105),   # Zona segura 3 pasto casa
        pygame.Rect(300, 360, 300, 150),   # Zona segura 3 pasto casa
        pygame.Rect(169, 190, 120, 350),  # Zona segura 4 vertical
        pygame.Rect(640, 186, 100, 350)   # Zona segura 5 vertical
        ]
        self.zonas_obstaculos = [
        pygame.Rect(280, 85, 370, 105),     # Zona segura 1 #left, top, width, height
        pygame.Rect(170, 520, 650, 80),   # Zona segura 2 #horizontal abajo
        pygame.Rect(800, 400, 300, 105),   # Zona segura 3 pasto casa
        pygame.Rect(300, 360, 300, 150),   # Zona segura 3 pasto casa
        pygame.Rect(169, 190, 120, 350),  # Zona segura 4 vertical
        pygame.Rect(640, 186, 100, 350)   # Zona segura 5 vertical
        ]    
        # Inicializar instancias de las clases
        self.pos_bot = (100,90)
        self.jugador = self.Jugador("img/assets/UAIBOT.png", self.nombre_personaje, self.pos_bot, self.velocidades[0], self.num_robot[0], self.pantalla)
        self.cesto_verde = self.Cesto("img/assets/cestoverder.jpeg", (1000, 105), self.pantalla)
        self.cesto_negro = self.Cesto("img/assets/cestogriss.png", (1000, 520), self.pantalla)
        self.cestos.extend([self.cesto_verde, self.cesto_negro])
        # Inicializar objetos del juego usando la función 'inicializar_objetos'
        self.inicializar_objetos()
        self.contador_bolsas = 0
        self.contador_bolsas_v = 0
        self.contador_bolsas_g = 0
        self.bolsas_v_depositadas = 0
        self.bolsas_g_depositadas = 0
        self.total_bolsas = len(self.bolsas)
        self.temporizador.reiniciar()
        self.temporizador.iniciar()
        print(f"{self.temporizador.tiempo_inicio} ")
    #Funcion para dibujar texto
    def dibujar_texto(self, texto, tipografia, color_texto, pos_x, pos_y):
        texto_renderizado = tipografia.render(texto, True, color_texto)
        texto_borde = tipografia.render(texto, True, (0, 0, 0))  # Negro para el borde

        # Dibujar el borde del texto en las posiciones ligeramente desplazadas
        self.pantalla.blit(texto_borde, (pos_x - 1, pos_y))  # Izquierda
        self.pantalla.blit(texto_borde, (pos_x + 1, pos_y))  # Derecha
        self.pantalla.blit(texto_borde, (pos_x, pos_y - 1))  # Arriba
        self.pantalla.blit(texto_borde, (pos_x, pos_y + 1))  # Abajo
        self.pantalla.blit(texto_borde, (pos_x - 1, pos_y - 1))  # Esquina superior izquierda
        self.pantalla.blit(texto_borde, (pos_x + 1, pos_y - 1))  # Esquina superior derecha
        self.pantalla.blit(texto_borde, (pos_x - 1, pos_y + 1))  # Esquina inferior izquierda
        self.pantalla.blit(texto_borde, (pos_x + 1, pos_y + 1))  # Esquina inferior derecha

        # Dibujar el texto principal sobre el borde
        self.pantalla.blit(texto_renderizado, (pos_x, pos_y))
    #Funcion que dibuja la interfaz grafica
    def dibujar_ui(self):
        marcador_bolsasv = str(self.contador_bolsas_v) #contador de bolsas verdes cargadas
        marcador_bolsasg = str(self.contador_bolsas_g) #contador  de bolsas grises cargadas
        cuenta_regresiva = str(self.total_bolsas) #contador total bolsas
        cestos_v_contador = str(self.bolsas_v_depositadas) #contador  de bolsas verdes depositadas
        cestos_n_contador =  str(self.bolsas_g_depositadas) #contador  de bolsas grises depositadas

        self.pantalla.blit(self.img_fondo, (0, 0)) #Dibujar el fondo en la pantalla
        #Variables para las coordenadas y el tamaño de los recuadros
        pos_x_img = [40, 13, 1070,1070]
        pos_y_img = [230, 420, 125,540]
        pos_x = [60,105, 105, 25, 1085,1085,800,500]
        pos_y = [15,240, 310, 500, 128,543,580,300] 
        intro_texto = "Elije a tu robot con la tecla C para recolecta residuos y llevarlos a sus cestos correspondientes"

        #for zona in self.zonas_obstaculos:
        #    pygame.draw.rect(self.pantalla, self.color_blanco, zona)
     
        self.pantalla.blit(self.img_cargar_bolsas, (pos_x_img[0], pos_y_img[0]))
        self.pantalla.blit(self.img_cont_bolsas, (pos_x_img[1], pos_y_img[1]))
        self.pantalla.blit(self.img_recuadro_verde, (pos_x_img[2], pos_y_img[2]))
        self.pantalla.blit(self.img_recuadro_gris, (pos_x_img[3], pos_y_img[3]))
        
        self.dibujar_texto(intro_texto, self.fuente_pequeña, self.color_blanco, pos_x[0], pos_y[0])
        self.dibujar_texto(marcador_bolsasv, self.fuente_mediana, self.color_blanco, pos_x[1], pos_y[1])
        self.dibujar_texto(marcador_bolsasg, self.fuente_mediana, self.color_blanco, pos_x[2], pos_y[2])
        self.dibujar_texto(cuenta_regresiva, self.fuente_grande, self.color_blanco, pos_x[3], pos_y[3])
        self.dibujar_texto(cestos_v_contador, self.fuente_mediana, self.color_blanco, pos_x[4], pos_y[4])
        self.dibujar_texto(cestos_n_contador, self.fuente_mediana, self.color_blanco, pos_x[5], pos_y[5])
        self.dibujar_texto(self.tiempo_total, self.fuente_mediana, self.color_blanco, pos_x[6], pos_y[6])
        self.dibujar_texto(self.nombre_jugador, self.fuente_mediana, self.color_blanco, pos_x[7], pos_y[7])        
    #Funcion que dibuja los personajes y objetos que constantemente se actualizan
    def actualizar(self):
        # Eventos y lógica del juego
        for bolsa in self.bolsas:
            bolsa.dibujar(self.pantalla)
        for cesto in self.cestos:
            cesto.dibujar(self.pantalla)
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)
    #Funcion para obtener la velovcidad del jugador y moverlo
    def obtener_velocidad_jugador(self):
        keys = pygame.key.get_pressed()
        velocidad = [0, 0]
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocidad[0] = -self.jugador.rapidez
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocidad[0] = self.jugador.rapidez
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velocidad[1] = -self.jugador.rapidez
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocidad[1] = self.jugador.rapidez
        return velocidad
    #Funcion para cambiar de personaje
    def cambiar_personaje(self):
        self.temporizador.detener()
        personaje_elegido = cambiar_personaje.main()
        if personaje_elegido in range(1, 5):
            self.jugador = self.Jugador(
                self.ruta_imagen[personaje_elegido - 1],
                self.nombres[personaje_elegido - 1],
                self.pos_bot,
                self.velocidades[personaje_elegido - 1],
                self.num_robot[personaje_elegido - 1],
                self.pantalla
            )
        pygame.display.set_caption("Inicio")
    #Funcion que maneja la lógica de colisiones con bolsas y cestos
    def logica_bolsa_cestos(self):
        for bolsa in self.bolsas[:]:
            if self.jugador.rect.colliderect(bolsa.rect):
                if self.contador_bolsas < self.jugador.carga_maxima:
                    self.contador_bolsas += 1
                    self.sonido_bolsa.reproducir()
                    if bolsa.tipo == "verde":
                        self.contador_bolsas_v += 1
                    elif bolsa.tipo == "gris":
                        self.contador_bolsas_g += 1
                    self.bolsas.remove(bolsa)

        velocidad = self.obtener_velocidad_jugador()
        # Hacer que el jugador choque con las colisiones y no pase a traves de ellas 
        for colision in self.zona_colision:
              if self.jugador.rect.colliderect(colision.rect):
                    self.jugador.rect.x -= velocidad[0]
                    self.jugador.rect.y -= velocidad[1]
        for obstaculo in self.obstaculos:
            if self.jugador.rect.colliderect(obstaculo.rect):
                # Revertir la posición del jugador si colisiona con un obstáculo
                self.jugador.rect.x -= velocidad[0]
                self.jugador.rect.y -= velocidad[1]
        # Depositar bolsas si se colisiona con un cesto dependiendo el color
        if self.contador_bolsas_v > 0 and self.jugador.rect.colliderect(self.cesto_verde.rect):
            self.total_bolsas -= self.contador_bolsas_v #al total le resto lo que va depositando
            self.bolsas_v_depositadas += self.contador_bolsas_v #al contador del cesto le sumo lo que recolecto
            self.contador_bolsas -= self.contador_bolsas_v  #al contador de bolsas le resto lo que deposito
            self.contador_bolsas_v = 0
            
        if self.contador_bolsas_g > 0 and self.jugador.rect.colliderect(self.cesto_negro.rect):
            self.total_bolsas -= self.contador_bolsas_g
            self.bolsas_g_depositadas += self.contador_bolsas_g
            self.contador_bolsas -= self.contador_bolsas_g
            self.contador_bolsas_g = 0

        if self.total_bolsas == 0:
            self.juego_ejecutado = False
    #Funcion que muestra una pantalla cuando gana
    def ganar(self):
        # Carga la imagen de fondo de victoria
        img_victoria = pygame.image.load("img/fondo_ganar.png").convert_alpha()
        img_victoria = pygame.transform.scale(img_victoria, (self.pantalla.get_width(), self.pantalla.get_height()))

        self.pantalla.blit(img_victoria, (0, 0))
        self.musica_ganar.reproducir()
        pygame.display.update()
        # Espera 3 segundos antes de salir
        time.sleep(3)    
    #Funcion principal que maneja todos los eventos del juego en un bucle
    def bucle_juego(self):
        while self.juego_ejecutado:
            pygame.display.set_caption("Juego en ejecución")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Cambiar de personaje cuando se presiona la tecla C
                    if event.key == pygame.K_c:
                        self.cambiar_personaje()
                    # Poner el juego en pausa cuando se presiona la tecla ESC
                    elif event.key == pygame.K_ESCAPE:
                        self.juego_pausado = not self.juego_pausado
                        self.temporizador.detener()
                        if self.juego_pausado:
                            pygame.display.set_caption("Menú de pausa")
                            self.menu_pausa.mostrar_menu(self.pantalla)
                            self.juego_pausado = False
                            return "pausa"
                    # Reiniciar juego cuando se presiona  la tecla R
                    elif event.key == pygame.K_r:
                        self.inicializar_juego()
                        self.musica_jugar.detener()
                        self.musica_jugar.reproducir_loop()
            
            if not self.juego_pausado:
                self.dibujar_ui()                
                if self.ingresando_nombre: #si es true pide que ingrese el nombre
                    self.entrada_texto()
                else:
                    self.temporizador.iniciar() # si ya ingreso el nombre entonces corre el juego 
                    minuts, seconds, miliseconds = self.temporizador.restar_tiempo()
                    if minuts == "00" and seconds == "00"and miliseconds == "00":
                        resultadoPartida = 0
                        break 
                    else:
                        resultadoPartida = 1
                    velocidad = self.obtener_velocidad_jugador()
                    self.jugador.mover(velocidad)
                    self.jugador.limitar_a_pantalla(self.ancho_pantalla, self.alto_pantalla)
                    self.logica_bolsa_cestos()
                    self.actualizar()
                    self.tiempo_total = str(minuts)+":"+str(seconds)+":"+str(miliseconds)
                pygame.display.update()
                self.reloj.tick(60)

        self.musica_jugar.detener()
        #Cuando termina el juego        
        if resultadoPartida==0:
            print("perdiste como un pichón")
            pygame.quit()
            sys.exit()
        elif resultadoPartida==1:        
            self.ganar()
            decision = self.guardar_partida()
            if decision == "guardar":
                print("eligio guardar")
                self.entrada_texto()
            elif decision == "no_guardar":
                print("eligio no guardar y va al main")
                main()
    
    def entrada_texto(self):
        ancho_pantalla, alto_pantalla = 874, 521
        self.ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        self.fondo_ingresar = pygame.transform.scale(pygame.image.load("img/ingresar.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        # Dibujar ventana
        self.ventana.blit(self.fondo_ingresar, (0, 0))
        # Texto del nombre que el jugador va escribiendo
        nombre_texto = self.fuente_pequeña.render(self.nombre_jugador, True, self.color_blanco)
        self.ventana.blit(nombre_texto, (200, 240))

        # Centramos la ventana
        pos_x = (self.pantalla.get_width() - ancho_pantalla) // 2
        pos_y = (self.pantalla.get_height() - alto_pantalla) // 2
        self.pantalla.blit(self.ventana, (pos_x, pos_y))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if self.ingresando_nombre:
                # Manejar el ingreso de texto
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Si presiona Enter
                        self.ingresando_nombre = False  # Termina el ingreso de nombre
                        return self.nombre_jugador
                    elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        self.nombre_jugador = self.nombre_jugador[:-1]
                    else:
                        # Añadir la letra al nombre
                        self.nombre_jugador += evento.unicode
            pygame.display.flip()
            self.reloj.tick(60)

    def guardar_partida(self):
        print("Guardar partida")
        ancho_pantalla, alto_pantalla = 874, 521
        ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption("Guardar partida")

        fondo_guardar = pygame.transform.scale(pygame.image.load("img/guardar_partida.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        ventana.blit(fondo_guardar, (0, 0))
        
        pos_x = (self.pantalla.get_width() - ancho_pantalla) // 2
        pos_y = (self.pantalla.get_height() - alto_pantalla) // 2
        self.pantalla.blit(ventana, (pos_x, pos_y))
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

    def otra_partida(self, texto):
        print(texto)
        self.inicializar_juego()
        self.bucle_juego()  
#___________________Funcion principal que maneja los estados del juego___________________
def main():    
    pantalla = pygame.display.set_mode((1150, 640))
    juego = Juego(pantalla)
    menu_inicio = MenuInicio()
    menu_pausa = MenuPausa(pantalla, menu_inicio)
    estado = Estado.INICIO
    
    while True:        
        if estado == Estado.INICIO:
            juego.musica_inicio.reproducir_loop()
            opcion_menu_inicio = menu_inicio.bucle_principal()
            if opcion_menu_inicio == "salir":
                pygame.quit()
                sys.exit()
            elif opcion_menu_inicio == "jugar":
                juego.musica_inicio.detener()
                estado = Estado.JUGANDO

        elif estado == Estado.JUGANDO:
            juego.inicializar_juego()
            juego.musica_jugar.reproducir_loop()
            respuesta = juego.bucle_juego()
            if respuesta == "pausa":
                juego.musica_jugar.detener()
                estado = Estado.PAUSA
                continue

        elif estado == Estado.PAUSA:
            print("estado en pausa")
            juego.musica_jugar.detener()
            opcion_menu_pausa = menu_pausa.mostrar_menu(pantalla)
            if opcion_menu_pausa == "continuar":
                juego.musica_pausa.detener()
                estado = Estado.JUGANDO
            elif opcion_menu_pausa == "salir":
                estado = Estado.INICIO
                juego.musica_pausa.detener()
            
if __name__ == "__main__":
    main()