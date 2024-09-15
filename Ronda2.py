# Equipo 19535 Tec.py integrado por 3 alumnos de la Escuela Técnica N°2 de la Rép. Argentina
# Integrantes: Juan Cruz. Melanie Romero. Leonardo Robles
# El siguiente programa tiene como funcionalidad manejar los eventos del jugador como jugar, ver instrucciones o salir
# en donde el juego principal es mover a un robot para recolectar basura y llevarla  a un contenedor de basura
import pygame #bajar la libreria desde la terminal
import sys
import random
import time
from menu_pausa import MenuPausa
from menu_inicio import MenuInicio
from tiempo import Temporizador
from utilidades import cargar_gif_fondo
import cambiar_personaje
import archivos
import mejores_tiempos

# Inicialización de Pygame
pygame.init()
pygame.font.init()

class Estado:
    INICIO = 1
    JUGANDO = 2
    PAUSA = 3
    SALIR = 4
class BarraCargaDecremental:
    def __init__(self, pantalla, posicion, tamano, color, tiempo_total):
        # Inicializa la barra de carga
        self.pantalla = pantalla            # Superficie de pygame donde se dibujará la barra de carga.
        self.posicion = posicion            # (x, y) posición inicial de la barra en la ventana.
        self.tamano = tamano                # Tamaño de la barra.
        self.color = color                  # Color de la barra.
        self.tiempo_total = tiempo_total    # Tiempo total en segundos para que la barra se vacíe.
        self.ancho_inicial = tamano[0]      # Ancho inicial de la barra.
        
    def actualizar(self, porcentaje_restante):
        # Calcula el ancho de la barra basado en el porcentaje restante del temporizador
        nuevo_ancho = int(self.ancho_inicial * (porcentaje_restante / 100))
        self.tamano = (nuevo_ancho, self.tamano[1])

    def dibujar(self):
        # Dibuja la barra de carga en la pantalla.
        pygame.draw.rect(self.pantalla, self.color, (*self.posicion, *self.tamano))

    def ha_terminado(self):
        # Verifica si la barra de carga ha terminado.
        return self.tamano[0] <= 0
