import sys
import random
from pathlib import Path
import pygame
from pygame import mixer

pygame.init()
ANCHO, ALTO = 800, 600
MARGEN_BORDE = 15
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 72)
ruta_fondo = Path(__file__).resolve().parent / "assets" / "bg-arkanoid.png"
fondo = pygame.image.load(ruta_fondo).convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
sonido_rebote = mixer.Sound('clase_04_arkanoid/assets/SFX1.wav')
sonido_ladrillo_especial = mixer.Sound('clase_04_arkanoid/assets/SFX5.wav')
pala = pygame.Rect(ANCHO // 2 - 60, ALTO - 40, 120, 15)
pelota = pygame.Rect(ANCHO // 2 - 8, ALTO // 2, 16, 16)
vel_x, vel_y = 5, -5

# Ladrillos: una fila de rectángulos
FILAS, COLS = 4, 10
colores_fila = [(255, 80, 80), (255, 170, 60), (100, 200, 100), (80, 160, 255)]
puntajes_fila = [40, 30, 20, 10]
ANCHO_LADRILLO = 70
ESPACIO_LADRILLOS = 7
ancho_formacion = COLS * ANCHO_LADRILLO + (COLS - 1) * ESPACIO_LADRILLOS
inicio_ladrillos = MARGEN_BORDE + (ANCHO - 2 * MARGEN_BORDE - ancho_formacion) // 2
ladrillos = []
for fila in range(FILAS):
    for col in range(COLS):
        posicion_x = inicio_ladrillos + col * (ANCHO_LADRILLO + ESPACIO_LADRILLOS)
        rectangulo = pygame.Rect(posicion_x, fila * 30 + 40, ANCHO_LADRILLO, 20)
        ladrillos.append((rectangulo, fila))
fila_especial = random.randrange(FILAS)
col_especial = random.randrange(COLS)
ladrillo_especial = pygame.Rect(
    inicio_ladrillos + col_especial * (ANCHO_LADRILLO + ESPACIO_LADRILLOS),
    fila_especial * 30 + 40,
    ANCHO_LADRILLO,
    20,
)
ladrillos = [
    (ladrillo, fila)
    for ladrillo, fila in ladrillos
    if ladrillo != ladrillo_especial
]
vidas = 3
puntos = 0
ladrillos_destruidos = 0
ejecutando = True
pelotas = [
    {"rect": pelota, "vel_x": vel_x, "vel_y": vel_y, "es_original": True}
]


def mostrar_cuenta_regresiva():
    for mensaje in ("3", "2", "1", "YA"):
        inicio = pygame.time.get_ticks()
        while pygame.time.get_ticks() - inicio < 1000:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False

            pantalla.blit(fondo, (0, 0))
            pygame.draw.rect(pantalla, (90, 180, 255), pala)
            for ladrillo, fila in ladrillos:
                pygame.draw.rect(pantalla, colores_fila[fila], ladrillo)
            if ladrillo_especial is not None:
                pygame.draw.rect(pantalla, (255, 255, 0), ladrillo_especial)

            texto = fuente.render(mensaje, True, (255, 255, 255))
            pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
            pygame.display.flip()
            reloj.tick(60)
    return True


while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Paleta sigue al mouse
    pala.x = pygame.mouse.get_pos()[0] - pala.width // 2
    pala.x = max(MARGEN_BORDE, min(ANCHO - MARGEN_BORDE - pala.width, pala.x))

    pelotas_nuevas = []
    pelotas_para_eliminar = []
    pelota_perdida = False
    for pelota_actual in pelotas:
        pelota = pelota_actual["rect"]
        vel_x = pelota_actual["vel_x"]
        vel_y = pelota_actual["vel_y"]

        pelota.x += vel_x
        pelota.y += vel_y

        if pelota.left <= MARGEN_BORDE:
            pelota.left = MARGEN_BORDE
            vel_x = abs(vel_x)
        elif pelota.right >= ANCHO - MARGEN_BORDE:
            pelota.right = ANCHO - MARGEN_BORDE
            vel_x = -abs(vel_x)
        if pelota.top <= MARGEN_BORDE:
            pelota.top = MARGEN_BORDE
            vel_y = abs(vel_y)
        if pelota.colliderect(pala) and vel_y > 0:
            posicion_impacto = (pelota.centerx - pala.left) / pala.width
            velocidad_horizontal = max(abs(vel_x), 1)
            if posicion_impacto < 1 / 3:
                vel_x = -velocidad_horizontal
            elif posicion_impacto > 2 / 3:
                vel_x = velocidad_horizontal
            else:
                vel_x = 0
            vel_y = -abs(vel_y)
            sonido_rebote.play()

        if ladrillo_especial is not None and pelota.colliderect(ladrillo_especial):
            sonido_ladrillo_especial.play()
            ladrillo_especial = None
            for desplazamiento in (-3, 3):
                pelotas_nuevas.append(
                    {
                        "rect": pelota.copy(),
                        "vel_x": vel_x + desplazamiento,
                        "vel_y": vel_y,
                        "es_original": False,
                    }
                )
            vel_y *= -1
        else:
            for ladrillo, fila in ladrillos[:]:
                if pelota.colliderect(ladrillo):
                    ladrillos.remove((ladrillo, fila))
                    puntos += puntajes_fila[fila]
                    ladrillos_destruidos += 1
                    if ladrillos_destruidos % 5 == 0:
                        vel_x += 1 if vel_x > 0 else -1
                        vel_y += 1 if vel_y > 0 else -1
                    vel_y *= -1
                    break

        if pelota.bottom >= ALTO:
            if pelota_actual["es_original"]:
                pelota_perdida = True
                pelota.center = (ANCHO // 2, ALTO // 2)
                vel_x, vel_y = 5, -5
            else:
                pelotas_para_eliminar.append(pelota_actual)

        pelota_actual["vel_x"] = vel_x
        pelota_actual["vel_y"] = vel_y

    for pelota_actual in pelotas_para_eliminar:
        pelotas.remove(pelota_actual)
    pelotas.extend(pelotas_nuevas)
    if pelota_perdida:
        vidas -= 1
        if vidas == 0:
            ejecutando = False
        elif not mostrar_cuenta_regresiva():
            ejecutando = False

    if len(ladrillos) == 0 and ladrillo_especial is None:
        print("\u00a1Ganaste!")
        ejecutando = False

    # Dibujar
    pantalla.blit(fondo, (0, 0))
    pygame.draw.rect(pantalla, (90, 180, 255), pala)
    for pelota_actual in pelotas:
        pygame.draw.rect(pantalla, (255, 255, 255), pelota_actual["rect"])
    for ladrillo, fila in ladrillos:
        pygame.draw.rect(pantalla, colores_fila[fila], ladrillo)
    if ladrillo_especial is not None:
        pygame.draw.rect(pantalla, (255, 255, 0), ladrillo_especial)
    if len(ladrillos) == 0 and ladrillo_especial is None:
        texto = fuente.render("\u00a1Ganaste!", True, (255, 255, 255))
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2)))
    pygame.display.set_caption(
        f"Arkanoid - Vidas: {vidas} - Puntos: {puntos} - Ladrillos:{len(ladrillos)}"
    )
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()
sys.exit()
