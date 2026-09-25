import random
import sys
from turtle import color
import pygame

pygame.init()
TAM = 36
ANCHO, ALTO = 760, 420
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 16)
def crear_tablero():
     return [["·"] * 10 for _ in range(10)]
def colocar_barcos(tablero, tamaños=(5, 4, 3, 3, 2)):
     for tam in tamaños:
        colocado = False
        while not colocado:
            horizontal = random.choice([True, False])
            if horizontal:
                x = random.randint(0, 9 - tam)
                y = random.randint(0, 9)
                celdas = [(x + i, y) for i in range(tam)]
            else:
                x = random.randint(0, 9)
                y = random.randint(0, 9 - tam)
                celdas = [(x, y + i) for i in range(tam)]
            if all(tablero[cx][cy] == "·" for cx, cy in celdas):
                for cx, cy in celdas:
                    tablero[cx][cy] = "B"
                colocado = True

jugador = crear_tablero()
enemigo = crear_tablero()
colocar_barcos(jugador)
colocar_barcos(enemigo)

# Las "X" y "T" que vamos marcando al disparar
disparos_jugador = crear_tablero()
disparos_enemigo = crear_tablero()
turno_jugador = True
hundidos = 0
ganaste = False
perdiste = False

def barcos_restantes(tablero):
    return sum(fila.count("B") for fila in tablero)

def dibujar_tablero(tablero_disparos, ox, oy, ver_barcos=False):
    for fila in range(10):
        for col in range(10):
            celda = tablero_disparos[fila][col]
            color = (30, 60, 120)
            if celda == "X":
                color = (60, 60, 60)
            elif celda == "T":
                color = (220, 60, 60)
            pygame.draw.rect(pantalla, color,(ox + col * TAM, oy + fila * TAM, TAM - 2, TAM - 2))
            
ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and turno_jugador and not ganaste and not perdiste:
            mx, my = pygame.mouse.get_pos()
            col = (mx - 10) // TAM
            fila = (my - 10) // TAM
            if 0 <= fila < 10 and 0 <= col < 10 and disparos_enemigo[fila][col] == "·":
                if enemigo[fila][col] == "B":
                    disparos_enemigo[fila][col] = "T"
                    enemigo[fila][col] = "X"
                    print("¡Tocado!")
                    if barcos_restantes(enemigo) == 0:
                        ganaste = True
                else:
                    disparos_enemigo[fila][col] = "X"
                    print("Agua. Turno de la IA...")
                    turno_jugador = False

 # Turno de la IA: dispara a una celda aleatoria
    if not turno_jugador and not ganaste and not perdiste:
        while True:
            fila = random.randint(0, 9)
            col = random.randint(0, 9)
            if disparos_jugador[fila][col] == "·":
                if jugador[fila][col] == "B":
                    disparos_jugador[fila][col] = "T"
                    jugador[fila][col] = "X"
                    print("La IA te tocó un barco.")
                    if barcos_restantes(jugador) == 0:
                        perdiste = True
                else:
                    disparos_jugador[fila][col] = "X"
                    print("La IA falló. ¡Tu turno!")
                    turno_jugador = True
                break
    pantalla.fill((15, 15, 25))
    pantalla.blit(fuente.render("Tu tablero", True, (255, 255, 255)), (10,400))
    pantalla.blit(fuente.render("Tablero del enemigo", True, (255, 255, 255)), (400, 400))
    pantalla.blit(fuente.render("Tus barcos: " + str(barcos_restantes(jugador)), True, (255, 255, 255)), (10, 385))
    pantalla.blit(fuente.render("Barcos enemigos: " + str(barcos_restantes(enemigo)), True, (255, 255, 255)), (400, 385))
    dibujar_tablero(disparos_jugador, 10, 10, ver_barcos=True)
    dibujar_tablero(disparos_enemigo, 400, 10)
    if ganaste:
        texto_ganaste = pygame.font.SysFont("arial", 32).render("¡Ganaste!", True, (255, 215, 0))
        pantalla.blit(texto_ganaste, (285, 180))
    elif perdiste:
        texto_perdiste = pygame.font.SysFont("arial", 32).render("¡Perdiste!", True, (255, 80, 80))
        pantalla.blit(texto_perdiste, (280, 180))
    pygame.display.flip()
    reloj.tick(30)
pygame.quit()
sys.exit()