class Juego:
    def __init__(self, pantalla):
        self.estado = Estado.INICIO
        self.pantalla = pantalla
        self.menu_inicio = MenuInicio()
        self.menu_pausa = MenuPausa(self.pantalla, self.menu_inicio)
        self.musica_inicio = self.Musica("sonidos/menu_inicio.mp3",-1,0.9)
        self.musica_pausa = self.Musica("sonidos/pausa.mp3",-1,0.4)
        self.musica_jugar = self.Musica("sonidos/jugar.mp3",-1,0.1)
        self.musica_ganar = self.Musica("sonidos/musica_ganar.mp3",1,0.9)
        self.musica_perder = self.Musica("sonidos/game_over.mp3",1,0.5)
        self.sonido_bolsa = self.Musica("sonidos/sonido_bolsa.mp3",1,0.3)
        self.sonido_reloj = self.Musica("sonidos/reloj.mp3",-1,0.1)
        self.sonido_cesto = self.Musica("sonidos/sonido_cesto.mp3",1,0.9)
        self.sonido_choque = self.Musica("sonidos/choque.mp3",1,0.7)
        self.sonido_habilidad = self.Musica("sonidos/level_up.mp3",1,0.5)
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
        self.tiempo_total = "00:00:00"
        self.menu_pausa = MenuPausa(pantalla, self.menu_inicio)
        self.porcentaje_total = "00"
        self.barra_carga = BarraCargaDecremental(self.pantalla, (550, 15), (300, 40), (255, 0, 0), 10)  # Barra roja, duración 10 segundos
        self.temporizador_habilidad = "5"
        self.mostrar_velocidad = False
        self.mostrar_atravesar = False
        self.duracion_habilidad = 10
        self.tiempo_habilidad_restante = 0
        # Datos del personaje
        self.nombre_personaje = 'UAIBOT'
        self.ruta_imagen = ["img/assets/UAIBOT.png", "img/assets/bota.png", "img/assets/uaibotino.png", "img/assets/uaibotina.png"]
        self.nombres = ['UAIBOT', 'BOTA', 'UAIBOTINO', 'UAIBOTINA']
        self.ancho = [22,17,22,22]
        self.alto = [10,5,10,10]
        self.velocidades = [7, 7, 10.15,10.15,11]#10.15 es el 45% mas que 7
        self.num_robot = [1, 2, 3, 4]
        self.habilidad_atravesar_obs = False
        self.habilidad_velocidad = False
        # Inicializar el juego
        self.inicializar_datos()
    #___________________CLASE JUGADOR___________________
    class Jugador(pygame.sprite.Sprite):
        def __init__(self, imagen, nombre, posicion_inicial, rapidez, num_personaje, pantalla,ancho,alto ):
            super().__init__()
            self.carga_maxima = 1
            if num_personaje == 1:
                self.carga_maxima = 2
            elif num_personaje == 2:
                self.carga_maxima = 3
            elif num_personaje == 3:
                self.carga_maxima = 1
            elif num_personaje == 4:
                self.carga_maxima = 1

            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // ancho, pantalla.get_height() // alto))
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
        def __init__(self, imagen, posicion, pantalla,ancho,alto,tipo):
            super().__init__()
            self.image =  pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // ancho, pantalla.get_height() // alto))
            self.rect = self.image.get_rect(topleft=posicion)
            self.tipo = tipo
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
        self.img_velocidad = pygame.transform.scale(pygame.image.load('img/velocidad.png').convert_alpha(), (120, 55))
        self.img_atravesar = pygame.transform.scale(pygame.image.load('img/atravesar.png').convert_alpha(), (140, 55))
        self.img_fondo_carga = pygame.transform.scale(pygame.image.load('img/fondo_carga.png').convert_alpha(), (300, 55))
        # Cargar fuentes
        self.fuente_grande = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 60)
        self.fuente_mediana = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 35)
        self.fuente_mediana2 = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 48)
        self.fuente_pequeña = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 17)  
        self.fuente_pequeña2 = pygame.font.Font("fonts/pixel_digivolve/Pixel Digivolve.otf", 25)  
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
            colisiona_con_cofre = any(cofre.rect.colliderect(nueva_posicion) for cofre in self.cofres)
            # Verificar si la bolsa está dentro de la zona segura y no colisiona con otro objeto
            if zona_seleccionada.contains(nueva_posicion) and not colisiona_con_bolsa and not colisiona_con_jugador and not colisiona_con_obstaculo and not colisiona_con_cofre:
                posicion_valida = True
        return (pos_x, pos_y)
    #Funcion que inicializa los objetos a utilizar y sus posiciones
    def inicializar_objetos(self):    
        bolsas_verdes = []
        bolsas_grises = []
        self.obstaculos = []
        self.items = []
        self.cofres = []  # Lista para almacenar los cofres
        obstaculos_img = ["img/assets/arbol1.png","img/assets/arbol2.png","img/assets/roca.png","img/assets/tronco.png"]
        self.items_img = ["img/assets/pocion.png","img/assets/escudo.png"]
        # Generar los obstaculos con los que choca            
        for _ in range(4):
            imagen = random.choice(obstaculos_img)
            posicion = self.generar_posicion_aleatoria(40,40,self.zonas_obstaculos) ## ancho, alto, zonas
            self.obstaculos.append(self.Obstaculos(imagen,posicion,self.pantalla,19,9,"obstaculo"))
        # Generar al menos 4 bolsas verdes y 4 bolsas grises
        for _ in range(4):
            pos_bolsa_verde = self.generar_posicion_aleatoria(50,50,self.zonas_seguras)
            bolsas_verdes.append(self.Bolsa("img/assets/BolsaVerde.png", pos_bolsa_verde, "verde", self.pantalla))    
            pos_bolsa_gris = self.generar_posicion_aleatoria(50,50,self.zonas_seguras)
            bolsas_grises.append(self.Bolsa("img/assets/BolsaGrisOscuro.png", pos_bolsa_gris, "gris", self.pantalla))
        # Generar las bolsas restantes (pueden ser verdes o grises)
        for _ in range(2):
            if random.choice([True, False]):
                pos_bolsa_verde = self.generar_posicion_aleatoria(50,50,self.zonas_seguras)
                bolsas_verdes.append(self.Bolsa("img/assets/BolsaVerde.png", pos_bolsa_verde, "verde", self.pantalla))
            else:
                pos_bolsa_gris = self.generar_posicion_aleatoria(50,50,self.zonas_seguras)
                bolsas_grises.append(self.Bolsa("img/assets/BolsaGrisOscuro.png", pos_bolsa_gris, "gris", self.pantalla))
        # Extender la lista de bolsas con las generadas
        self.bolsas.extend(bolsas_verdes + bolsas_grises)
    #Funcion que incializa las estructuras de datos necesarias para el juego
    def inicializar_juego(self):
        self.bolsas = []
        self.cestos = []
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
        pygame.Rect(280, 85, 370, 55),     # Zona segura 1 #left, top, width, height
        pygame.Rect(170, 520, 650, 80),   # Zona segura 2 #horizontal abajo
        pygame.Rect(800, 400, 300, 105),   # Zona segura 3 pasto casa
        pygame.Rect(300, 360, 300, 150),   # Zona segura 3 pasto casa
        pygame.Rect(229, 190, 60, 350),  # Zona segura 4 vertical
        pygame.Rect(640, 186, 100, 350)   # Zona segura 5 vertical
        ]    
        # Inicializar instancias de las clases
        self.pos_bot = (100,90)
        self.jugador = self.Jugador("img/assets/UAIBOT.png", self.nombre_personaje, self.pos_bot, self.velocidades[0], self.num_robot[0], self.pantalla,self.ancho[0],self.alto[0])
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
        self.tiempo_proximo_evento = random.randint(60, 70)
        self.duracion_habilidad_velocidad = 10  # segundos
        self.duracion_habilidad_atravesar = 10  # segundos
        self.resultado_partida = 1
        print(f"{self.tiempo_proximo_evento}")
        self.total_bolsas = len(self.bolsas)
        self.temporizador.reiniciar()
    #Funcion para dibujar texto
    def dibujar_texto(self, texto, tipografia, color_texto, pos_x, pos_y,pantalla):
        texto_renderizado = tipografia.render(texto, True, color_texto)
        texto_borde = tipografia.render(texto, True, (0, 0, 0))  # Negro para el borde
        # Dibujar el borde del texto en las posiciones ligeramente desplazadas
        pantalla.blit(texto_borde, (pos_x - 1, pos_y))  # Izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y))  # Derecha
        pantalla.blit(texto_borde, (pos_x, pos_y - 1))  # Arriba
        pantalla.blit(texto_borde, (pos_x, pos_y + 1))  # Abajo
        pantalla.blit(texto_borde, (pos_x - 1, pos_y - 1))  # Esquina superior izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y - 1))  # Esquina superior derecha
        pantalla.blit(texto_borde, (pos_x - 1, pos_y + 1))  # Esquina inferior izquierda
        pantalla.blit(texto_borde, (pos_x + 1, pos_y + 1))  # Esquina inferior derecha
        # Dibujar el texto principal sobre el borde
        pantalla.blit(texto_renderizado, (pos_x, pos_y))
    def dibujar_porcentaje_sobre_barra(self):
        #Dibuja el porcentaje de tiempo restante sobre la barra decremental.
        pos_x_barra, pos_y_barra = self.barra_carga.posicion # Obtener la posición de la barra de carga
        # Preparar el texto del porcentaje
        texto_porcentaje = f"{self.porcentaje_total}%"
        texto_ancho, texto_alto = self.fuente_mediana2.size(texto_porcentaje)  # Obtener tamaño del texto
        pos_x_texto = pos_x_barra + (self.barra_carga.tamano[0] // 2) - (texto_ancho // 2)
        pos_y_texto = pos_y_barra + (self.barra_carga.tamano[1] // 2) - (texto_alto // 2)
        self.dibujar_texto(texto_porcentaje, self.fuente_pequeña2, self.color_blanco, pos_x_texto, pos_y_texto,self.pantalla)
    #Funcion que dibuja la interfaz grafica
    def dibujar_ui(self):
        marcador_bolsasv = str(self.contador_bolsas_v) #contador de bolsas verdes cargadas
        marcador_bolsasg = str(self.contador_bolsas_g) #contador  de bolsas grises cargadas
        cuenta_regresiva = str(self.total_bolsas) #contador total bolsas
        cestos_v_contador = str(self.bolsas_v_depositadas) #contador  de bolsas verdes depositadas
        cestos_n_contador =  str(self.bolsas_g_depositadas) #contador  de bolsas grises depositadas

        self.pantalla.blit(self.img_fondo, (0, 0)) #Dibujar el fondo en la pantalla
        #Variables para las coordenadas y el tamaño de los recuadros
        pos_x_img = [40 , 13 , 1070 ,1070,250,415,545]
        pos_y_img = [230, 420, 125  ,540 ,15 ,15 ,11]
        pos_x = [60 ,105, 105, 25 , 1085,1085,950,20,220,390]
        pos_y = [610,240, 310, 500, 128 ,543 ,15 ,18,20 ,20]  #yyyyy
        intro_texto = "Elije a tu robot con la tecla C para recolecta residuos y llevarlos a sus cestos correspondientes"

        #for zona in self.zonas_obstaculos:
        #    pygame.draw.rect(self.pantalla, self.color_blanco, zona)
        self.pantalla.blit(self.img_cargar_bolsas, (pos_x_img[0], pos_y_img[0]))
        self.pantalla.blit(self.img_cont_bolsas, (pos_x_img[1], pos_y_img[1]))
        self.pantalla.blit(self.img_recuadro_verde, (pos_x_img[2], pos_y_img[2]))
        self.pantalla.blit(self.img_recuadro_gris, (pos_x_img[3], pos_y_img[3]))

        self.pantalla.blit(self.img_fondo_carga, (pos_x_img[6], pos_y_img[6]))

        if self.mostrar_velocidad:
            tiempo_transcurrido = time.time() - self.habilidad_velocidad_tiempo
            tiempo_restante = max(0, self.duracion_habilidad_velocidad - int(tiempo_transcurrido))
            tiempo_restante = str(tiempo_restante)
            self.pantalla.blit(self.img_velocidad, (pos_x_img[4],pos_y_img[4]))
            self.dibujar_texto(tiempo_restante,self.fuente_mediana,self.color_blanco, pos_x[8], pos_y[8],self.pantalla)
        if self.mostrar_atravesar:
            tiempo_transcurrido = time.time() - self.habilidad_atravesar_obs_tiempo
            tiempo_restante = max(0, self.duracion_habilidad_atravesar - int(tiempo_transcurrido))
            tiempo_restante = str(tiempo_restante)
            self.pantalla.blit(self.img_atravesar, (pos_x_img[5],pos_y_img[5]))
            self.dibujar_texto(tiempo_restante,self.fuente_mediana,self.color_blanco, pos_x[9], pos_y[9],self.pantalla)

        self.dibujar_texto(intro_texto, self.fuente_pequeña, self.color_blanco, pos_x[0], pos_y[0],self.pantalla)
        self.dibujar_texto(marcador_bolsasv, self.fuente_mediana, self.color_blanco, pos_x[1], pos_y[1],self.pantalla)
        self.dibujar_texto(marcador_bolsasg, self.fuente_mediana, self.color_blanco, pos_x[2], pos_y[2],self.pantalla)
        self.dibujar_texto(cuenta_regresiva, self.fuente_grande, self.color_blanco, pos_x[3], pos_y[3],self.pantalla)
        self.dibujar_texto(cestos_v_contador, self.fuente_mediana, self.color_blanco, pos_x[4], pos_y[4],self.pantalla)
        self.dibujar_texto(cestos_n_contador, self.fuente_mediana, self.color_blanco, pos_x[5], pos_y[5],self.pantalla)
        self.dibujar_texto(self.tiempo_total, self.fuente_mediana, self.color_blanco, pos_x[6], pos_y[6],self.pantalla) ##temporizador
        if self.ingresando_nombre == False:
            # **Dibuja la barra de carga primero**
            self.barra_carga.dibujar()
            # **Dibuja el porcentaje sobre la barra de carga después**
            self.dibujar_porcentaje_sobre_barra()

            self.dibujar_texto(self.nombre_jugador[:10], self.fuente_mediana, self.color_blanco, pos_x[7], pos_y[7],self.pantalla)#imprime solo los primeros 10 caracteres      
    #Funcion que dibuja los personajes y objetos que constantemente se actualizan
    def actualizar(self):
        # Eventos y lógica del juego
        for bolsa in self.bolsas:
            bolsa.dibujar(self.pantalla)
        for cesto in self.cestos:
            cesto.dibujar(self.pantalla)
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.pantalla)
        for cofre in self.cofres:
            cofre.dibujar(self.pantalla)
        for item in self.items:
            item.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)
    #Funcion para genera eventos aleatorios donde crear los cofres
    def actualizar_eventos_temporizador(self):
        # Verificar si ha pasado el tiempo para generar un cofre
        if self.temporizador.tiempo_actual <= self.tiempo_proximo_evento:
            posicion = self.generar_posicion_aleatoria(20,20,self.zonas_seguras)
            self.cofres.append(self.Obstaculos("img/assets/cofre.png",posicion,self.pantalla,26,16,"cofre"))
            # Definir un nuevo tiempo aleatorio para el siguiente cofre
            self.tiempo_proximo_evento = self.temporizador.tiempo_actual - random.randint(10, 18)
            print(f"proximo evento {self.tiempo_proximo_evento}")
    #Funcion para obtener la velovcidad del jugador y moverlo
    def obtener_velocidad_jugador(self,rapidez):
        keys = pygame.key.get_pressed()
        velocidad = [0, 0]
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocidad[0] = -rapidez
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocidad[0] = rapidez
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velocidad[1] = -rapidez
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocidad[1] = rapidez
        return velocidad
    #Funcion para cambiar de personaje
    def cambiar_personaje(self):
        self.temporizador.detener()
        personaje_elegido = cambiar_personaje.main()
        if personaje_elegido in range(1, 5):
            print(f"Cambiando a personaje {personaje_elegido} con velocidad {self.velocidades[personaje_elegido - 1]}")
            self.jugador = self.Jugador(
                self.ruta_imagen[personaje_elegido - 1],
                self.nombres[personaje_elegido - 1],
                self.pos_bot,
                self.velocidades[personaje_elegido - 1],
                self.num_robot[personaje_elegido - 1],
                self.pantalla,
                self.ancho[personaje_elegido-1],
                self.alto[personaje_elegido-1],
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

        if self.habilidad_velocidad:
            velocidad = self.obtener_velocidad_jugador(self.velocidades[4])
        else:
            velocidad = self.obtener_velocidad_jugador(self.jugador.rapidez)
        # Hacer que el jugador choque con las colisiones y no pase a traves de ellas 
        for colision in self.zona_colision:
              if self.jugador.rect.colliderect(colision.rect):
                    self.jugador.rect.x -= velocidad[0]
                    self.jugador.rect.y -= velocidad[1]
        # Revertir la posición del jugador si colisiona con un obstáculo
        for obstaculo in self.obstaculos:
            if self.jugador.rect.colliderect(obstaculo.rect) and self.habilidad_atravesar_obs == False:
                self.sonido_choque.reproducir()
                self.jugador.rect.x -= velocidad[0]
                self.jugador.rect.y -= velocidad[1]
        
        for cofre in self.cofres[:]:
            if self.jugador.rect.colliderect(cofre):
                self.cofres.remove(cofre)  # Eliminar cofre
                imagen = random.choice(self.items_img)
                tipo = "pocion" if "pocion" in imagen else "escudo"
                posicion = (cofre.rect.x + 10, cofre.rect.y + 10)
                self.items.append(self.Obstaculos(imagen,posicion,self.pantalla,29,15,tipo))
        
        for item in self.items[:]:
            if self.jugador.rect.colliderect(item):
                self.sonido_habilidad.reproducir()
                if item.tipo == "pocion":
                    self.habilidad_velocidad = True 
                    self.mostrar_velocidad = True
                    self.habilidad_velocidad_tiempo = time.time()
                    pygame.time.delay(1000)
                    self.items.remove(item)
                else:
                    self.habilidad_atravesar_obs = True
                    self.mostrar_atravesar = True
                    self.habilidad_atravesar_obs_tiempo = time.time()
                    pygame.time.delay(1000)
                    self.items.remove(item)
        # Verificar si la habilidad de velocidad ha estado activa por más de 5 segundos
        if self.habilidad_velocidad and (time.time() - self.habilidad_velocidad_tiempo > 10):
            self.habilidad_velocidad = False  # Desactiva la habilidad de velocidad
            self.mostrar_velocidad = False
        if self.habilidad_atravesar_obs and (time.time() - self.habilidad_atravesar_obs_tiempo > 10):
            self.habilidad_atravesar_obs = False  # Desactiva la habilidad de atravesar obstáculos
            self.mostrar_atravesar = False
        # Depositar bolsas si se colisiona con un cesto dependiendo el color
        if self.contador_bolsas_v > 0 and self.jugador.rect.colliderect(self.cesto_verde.rect):
            self.sonido_cesto.reproducir()
            self.total_bolsas -= self.contador_bolsas_v #al total le resto lo que va depositando
            self.bolsas_v_depositadas += self.contador_bolsas_v #al contador del cesto le sumo lo que recolecto
            self.contador_bolsas -= self.contador_bolsas_v  #al contador de bolsas le resto lo que deposito
            self.contador_bolsas_v = 0
            
        if self.contador_bolsas_g > 0 and self.jugador.rect.colliderect(self.cesto_negro.rect):
            self.sonido_cesto.reproducir()
            self.total_bolsas -= self.contador_bolsas_g
            self.bolsas_g_depositadas += self.contador_bolsas_g
            self.contador_bolsas -= self.contador_bolsas_g
            self.contador_bolsas_g = 0

        if self.total_bolsas == 0:
            self.juego_ejecutado = False
    #Funcion que muestra una pantalla cuando gana
    def ganar(self):
        # Cargar frames del video
        self.frames = cargar_gif_fondo("img/ganar/frame_1 (1).png",20,6,").gif")
        self.frame_actual = 0
        self.pantalla.fill((0, 0, 0))
        self.musica_ganar.reproducir()
        corriendo = True
        while corriendo:
            if self.frame_actual < len(self.frames) - 1:
                # Actualizar frame del video
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                self.pantalla.blit(self.frames[self.frame_actual], (0, 0))
                pygame.display.flip()
                self.reloj.tick(30)
            else:
                # Mostrar el ultimo frame y no actualizar mas
                self.pantalla.blit(self.frames[-1], (0, 0))
                corriendo = False
        
    #Funcion que muestra una animacion cuando pierde
    def perder(self):
        # Cargar frames del video
        self.frames = cargar_gif_fondo("img/game_over/GAME OVER_50ms_1.png",1,5,".png")
        self.frame_actual = 0
        self.pantalla.fill((0, 0, 0))
        corriendo = True
        self.musica_perder.reproducir()
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_1:
                        self.inicializar_juego()
                        self.musica_jugar.reproducir_loop()
                        self.bucle_juego()
                    elif evento.key == pygame.K_2:
                        main()
            if self.frame_actual < len(self.frames) - 1:
                # Actualizar frame del video
                self.frame_actual = (self.frame_actual + 1) % len(self.frames)
                self.pantalla.blit(self.frames[self.frame_actual], (0, 0))
                pygame.display.flip()
                self.reloj.tick(30)
            else:
                # Mostrar el ultimo frame y no actualizar mas
                self.pantalla.blit(self.frames[-1], (0, 0))
        
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
                    self.minuts, self.seconds, self.miliseconds, porcentaje_restante = self.temporizador.restar_tiempo()
                    if self.minuts == "00" and self.seconds == "00"and self.miliseconds == "00":
                        self.resultado_partida = 0
                        break 
                    else:
                        self.resultado_partida = 1
                    if self.habilidad_velocidad:
                        velocidad = self.obtener_velocidad_jugador(self.velocidades[4])
                    else:
                        velocidad = self.obtener_velocidad_jugador(self.jugador.rapidez)
                    self.jugador.mover(velocidad)
                    self.jugador.limitar_a_pantalla(self.ancho_pantalla, self.alto_pantalla)
                    self.logica_bolsa_cestos()
                    # Actualizar barra de carga con porcentaje restante
                    self.barra_carga.actualizar(float(porcentaje_restante))
                    self.actualizar()
                    self.actualizar_eventos_temporizador()
                    self.tiempo_total = str(self.minuts)+":"+str(self.seconds)+":"+str(self.miliseconds)
                    self.porcentaje_total = f"{porcentaje_restante}"  # Formato del porcentaje
                pygame.display.update()
                self.reloj.tick(60)

        self.musica_jugar.detener()
        self.sonido_reloj.detener()
        #Cuando termina el juego        
        if self.resultado_partida==0:
            self.perder()
        elif self.resultado_partida==1:
            time.sleep(2)
            self.ganar()
            decision = self.guardar_partida()
            if decision == "guardar":
                print("eligio guardar")
                archivos.main(self.nombre_jugador,self.tiempo_total )
                
                mejores_tiempos.main()
            elif decision == "no_guardar":
                print("eligio no guardar y va al main")
        main()
    
    def entrada_texto(self):
        ancho_pantalla, alto_pantalla = 874, 521
        self.ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        self.fondo_ingresar = pygame.transform.scale(pygame.image.load("img/fondo_ingresar.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        titulo = "Ingresar Nombre de Jugador"
        bienvenida = f"¡Bienvenido al futuro sustentable, {self.nombre_jugador}!"
        bienvenida2 = "¿Listo para salvar el planeta reciclando?"
        # Dibujar ventana
        self.ventana.blit(self.fondo_ingresar, (0, 0))
        self.dibujar_texto(titulo,self.fuente_mediana2,self.color_blanco,52,50,self.ventana)
        # Texto del nombre que el jugador va escribiendo
        nombre_texto = self.fuente_mediana.render(self.nombre_jugador, True, self.color_blanco)
        self.ventana.blit(nombre_texto, (200, 300))

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
                        self.dibujar_texto(bienvenida, self.fuente_pequeña2, self.color_blanco, 280, 470, self.pantalla)
                        self.dibujar_texto(bienvenida2, self.fuente_pequeña2, self.color_blanco, 260, 495, self.pantalla)
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        self.ingresando_nombre = False  # Termina el ingreso de nombre  
                    elif evento.key == pygame.K_BACKSPACE:  # Borrar último carácter
                        self.nombre_jugador = self.nombre_jugador[:-1]
                    else:
                        # Añadir la letra al nombre
                        self.nombre_jugador += evento.unicode
            pygame.display.flip()
            self.reloj.tick(60)

    def guardar_partida(self):
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
            juego.sonido_reloj.reproducir_loop()
            respuesta = juego.bucle_juego()
            if respuesta == "pausa":
                estado = Estado.PAUSA
                continue

        elif estado == Estado.PAUSA:
            print("estado en pausa")
            juego.musica_jugar.detener()
            juego.sonido_reloj.detener()
            opcion_menu_pausa = menu_pausa.mostrar_menu(pantalla)
            if opcion_menu_pausa == "continuar":
                juego.musica_pausa.detener()
                estado = Estado.JUGANDO
            elif opcion_menu_pausa == "salir":
                estado = Estado.INICIO
                juego.musica_pausa.detener()
            
if __name__ == "__main__":
    main()