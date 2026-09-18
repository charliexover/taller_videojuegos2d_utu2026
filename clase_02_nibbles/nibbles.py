import random
import sys
import pygame

pygame.init()
ANCHO, ALTO = 600, 600
CELDA = 30
COLUMNAS = ANCHO // CELDA
FILAS = ALTO // CELDA
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# El cuerpo: lista de (columna, fila). La cabeza es el primer elemento.
serpiente = [(5, 5)]
direccion = (1, 0) # (dx, dy) -> derecha
def manzana_nueva():
 while True:
    m = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS -1))
    if m not in serpiente:
        return m
manzana = manzana_nueva()
manzana_dorada = None
puntos = 0

def dibujar_celda(pos, color):
    pygame.draw.rect(pantalla, color,(pos[0] * CELDA, pos[1] * CELDA, CELDA - 2, CELDA -2))

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
        # No dejar que gire 180 grados (no puede ir para atrás)
            if evento.key == pygame.K_UP and direccion != (0, 1):
                direccion = (0, -1)
            elif evento.key == pygame.K_DOWN and direccion != (0, -1):
                direccion = (0, 1)
            elif evento.key == pygame.K_LEFT and direccion != (1, 0):
                direccion = (-1, 0)
            elif evento.key == pygame.K_RIGHT and direccion != (-1, 0):
                direccion = (1, 0)

    # 1) Nueva cabeza
    cabeza = (
        serpiente[0][0] + direccion[0], 
        serpiente[0][1] + direccion[1])
    serpiente.insert(0, cabeza)

    # 2) ¿Comió?
    if cabeza == manzana_dorada:
        puntos += 5
        manzana_dorada = None
    elif cabeza == manzana:
        puntos += 1
        manzana = manzana_nueva()
        if manzana_dorada is None and random.random() < 0.10:
            manzana_dorada = manzana_nueva()
    else:
        serpiente.pop() # no comió -> se achica por el final

    # 3) ¿Chocó con el borde o consigo misma?
    if (
        cabeza[0] < 0 
        or cabeza[0] >= COLUMNAS 
        or cabeza[1] < 0 
        or cabeza[1] >= FILAS 
        or cabeza in serpiente[1:]):
        ejecutando = False

    # 4) Dibujar
    pantalla.fill((10, 10, 15))
    for segmento in serpiente:
        dibujar_celda(segmento, (0, 220, 60))
    dibujar_celda(manzana, (230, 40, 40))
    if manzana_dorada is not None:
        dibujar_celda(manzana_dorada, (255, 215, 0))
    pygame.display.set_caption(f"Puntos: {puntos}")
    pygame.display.flip()
    reloj.tick(5) # 10 FPS: velocidad clásica

try:
    with open("record.txt") as f:
        record = int(f.read())
except FileNotFoundError:
    record = 0
if puntos > record:
    record = puntos
    with open("record.txt", "w") as f:
        f.write(str(record))

pygame.quit()
print(f"Fin del juego. Puntos: {puntos}")
sys.exit()
