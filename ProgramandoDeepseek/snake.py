#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Juego Snake en Python usando Pygame
"""

import pygame       # Biblioteca principal para crear juegos
import random       # Para generar números aleatorios (posición de la comida)
import sys          # Para funciones del sistema (salir del juego)
import time         # Para controlar tiempos y pausas

# Inicializar todos los módulos de pygame necesarios para el juego
pygame.init()

# Definir colores en formato RGB (Red, Green, Blue)
NEGRO = (0, 0, 0)           # Color negro para el fondo
BLANCO = (255, 255, 255)    # Color blanco para textos
ROJO = (255, 0, 0)          # Color rojo para la comida
VERDE = (0, 255, 0)         # Color verde para la serpiente
AZUL = (0, 0, 255)          # Color azul para efectos especiales
VERDE_OSCURO = (0, 150, 0)  # Color verde oscuro para el cuerpo de la serpiente
VERDE_CLARO = (50, 255, 50) # Color verde claro para efectos en la serpiente

# Configuración de la pantalla
ANCHO = 800                 # Ancho de la ventana en píxeles
ALTO = 600                  # Alto de la ventana en píxeles
TAMANO_CELDA = 20           # Tamaño de cada celda en píxeles (tamaño de la cuadrícula)
FPS = 5  # Velocidad inicial del juego (más bajo = más lento)

# Crear la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)  # Modo redimensionable
pygame.display.set_caption('Juego de Snake')  # Título de la ventana

# Variable para controlar el modo de pantalla completa
pantalla_completa = False

# Definir el reloj para controlar la velocidad del juego (FPS)
reloj = pygame.time.Clock()

# Definir la clase Snake
class Snake:
    def __init__(self):
        """Inicializa la serpiente en el centro de la pantalla"""
        self.x = ANCHO // 2
        self.y = ALTO // 2
        self.velocidad_x = TAMANO_CELDA  # Movimiento inicial hacia la derecha
        self.velocidad_y = 0
        self.cuerpo = []
        self.longitud = 1
    
    def mover(self):
        """Actualiza la posición de la serpiente según su velocidad"""
        # Actualizar la posición de la cabeza
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Agregar la nueva posición al principio del cuerpo
        self.cuerpo.insert(0, (self.x, self.y))
        
        # Eliminar la última posición si excede la longitud actual
        if len(self.cuerpo) > self.longitud:
            self.cuerpo.pop()
    
    def cambiar_direccion(self, dx, dy):
        """Cambia la dirección de movimiento de la serpiente"""
        # Evitar que la serpiente se mueva en dirección opuesta a la actual
        if self.velocidad_x == 0 or dx == 0:
            self.velocidad_x = dx
            self.velocidad_y = dy
    
    def dibujar(self):
        """Dibuja la serpiente en la pantalla con estilo pixelart"""
        # Dibujar cada segmento del cuerpo con un estilo pixelart
        for i, segmento in enumerate(self.cuerpo):
            # Calcular el color (la cabeza es más clara que el cuerpo)
            if i == 0:  # Es la cabeza
                color_interior = VERDE_CLARO
                borde = 3  # Borde más grueso para la cabeza
            else:  # Es parte del cuerpo
                # Alternar tonos para dar efecto de segmentos
                if i % 2 == 0:
                    color_interior = VERDE
                else:
                    color_interior = VERDE_OSCURO
                borde = 2  # Borde para el cuerpo
            
            # Dibujar el rectángulo interior (relleno)
            rect = pygame.Rect(segmento[0], segmento[1], TAMANO_CELDA, TAMANO_CELDA)
            pygame.draw.rect(pantalla, color_interior, rect)
            
            # Dibujar el borde más oscuro
            pygame.draw.rect(pantalla, NEGRO, rect, borde)
            
            # Añadir detalles a la cabeza (ojos)
            if i == 0:
                # Determinar la posición de los ojos según la dirección
                if self.velocidad_x > 0:  # Mirando a la derecha
                    ojo_izq = (segmento[0] + TAMANO_CELDA - 6, segmento[1] + 5)
                    ojo_der = (segmento[0] + TAMANO_CELDA - 6, segmento[1] + TAMANO_CELDA - 8)
                elif self.velocidad_x < 0:  # Mirando a la izquierda
                    ojo_izq = (segmento[0] + 5, segmento[1] + 5)
                    ojo_der = (segmento[0] + 5, segmento[1] + TAMANO_CELDA - 8)
                elif self.velocidad_y < 0:  # Mirando arriba
                    ojo_izq = (segmento[0] + 5, segmento[1] + 5)
                    ojo_der = (segmento[0] + TAMANO_CELDA - 8, segmento[1] + 5)
                else:  # Mirando abajo o posición inicial
                    ojo_izq = (segmento[0] + 5, segmento[1] + TAMANO_CELDA - 6)
                    ojo_der = (segmento[0] + TAMANO_CELDA - 8, segmento[1] + TAMANO_CELDA - 6)
                
                # Dibujar los ojos
                pygame.draw.circle(pantalla, NEGRO, ojo_izq, 3)
                pygame.draw.circle(pantalla, NEGRO, ojo_der, 3)
    
    def verificar_colision(self):
        """Verifica si la serpiente ha colisionado con los bordes o consigo misma"""
        # Verificar colisión con los bordes de la pantalla
        if (self.x < 0 or self.x >= ANCHO or 
            self.y < 0 or self.y >= ALTO):
            return True
        
        # Verificar colisión con su propio cuerpo
        for segmento in self.cuerpo[1:]:
            if segmento == (self.x, self.y):
                return True
        
        return False
    
    def crecer(self):
        """Incrementa la longitud de la serpiente"""
        self.longitud += 1

# Definir la clase Comida
class Comida:
    def __init__(self):
        """Inicializa la comida en una posición aleatoria"""
        self.generar_posicion()
    
    def generar_posicion(self):
        """Genera una nueva posición aleatoria para la comida"""
        # Asegurarse de que la posición esté alineada con la cuadrícula
        self.x = random.randrange(0, ANCHO, TAMANO_CELDA)
        self.y = random.randrange(0, ALTO, TAMANO_CELDA)
    
    def dibujar(self):
        """Dibuja la comida en la pantalla con estilo pixelart"""
        # Crear un rectángulo para la posición de la comida
        rect = pygame.Rect(self.x, self.y, TAMANO_CELDA, TAMANO_CELDA)
        
        # Dibujar el relleno (interior) de la comida
        pygame.draw.rect(pantalla, ROJO, rect)
        
        # Dibujar el borde de la comida
        pygame.draw.rect(pantalla, NEGRO, rect, 2)
        
        # Añadir detalles para que parezca una manzana
        # Tallo
        pygame.draw.rect(pantalla, (100, 50, 0), (self.x + TAMANO_CELDA//2 - 1, self.y - 2, 2, 4))
        # Reflejo de luz (brillo)
        pygame.draw.circle(pantalla, (255, 200, 200), (self.x + 5, self.y + 5), 2)

def mostrar_puntuacion(puntaje):
    """Muestra la puntuación actual en la pantalla"""
    fuente = pygame.font.SysFont('Arial', 30)
    texto = fuente.render(f'Puntuación: {puntaje}', True, BLANCO)
    pantalla.blit(texto, (10, 10))

def mostrar_mensaje(mensaje, tamano=50):
    """Muestra un mensaje en el centro de la pantalla"""
    fuente = pygame.font.SysFont('Arial', tamano)
    texto = fuente.render(mensaje, True, BLANCO)
    # Centrar el texto en la pantalla
    rectangulo_texto = texto.get_rect()
    rectangulo_texto.center = (ANCHO//2, ALTO//2)
    pantalla.blit(texto, rectangulo_texto)
    pygame.display.update()

def juego_terminado(puntaje):
    """Muestra un mensaje de juego terminado y la puntuación final"""
    pantalla.fill(NEGRO)
    mostrar_mensaje('¡Juego Terminado!', 50)
    mostrar_mensaje(f'Puntuación Final: {puntaje}', 30)
    mostrar_mensaje('Presiona ESPACIO para jugar de nuevo', 30)
    pygame.display.update()
    
    # Esperar a que el jugador presione ESPACIO para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def dibujar_cuadricula():
    """Dibuja una cuadrícula para visualizar mejor el área de juego"""
    # Dibujar líneas verticales
    for x in range(0, ANCHO, TAMANO_CELDA):
        pygame.draw.line(pantalla, (50, 50, 50), (x, 0), (x, ALTO))
    
    # Dibujar líneas horizontales
    for y in range(0, ALTO, TAMANO_CELDA):
        pygame.draw.line(pantalla, (50, 50, 50), (0, y), (ANCHO, y))

def alternar_pantalla_completa():
    """Alterna entre el modo ventana y pantalla completa"""
    global pantalla, pantalla_completa
    
    pantalla_completa = not pantalla_completa
    
    if pantalla_completa:
        # Guardar el modo de ventana actual antes de cambiar a pantalla completa
        pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        # Volver al modo ventana
        pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)

def main():
    """Función principal del juego que contiene el bucle principal"""
    global FPS, pantalla_completa
    while True:
        # Inicializar objetos
        serpiente = Snake()     # Crear la serpiente
        comida = Comida()       # Crear la comida
        puntuacion = 0          # Inicializar puntuación
        juego_pausado = False   # Variable para controlar si el juego está pausado
        
        # Mostrar mensaje de inicio
        pantalla.fill(NEGRO)
        mostrar_mensaje('Snake Game - Presiona cualquier tecla para comenzar')
        pygame.display.update()
        
        # Esperar a que el jugador presione una tecla
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    esperando = False
        
        # Bucle principal del juego
        jugando = True          # Variable para controlar si el juego está activo
        while jugando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    # Controlar dirección de la serpiente con teclas de flecha
                    if not juego_pausado:  # Solo cambiar dirección si el juego no está pausado
                        if evento.key == pygame.K_UP and serpiente.velocidad_y != TAMANO_CELDA:
                            serpiente.cambiar_direccion(0, -TAMANO_CELDA)
                        elif evento.key == pygame.K_DOWN and serpiente.velocidad_y != -TAMANO_CELDA:
                            serpiente.cambiar_direccion(0, TAMANO_CELDA)
                        elif evento.key == pygame.K_LEFT and serpiente.velocidad_x != TAMANO_CELDA:
                            serpiente.cambiar_direccion(-TAMANO_CELDA, 0)
                        elif evento.key == pygame.K_RIGHT and serpiente.velocidad_x != -TAMANO_CELDA:
                            serpiente.cambiar_direccion(TAMANO_CELDA, 0)
                        # Controlar pausa con tecla P
                        elif evento.key == pygame.K_p:
                            juego_pausado = not juego_pausado
                        # Alternar pantalla completa con F11
                        elif evento.key == pygame.K_F11:
                            alternar_pantalla_completa()
            # Si el juego está pausado, no actualizar nada
            if juego_pausado:
                # Mostrar mensaje de pausa en la pantalla
                mostrar_mensaje("PAUSA", 40)
                continue
            
            # Mover la serpiente
            serpiente.mover()
            
            # Verificar colisiones
            if serpiente.verificar_colision():
                jugando = False
            
            # Verificar si la serpiente ha comido
            if serpiente.cuerpo[0] == (comida.x, comida.y):
                serpiente.crecer()
                comida.generar_posicion()
                puntuacion += 1
                # Aumentar velocidad cada 5 puntos
                if puntuacion % 5 == 0 and FPS < 10:
                    FPS += 1
            
            # Limpiar pantalla
            pantalla.fill(NEGRO)
            
            # Dibujar cuadrícula
            dibujar_cuadricula()
            
            # Dibujar serpiente y comida
            serpiente.dibujar()
            comida.dibujar()
            
            # Mostrar puntuación
            mostrar_puntuacion(puntuacion)
            
            # Actualizar pantalla
            pygame.display.update()
            
            # Controlar velocidad del juego
            reloj.tick(FPS)
        
        # Juego terminado, mostrar puntuación final
        juego_terminado(puntuacion)

# Iniciar el juego
if __name__ == "__main__":
    main()