#!/usr/bin/env python, -*- coding: utf-8 -*-
import pygame #bajar la libreria desde la terminal
import pygame_gui #bajar la libreria desde la terminal
import sys
import random
from menu_pausa import MenuPausa
from menu_inicio import MenuInicio
from tiempo import Cronometro
import cambiarpersonaje
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
        def __init__(self, imagen, nombre, posicion_inicial, rapidez, numPersonaje, pantalla):
            super().__init__()
            if numPersonaje == 1:
                self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/UAIBOT.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
            elif numPersonaje == 2:
                self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/bota.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
            elif numPersonaje == 3:
                self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/uaibotino.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
            elif numPersonaje == 4:
                self.robotActual = pygame.transform.scale(pygame.image.load("img/assets/uaibotina.png").convert_alpha(), (pantalla.get_width() // 10, pantalla.get_height() // 5))
                
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
            self.image = pygame.transform.scale(pygame.image.load(imagen).convert_alpha(), (pantalla.get_width() // 12, pantalla.get_height() // 5))        
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
    #___________________CLASE CASAS___________________
    class Colisiones:
        def __init__(self, x, y, ancho, alto):
            self.rect = pygame.Rect(x, y, ancho, alto)

        def colisiona_con(self, otro_rect):
            return self.rect.colliderect(otro_rect)
        
    #___________________FUNCIONES DEL JUEGO___________________
    def inicializar_datos(self):
        self.img_fondo = pygame.transform.scale(pygame.image.load("img/fondo.jpg").convert_alpha(), (self.pantalla.get_width(), self.pantalla.get_height()))
        self.tipografia_grande = pygame.font.SysFont('Arial', 30)
        self.tipografia = pygame.font.SysFont('Arial', 18)
        self.color_verde, self.color_azul, self.color_blanco, self.color_negro, self.color_naranja, self.color_bordeaux = (103, 210, 137), (84, 125, 193), (255, 255, 255), (0, 0, 0), (239, 27, 126), (102, 41, 53)

    def generar_posicion_aleatoria(self,zonas_seguras):
        while True:
            pos = [random.randint(0, 1150), random.randint(0, 640)]  # Ajusta los límites según el tamaño de tu pantalla
            for zona in zonas_seguras:
                if zona.collidepoint(pos):
                    return pos

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
        self.jugador = self.Jugador("img/assets/uaibotino.png", self.nombre_personaje, self.pos_bot, self.rapidez_personaje, self.numRobot[0], self.pantalla)
        self.cesto_verde = self.Cesto("img/assets/cestoverder.png", (1000, 65), self.pantalla)
        self.cesto_negro = self.Cesto("img/assets/cestogriss.png", (1000, 450), self.pantalla)
        bolsa_verde_1 = self.Bolsa("img/assets/BolsaVerde.png", posBolsaVerde1, "verde", self.pantalla)
        bolsa_verde_2 = self.Bolsa("img/assets/BolsaVerde.png", posBolsaVerde2, "verde", self.pantalla)
        bolsa_negra_1 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris1, "gris", self.pantalla)
        bolsa_negra_2 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris2, "gris", self.pantalla)
        bolsa_negra_3 = self.Bolsa("img/assets/BolsaGrisOscuro.png", posBolsaGris3, "gris", self.pantalla)

        self.bolsas.extend([bolsa_verde_1, bolsa_verde_2, bolsa_negra_1, bolsa_negra_2, bolsa_negra_3])
        self.cestos.extend([self.cesto_verde, self.cesto_negro])
        
        self.contador_bolsas_v = 0
        self.contador_bolsas_g = 0
        self.bolsas_v_depositadas = 0
        self.bolsas_g_depositadas = 0
        self.total_bolsas = len(self.bolsas)
        self.cronometro.iniciar()
        print(f"reinicia valores: contador_b_v: {self.contador_bolsas_v,self.contador_bolsas_g,self.bolsas_v_depositadas,self.bolsas_g_depositadas,self.total_bolsas}")

    def dibujar_texto(self, texto, tipografia, color_texto, ancho_recuadro, alto_recuadro, color_recuadro, pos_x, pos_y):
        textoReglas = tipografia.render(texto, False, color_texto)
        pygame.draw.rect(self.pantalla, color_recuadro, (pos_x, pos_y, ancho_recuadro, alto_recuadro))
        self.pantalla.blit(textoReglas, (pos_x + 5, pos_y + 5, ancho_recuadro, alto_recuadro))

    def dibujar_ui(self):
        texto = 'Elige a tu personaje con la tecla C y muévelo con las flechas para recolectar residuos y llevarlos a sus cestos correspondientes.'
        marcador_bolsasv = ' Bolsas Verdes: ' + str(self.contador_bolsas_v)
        marcador_bolsasg = ' Bolsas Grises: ' + str(self.contador_bolsas_g)
        txt_marcador = marcador_bolsasv + marcador_bolsasg
        cuenta_regresiva = " Bolsas restantes: " + str(self.total_bolsas)
        cestos_v_contador = " Cesto verde: " + str(self.bolsas_v_depositadas)
        cestos_n_contador = " Cesto negro: " + str(self.bolsas_g_depositadas)
        cestos_msj = cestos_v_contador + cestos_n_contador
        self.pantalla.blit(self.img_fondo, (0, 0)) #Dibujar el fondo en la pantalla
        #Variables para las coordenadas y el tamaño de los recuadros
        ancho_recuadro = [400, 820, 300, 290]
        alto_recuadro = [40, 30, 40, 40]
        pos_x = [70, 15, 500, 830,840]
        pos_y = [15, 600, 15, 15,580]
        self.dibujar_texto(txt_marcador, self.tipografia_grande, self.color_blanco, ancho_recuadro[0], alto_recuadro[0], self.color_azul, pos_x[0], pos_y[0])
        self.dibujar_texto(texto, self.tipografia, self.color_blanco, ancho_recuadro[1], alto_recuadro[1], self.color_bordeaux, pos_x[1], pos_y[1])
        self.dibujar_texto(cuenta_regresiva, self.tipografia_grande, self.color_blanco, ancho_recuadro[2], alto_recuadro[2], self.color_verde, pos_x[2], pos_y[2])
        self.dibujar_texto(cestos_msj, self.tipografia_grande, self.color_blanco, ancho_recuadro[3], alto_recuadro[3], self.color_naranja, pos_x[3], pos_y[3])
        self.dibujar_texto(self.tiempo_total, self.tipografia_grande, self.color_blanco, ancho_recuadro[3], alto_recuadro[3] , self.color_naranja  , pos_x[4], pos_y[4])
    
    def actualizar(self):
        # Eventos y lógica del juego
        for bolsa in self.bolsas:
            bolsa.dibujar(self.pantalla)
        for cesto in self.cestos:
            cesto.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)

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

    def cambiar_personaje(self):
        self.cronometro.detener()
        personajeElegido = cambiarpersonaje.main()
        if personajeElegido in range(1, 5):
            self.jugador = self.Jugador(
                self.ruta_imagen[personajeElegido - 1],
                self.nombres[personajeElegido - 1],
                self.pos_bot,
                self.velocidades[personajeElegido - 1],
                self.numRobot[personajeElegido - 1],
                self.pantalla
            )
        pygame.display.set_caption("Inicio")
#_______Funcion que maneja la lógica de colisiones con bolsas y cestos______
    def logica_bolsa_cestos(self):
        for bolsa in self.bolsas[:]:
            if self.jugador.rect.colliderect(bolsa.rect):
                if bolsa.tipo == "verde" and self.contador_bolsas_v < 2:
                    self.contador_bolsas_v += 1
                    self.bolsas.remove(bolsa)
                elif bolsa.tipo == "gris" and self.contador_bolsas_g < 2:
                    self.contador_bolsas_g += 1
                    self.bolsas.remove(bolsa)

        velocidad = self.obtener_velocidad_jugador()
        for casa in self.casas:
              if self.jugador.rect.colliderect(casa.rect):
                    self.jugador.rect.x -= velocidad[0]
                    self.jugador.rect.y -= velocidad[1]
        # Depositar bolsas si se colisiona con un cesto
        if self.contador_bolsas_v > 0 and self.jugador.rect.colliderect(self.cesto_verde.rect):
            self.total_bolsas -= self.contador_bolsas_v
            self.bolsas_v_depositadas += self.contador_bolsas_v
            self.contador_bolsas_v = 0
            
        if self.contador_bolsas_g > 0 and self.jugador.rect.colliderect(self.cesto_negro.rect):
            self.total_bolsas -= self.contador_bolsas_g
            self.bolsas_g_depositadas += self.contador_bolsas_g
            self.contador_bolsas_g = 0

        if self.total_bolsas == 0:
            self.juego_ejecutado = False

    def bucle_juego(self):
        self.inicializar_juego()
        while self.juego_ejecutado:
            pygame.display.set_caption("Juego en ejecución")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.cronometro.detener()
                        if self.juego_pausado:
                            self.juego_pausado = False
                        else:
                            self.juego_pausado = True
                            pygame.display.set_caption("Menú de pausa")
                            self.menu_pausa.mostrar_menu(self.pantalla)
                            continue  # Salir del bucle y volver a comprobar el estado

                    if event.key == pygame.K_c:
                        self.cambiar_personaje()

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
        decision = self.guardar_partida()
        if decision == "guardar":
            print("eligio guardar")
            self.entrada_texto()
        elif decision == "no_guardar":
            print("eligio no guardar y va al main")
            main()
            return "menu_inicio"
        
        return "menu_inicio"
    
    def guardar_partida(self):
        print("Guardar partida")
        ancho_pantalla, alto_pantalla = 874, 521
        ventana = pygame.Surface((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption("Guardar partida")

        fondo_guardar = pygame.transform.scale(pygame.image.load("img/guardar_partida.png").convert_alpha(), (ancho_pantalla, alto_pantalla))
        print("Dibujar el fondo en la ventana")
        ventana.blit(fondo_guardar, (0, 0))
        
        pos_x = (self.pantalla.get_width() - ancho_pantalla) // 2
        pos_y = (self.pantalla.get_height() - alto_pantalla) // 2
        print("Dibujar la ventana en la pantalla")
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
            ancho = 100
            alto = 40
            pos_x = 550
            pos_y = 423
            self.dibujar_texto(self.tiempo_total, self.tipografia_grande, self.color_blanco, ancho, alto, self.color_negro, pos_x, pos_y)
            pygame.display.update()

    def otra_partida(self, texto):
        print(texto)
        self.inicializar_juego()
        self.bucle_juego()

    
#___________________Funcion que incia el juego en un main___________________
def main():
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menu inicio")

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
            resultado = juego.bucle_juego()
            if resultado == "pausa":
                estado = Estado.PAUSA
            elif resultado == "menu_inicio":
                estado = Estado.INICIO

        elif estado == Estado.PAUSA:
            print(f"en menu pausa if: opcion {opcion_menu_pausa}")
            opcion_menu_pausa = menu_pausa.mostrar_menu(pantalla)
            if opcion_menu_pausa == "continuar":
                print("decidio continuar")
                estado = Estado.JUGANDO
            elif opcion_menu_pausa == "salir":
                print("decidio salir")
                estado = Estado.INICIO
if __name__ == "__main__":
    main()