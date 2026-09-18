import math
import sys
import pygame
from core.datos import (
    angulo,
    disparos,
    gravedad,
    max_disparos,
    potencia,
    puntos,
    velocidad_blancos,
    viento,
)

pygame.init()
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
fuente = pygame.font.Font(None, 72)
reloj = pygame.time.Clock()
origen = (90, ALTO - 30) # posición del cañón
balas = [] # cada bala es un dict: x, y, vx, vy
blancos = [
    {
        "x": x,
        "y": 120 + indice * 55,
        "ancho": 60,
        "alto": 40,
        "vy": (1 if indice % 2 == 0 else -1) *
              (velocidad_blancos + (indice % 3) * 0.25)
    }
    for indice, x in enumerate(range(350, 850, 90))
]
def disparar(angulo):
    rad = math.radians(angulo)
    vx = potencia * math.cos(rad)
    vy = -potencia * math.sin(rad)
    balas.append({"x": origen[0], "y": origen[1], "vx": vx, "vy": vy})

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            angulo = math.degrees(math.atan2(origen[1] - my, mx - origen[0]))
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if disparos < max_disparos:
                disparar(angulo)
                disparos += 1

# Movimiento de los blancos
    for blanco in blancos:
        blanco["y"] += blanco["vy"]
        if blanco["y"] <= 80 or blanco["y"] >= ALTO - 130:
            blanco["vy"] *= -1
            blanco["y"] = max(80, min(blanco["y"], ALTO - 130))

# Física de cada bala
    for b in balas:
        b["vx"] += viento
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += gravedad
        if b["y"] < 10: # rebote en el techo
            b["vy"] *= -0.7
            b["y"] = 10
        if b["y"] > ALTO - 10: # rebote en el piso
            b["vy"] *= -0.7
            b["y"] = ALTO - 10

    for b in balas[:]:
        for blanco in blancos[:]:
                if (blanco["x"] <= b["x"] <= blanco["x"] + blanco["ancho"] and
                    blanco["y"] <= b["y"] <= blanco["y"] + blanco["alto"]):
                    centro_x = blanco["x"] + blanco["ancho"] / 2
                    centro_y = blanco["y"] + blanco["alto"] / 2
                    distancia = math.hypot(b["x"] - centro_x, b["y"] - centro_y)
                    distancia_maxima = math.hypot(
                        blanco["ancho"] / 2, blanco["alto"] / 2
                    )
                    precision = max(0, 1 - distancia / distancia_maxima)
                    puntos += int(10 + precision * 90)
                    blancos.remove(blanco)
                    balas.remove(b)
                    break
        

# Dibujar
    pantalla.fill((25, 25, 45))
    pygame.draw.rect(pantalla, (80, 220, 120), (0, ALTO - 10, ANCHO, 10))
    for blanco in blancos:
        pygame.draw.rect(pantalla, (220, 80, 80),
        (blanco["x"], blanco["y"], blanco["ancho"], blanco["alto"]))
    rad = math.radians(angulo)
    pygame.draw.line(pantalla, (240, 200, 60), origen,
                    (origen[0] + 60 * math.cos(rad),
                    origen[1] - 60 * math.sin(rad)), 6)
    for b in balas:
        pygame.draw.circle(pantalla, (240, 240, 240),
                            (int(b["x"]), int(b["y"])), 8)
    if not blancos:
        texto = fuente.render("Ganaste!", True, (255, 255, 255))
        rectangulo_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(texto, rectangulo_texto)
    municion = max_disparos - disparos
    pygame.display.set_caption(
        f"Cañones - Puntos: {puntos} - Munición: {municion}"
    )
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()
sys.exit()
