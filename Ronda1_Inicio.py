#!/usr/bin/env python, -*- coding: utf-8 -*-
import pygame #bajar la libreria desde la terminal
import sys
import random
import time
import pygame_gui
from menu_pausa import MenuPausa
from menu_inicio import MenuInicio
from tiempo import Cronometro
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
        self.ancho_pantalla = 1150
        self.alto_pantalla = 640
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("OFIRCA 2024 - Ronda 1 - Inicio")
        self.reloj = pygame.time.Clock()
        self.juego_ejecutado = True
        self.juego_pausado = False
        self.cronometro = Cronometro()
        self.tiempo_total = "0:00:00"
        self.menu_pausa = MenuPausa(pantalla, self.menu_inicio)

        # Datos del personaje
        self.nombre_personaje = 'UAIBOT'
        self.rapidez_personaje = 7
        self.ruta_imagen = ["img/assets/UAIBOT.png", "img/assets/bota.png", "img/assets/uaibotino.png", "img/assets/uaibotina.png"]
        self.nombres = ['UAIBOT', 'BOTA', 'UAIBOTINO', 'UAIBOTINA']
        self.velocidades = ['7', '6', '8', '8']
        self.numRobot = [1, 2, 3, 4]
        # Inicializar el juego
        self.inicializar_datos()
    #___________________CLASE JUGADOR___________________
    class Jugador(pygame.sprite.Sprite):
        def __init__(self, imagen, nombre, posicion_inicial, rapidez, num_personaje, pantalla, ):
            super().__init__()
            self.carga_maxima = 1
            if num_personaje == 1:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/UAIBOT.png").convert_alpha(), (pantalla.get_width() // 3, pantalla.get_height() // 0.5))
                self.carga_maxima = 2
            elif num_personaje == 2:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/bota.png").convert_alpha(), (pantalla.get_width() // 3, pantalla.get_height() // 0.5))
                self.carga_maxima = 3
            elif num_personaje == 3:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/uaibotino.png").convert_alpha(), (pantalla.get_width() // 7, pantalla.get_height() // 2))
                self.carga_maxima = 1
            elif num_personaje == 4:
                self.robot_actual = pygame.transform.scale(pygame.image.load("img/assets/uaibotina.png").convert_alpha(), (pantalla.get_width() // 7, pantalla.get_height() // 2))
                self.carga_maxima = 1

            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 16, pantalla.get_height() // 8))
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
            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 15, pantalla.get_height() // 6))        
            self.rect = self.image.get_rect(topleft=posicion)
        
        def dibujar(self, pantalla):
            pantalla.blit(self.image, self.rect)
    #___________________CLASE BOLSA___________________
    class Bolsa(pygame.sprite.Sprite):
        def __init__(self, imagen, posicion, tipo, pantalla):
            super().__init__()
            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 18, pantalla.get_height() // 7))
            self.rect = self.image.get_rect(topleft=posicion)
            self.tipo = tipo

        def dibujar(self, pantalla):
            pantalla.blit(self.image, self.rect)
    #___________________CLASE COLISIONES___________________
    class Colisiones:
        def __init__(self, x, y, ancho, alto):
            self.rect = pygame.Rect(x, y, ancho, alto)

        def colisiona_con(self, otro_rect):
            return self.rect.colliderect(otro_rect)
        
    #______________________________FUNCIONES DEL JUEGO________________________
    #Funcion que incializa los datos de graficos
    def inicializar_datos(self):
        self.img_fondo = pygame.transform.scale(pygame.image.load("img/fondo.jpg").convert_alpha(), (self.pantalla.get_width(), self.pantalla.get_height()))
        self.tipografia_grande = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 60)
        self.tipografia = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 35)        
        self.color_blanco, self.color_negro, = (255, 255, 255), (0, 0, 0)
    #Funcion que genera posiciones aleatorias en zonas seguras
    def generar_posicion_aleatoria(self,zonas_seguras):
        while True:
            pos = [random.randint(0, 1150), random.randint(0, 640)]  # Ajusta los límites según el tamaño de tu pantalla
            for zona in zonas_seguras:
                if zona.collidepoint(pos):
                    return pos
    #Funcion que incializa las estructuras de datos necesarias para el juego
    def inicializar_juego(self):
        self.bolsas = []
        self.cestos = []
        print("inicializando juego")
        
        zonas_seguras = [
        pygame.Rect(0, 85, 250, 105),     # Zona segura 1
        pygame.Rect(550, 85, 150, 115),   # Zona segura 2
        pygame.Rect(900, 85, 300, 105),   # Zona segura 3
        pygame.Rect(169, 190, 130, 700),  # Zona segura 4
        pygame.Rect(450, 196, 295, 184)   # Zona segura 5
        ]
        # Posiciones random
        posBolsaGris1 = self.generar_posicion_aleatoria(zonas_seguras)
        posBolsaGris2 = self.generar_posicion_aleatoria(zonas_seguras)
        posBolsaGris3 = self.generar_posicion_aleatoria(zonas_seguras)
        posBolsaVerde1 = self.generar_posicion_aleatoria(zonas_seguras)
        posBolsaVerde2 = self.generar_posicion_aleatoria(zonas_seguras)
        self.pos_bot = (100,90)
        self.casas = [
                self.Colisiones(0, 0, 550, 85), #colision arriba
                self.Colisiones(700, 0, 450, 85), #colision arriba lado 2
                self.Colisiones(0, 190, 169, 600),#colision izquierda
                self.Colisiones(745, 196, 400, 184),#colision derecha
                self.Colisiones(299, 190, 150, 130),#colision casa central
                self.Colisiones(460, 200, 40, 50),#colision arbol central
                self.Colisiones(580, 200, 40, 50)#colision arbol 2 central
        ]
        # Inicializar instancias de las clases
        self.jugador = self.Jugador("img/assets/UAIBOT.png", self.nombre_personaje, self.pos_bot, self.rapidez_personaje, self.numRobot[0], self.pantalla)
        self.cesto_verde = self.Cesto("img/assets/cestoverder.jpeg", (1000, 85), self.pantalla)
        self.cesto_negro = self.Cesto("img/assets/cestogriss.png", (1000, 500), self.pantalla)
        bolsa_verde_1 = self.Bolsa("img/assets/BolsaVerde.png", posBolsaVerde1, "verde", self.pantalla)
        bolsa_verde_2 = self.Bolsa("img/assets/BolsaVerde.png", posBolsaVerde2, "verde", self.pantalla)
        bolsa_negra_1 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris1, "gris", self.pantalla)
        bolsa_negra_2 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris2, "gris", self.pantalla)
        bolsa_negra_3 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris3, "gris", self.pantalla)

        self.bolsas.extend([bolsa_verde_1, bolsa_verde_2, bolsa_negra_1, bolsa_negra_2, bolsa_negra_3])
        self.cestos.extend([self.cesto_verde, self.cesto_negro])
        
        self.contador_bolsas = 0
        self.contador_bolsas_v = 0
        self.contador_bolsas_g = 0
        self.bolsas_v_depositadas = 0
        self.bolsas_g_depositadas = 0
        self.total_bolsas = len(self.bolsas)
        self.cronometro.tiempo_inicio = 0  # Resetear tiempo de inicio
        self.cronometro.tiempo_total = 0
        self.cronometro.iniciar()
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
        # Cargar imágenes
        img_texto = pygame.transform.scale(pygame.image.load('img/intro_text.png').convert_alpha(), (1100, 30))
        img_recuadro = pygame.transform.scale(pygame.image.load('img/recuadro_contador.png').convert_alpha(), (50, 50))
        img_cargar_bolsas = pygame.transform.scale(pygame.image.load('img/bolsas_cargadas.png').convert_alpha(), (100, 150))
        img_cont_bolsas = pygame.transform.scale(pygame.image.load('img/contador_bolsas.png').convert_alpha(), (130, 170))
        marcador_bolsasv = str(self.contador_bolsas_v) #contador de bolsas verdes cargadas
        marcador_bolsasg = str(self.contador_bolsas_g) #contador  de bolsas grises cargadas
        cuenta_regresiva = str(self.total_bolsas) #contador total bolsas
        cestos_v_contador = str(self.bolsas_v_depositadas) #contador  de bolsas verdes depositadas
        cestos_n_contador =  str(self.bolsas_g_depositadas) #contador  de bolsas grises depositadas

        self.pantalla.blit(self.img_fondo, (0, 0)) #Dibujar el fondo en la pantalla
        #Variables para las coordenadas y el tamaño de los recuadros
        pos_x_img = [15, 40, 20, 1090,1090]
        pos_y_img = [15, 230, 420, 105,500]
        pos_x = [105, 105, 35, 1105,1105,800]
        pos_y = [240, 310, 500, 110,505,580]
        self.pantalla.blit(img_texto, (pos_x_img[0], pos_y_img[0]))
        self.pantalla.blit(img_cargar_bolsas, (pos_x_img[1], pos_y_img[1]))
        self.pantalla.blit(img_cont_bolsas, (pos_x_img[2], pos_y_img[2]))
        self.pantalla.blit(img_recuadro, (pos_x_img[3], pos_y_img[3]))
        self.pantalla.blit(img_recuadro, (pos_x_img[4], pos_y_img[4]))
        
        self.dibujar_texto(marcador_bolsasv, self.tipografia, self.color_blanco, pos_x[0], pos_y[0])
        self.dibujar_texto(marcador_bolsasg, self.tipografia, self.color_blanco, pos_x[1], pos_y[1])
        self.dibujar_texto(cuenta_regresiva, self.tipografia_grande, self.color_blanco, pos_x[2], pos_y[2])
        self.dibujar_texto(cestos_v_contador, self.tipografia, self.color_blanco, pos_x[3], pos_y[3])
        self.dibujar_texto(cestos_n_contador, self.tipografia, self.color_blanco, pos_x[4], pos_y[4])
        self.dibujar_texto(self.tiempo_total, self.tipografia, self.color_blanco, pos_x[5], pos_y[5])    
    #Funcion que dibuja los personajes y objetos que constantemente se actualizan
    def actualizar(self):
        # Eventos y lógica del juego
        for bolsa in self.bolsas:
            bolsa.dibujar(self.pantalla)
        for cesto in self.cestos:
            cesto.dibujar(self.pantalla)
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
        self.cronometro.detener()
        personaje_elegido = cambiar_personaje.main()
        if personaje_elegido in range(1, 5):
            self.jugador = self.Jugador(
                self.ruta_imagen[personaje_elegido - 1],
                self.nombres[personaje_elegido - 1],
                self.pos_bot,
                self.velocidades[personaje_elegido - 1],
                self.numRobot[personaje_elegido - 1],
                self.pantalla
            )
        pygame.display.set_caption("Inicio")
    #Funcion que maneja la lógica de colisiones con bolsas y cestos
    def logica_bolsa_cestos(self):
        for bolsa in self.bolsas[:]:
            if self.jugador.rect.colliderect(bolsa.rect):
                if self.contador_bolsas < self.jugador.carga_maxima:
                    self.contador_bolsas += 1
                    if bolsa.tipo == "verde":
                        self.contador_bolsas_v += 1
                    elif bolsa.tipo == "gris":
                        self.contador_bolsas_g += 1
                    self.bolsas.remove(bolsa)

        velocidad = self.obtener_velocidad_jugador()
        for casa in self.casas:
              if self.jugador.rect.colliderect(casa.rect):
                    self.jugador.rect.x -= velocidad[0]
                    self.jugador.rect.y -= velocidad[1]
        # Depositar bolsas si se colisiona con un cesto dependiendo el color
        if self.contador_bolsas_v > 0 and self.jugador.rect.colliderect(self.cesto_verde.rect):
            self.total_bolsas -= self.contador_bolsas_v
            self.bolsas_v_depositadas += self.contador_bolsas_v
            self.contador_bolsas_v = 0
            self.contador_bolsas = 0
            
        if self.contador_bolsas_g > 0 and self.jugador.rect.colliderect(self.cesto_negro.rect):
            self.total_bolsas -= self.contador_bolsas_g
            self.bolsas_g_depositadas += self.contador_bolsas_g
            self.contador_bolsas_g = 0
            self.contador_bolsas = 0

        if self.total_bolsas == 0:
            self.juego_ejecutado = False
    #Funcion que muestra una pantalla cuando gana
    def ganar(self):
        # Carga la imagen de fondo de victoria
        img_victoria = pygame.image.load("img/fondo_ganar.png").convert_alpha()
        img_victoria = pygame.transform.scale(img_victoria, (self.pantalla.get_width(), self.pantalla.get_height()))

        self.pantalla.blit(img_victoria, (0, 0))
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
                    if event.key == pygame.K_c:
                        self.cambiar_personaje()

                    elif event.key == pygame.K_ESCAPE:
                        self.juego_pausado = not self.juego_pausado
                        self.cronometro.detener()
                        if self.juego_pausado:
                            pygame.display.set_caption("Menú de pausa")
                            self.menu_pausa.mostrar_menu(self.pantalla)
                            self.juego_pausado = False
                            return "pausa"
                            
            if not self.juego_pausado:
                self.cronometro.iniciar()
                minuts, seconds, miliseconds = self.cronometro.actualizar_tiempo()
                velocidad = self.obtener_velocidad_jugador()
                self.jugador.mover(velocidad)
                self.jugador.limitar_a_pantalla(self.ancho_pantalla, self.alto_pantalla)
                self.logica_bolsa_cestos()

                self.dibujar_ui()
                self.actualizar()
                self.tiempo_total = str(minuts)+":"+str(seconds)+":"+str(miliseconds)
                pygame.display.update()
                self.reloj.tick(60)

        #Cuando termina el juego        
        self.ganar()
        decision = self.guardar_partida()
        if decision == "guardar":
            print("eligio guardar")
            self.entrada_texto()
        elif decision == "no_guardar":
            print("eligio no guardar y va al main")
            main()

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

    def entrada_texto(self):
        ancho_pantalla, alto_pantalla = 874, 521
        ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption("Guardar datos")

        fondo_ingresar = pygame.transform.scale(pygame.image.load("img/ingresar.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        ventana.blit(fondo_ingresar, (0, 0))
        manager = pygame_gui.UIManager((ancho_pantalla, alto_pantalla))

        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((320, 280), (500, 50)), manager=manager, object_id='#main_text_entry')
        reloj = pygame.time.Clock()
        pygame.display.flip()
        
        while True:
            UI_REFRESH_RATE = reloj.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry':
                    self.otra_partida(event.text)
                
                manager.process_events(event)
            manager.update(UI_REFRESH_RATE)
            pos_x = (self.pantalla.get_width() - ancho_pantalla) // 2
            pos_y = (self.pantalla.get_height() - alto_pantalla) // 2
            self.pantalla.blit(ventana, (pos_x, pos_y))
            manager.draw_ui(self.pantalla)
            pos_x = 550
            pos_y = 423
            self.dibujar_texto(self.tiempo_total,self.tipografia_grande,self.color_blanco,pos_x,pos_y)
            pygame.display.update()

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
            opcion_menu_inicio = menu_inicio.bucle_principal()
            if opcion_menu_inicio == "salir":
                pygame.quit()
                sys.exit()
            elif opcion_menu_inicio == "jugar":
                estado = Estado.JUGANDO

        elif estado == Estado.JUGANDO:
            juego.inicializar_juego()
            respuesta = juego.bucle_juego()
            if respuesta == "pausa":
                estado = Estado.PAUSA
                continue

        elif estado == Estado.PAUSA:
            opcion_menu_pausa = menu_pausa.mostrar_menu(pantalla)
            if opcion_menu_pausa == "continuar":
                estado = Estado.JUGANDO
            elif opcion_menu_pausa == "salir":
                estado = Estado.INICIO
            
if __name__ == "__main__":
    main()