import sys
import pygame

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fondo = pygame.image.load("clase_05_el_mono/GrassLand_Background_1.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
tileset = pygame.image.load("clase_05_el_mono/Grassland_Terrain_47Tiles.png").convert_alpha()
tile_terreno = tileset.subsurface(pygame.Rect(16, 0, 16, 16)).copy()
tile_terreno = pygame.transform.scale(tile_terreno, (32, 32))
sonido_banana = pygame.mixer.Sound("clase_05_el_mono/Beepbee.wav")
sonido_salto = pygame.mixer.Sound("clase_05_el_mono/Waterjump.wav")
GRAVEDAD = 0.5
VEL_MOV = 6
FUERZA_SALTO = -13
fuente = pygame.font.Font(None, 32)
inicio_tiempo = pygame.time.get_ticks()
tiempo_final = None


def cargar_spritesheet(nombre, cantidad_cuadros):
    imagen = pygame.image.load(nombre).convert_alpha()
    ancho_cuadro = imagen.get_width() // cantidad_cuadros
    cuadros = []

    for i in range(cantidad_cuadros):
        cuadro = imagen.subsurface(pygame.Rect(i * ancho_cuadro, 0, ancho_cuadro, imagen.get_height()))
        cuadros.append(cuadro.copy())

    return cuadros


sprites_idle = cargar_spritesheet("clase_05_el_mono/male_hero-idle.png", 10)
sprites_saltar = cargar_spritesheet("clase_05_el_mono/male_hero-jump.png", 6)
sprites_correr = cargar_spritesheet("clase_05_el_mono/male_hero-run.png", 10)
sprites_hongo_idle = cargar_spritesheet("clase_05_el_mono/Mushroom-Idle.png", 7)
sprites_hongo_correr = cargar_spritesheet("clase_05_el_mono/Mushroom-Run.png", 8)
cuadro_actual = 0
animacion_actual = "idle"
ultimo_cambio_cuadro = pygame.time.get_ticks()
mirando_izquierda = False
mono = pygame.Rect(100, 300, 40, 40)
vel_x, vel_y = 0, 0
en_piso = False
niveles = [
    {
        "plataformas": [(0, 560, 800, 40), (150, 470, 180, 25), (400, 380, 180, 25), (620, 290, 150, 25)],
        "bananas": [(220, 430), (470, 340), (680, 250)],
        "enemigos": [(180, 440, 1, 2, 150, 300)],
    },
    {
        "plataformas": [(0, 560, 800, 40), (80, 450, 130, 25), (300, 350, 140, 25), (570, 430, 130, 25), (650, 250, 130, 25)],
        "bananas": [(130, 410), (360, 310), (620, 390), (700, 210)],
        "enemigos": [(110, 420, 1, 2, 80, 180), (330, 320, -1, 2, 300, 420), (590, 400, 1, 2, 570, 680)],
    },
    {
        "plataformas": [(0, 560, 140, 40), (220, 470, 110, 25), (430, 370, 100, 25), (620, 270, 100, 25), (400, 170, 120, 25), (650, 100, 120, 25)],
        "bananas": [(260, 430), (465, 330), (655, 230), (450, 130), (690, 60)],
        "enemigos": [(235, 440, 1, 2, 220, 300), (445, 340, -1, 2, 430, 510), (640, 240, 1, 2, 620, 700)],
    },
]
nivel_actual = 0


def cargar_nivel(numero):
    plataformas = [pygame.Rect(datos) for datos in niveles[numero]["plataformas"]]
    bananas = [pygame.Rect(x, y, 20, 20) for x, y in niveles[numero]["bananas"]]
    enemigos = []
    for x, y, direccion, velocidad, limite_izquierdo, limite_derecho in niveles[numero]["enemigos"]:
        enemigos.append({
            "rect": pygame.Rect(x, y, 30, 30),
            "direccion": direccion,
            "velocidad": velocidad,
            "limite_izquierdo": limite_izquierdo,
            "limite_derecho": limite_derecho,
            "cuadro": 0,
            "ultimo_cambio": 0,
            "pausa_hasta": 0,
            "animacion": "idle",
        })
    return plataformas, bananas, enemigos


plataformas, bananas, enemigos = cargar_nivel(nivel_actual)
juntas = 0
vidas = 3
invulnerable_hasta = 0

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and en_piso:
                vel_y = FUERZA_SALTO
                sonido_salto.play()

    if tiempo_final is None and vidas > 0:
        # Movimiento horizontal con teclado
        teclas = pygame.key.get_pressed()
        vel_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * VEL_MOV
        if vel_x < 0:
            mirando_izquierda = True
        elif vel_x > 0:
            mirando_izquierda = False

        # Gravedad y movimiento
        vel_y += GRAVEDAD
        mono.x += vel_x
        mono.y += vel_y

        # Colisión con plataformas
        en_piso = False
        for p in plataformas:
            if mono.colliderect(p) and vel_y > 0 and mono.bottom <= p.top + 15:
                mono.bottom = p.top
                vel_y = 0
                en_piso = True

        # Juntar bananas
        for b in bananas[:]:
            if mono.colliderect(b):
                bananas.remove(b)
                sonido_banana.play()
                juntas += 1

        ahora = pygame.time.get_ticks()
        for enemigo in enemigos:
            if ahora >= enemigo["pausa_hasta"]:
                enemigo["rect"].x += enemigo["direccion"] * enemigo["velocidad"]
                if enemigo["rect"].left <= enemigo["limite_izquierdo"] or enemigo["rect"].right >= enemigo["limite_derecho"]:
                    enemigo["rect"].left = max(enemigo["rect"].left, enemigo["limite_izquierdo"])
                    enemigo["rect"].right = min(enemigo["rect"].right, enemigo["limite_derecho"])
                    enemigo["direccion"] *= -1
                    enemigo["pausa_hasta"] = ahora + 250

        # Quitar una sola vida por contacto y devolver al mono al inicio.
        if ahora >= invulnerable_hasta:
            for enemigo in enemigos:
                if mono.colliderect(enemigo["rect"]):
                    vidas -= 1
                    mono.x = 100
                    mono.y = 300
                    vel_y = 0
                    invulnerable_hasta = ahora + 1000
                    break

        # Si se cae, reiniciar también el cronómetro.
        if mono.top > ALTO:
            mono.x = 100
            mono.y = 300
            vel_y = 0
            plataformas, bananas, enemigos = cargar_nivel(nivel_actual)
            juntas = 0
            inicio_tiempo = pygame.time.get_ticks()

        if len(bananas) == 0:
            if nivel_actual < len(niveles) - 1:
                nivel_actual += 1
                plataformas, bananas, enemigos = cargar_nivel(nivel_actual)
                mono.x = 100
                mono.y = 300
                vel_y = 0
                juntas = 0
                inicio_tiempo = pygame.time.get_ticks()
            else:
                tiempo_final = (pygame.time.get_ticks() - inicio_tiempo) // 1000

    if not en_piso:
        sprites_actuales = sprites_saltar
        nombre_animacion = "saltar"
    elif vel_x != 0:
        sprites_actuales = sprites_correr
        nombre_animacion = "correr"
    else:
        sprites_actuales = sprites_idle
        nombre_animacion = "idle"

    if nombre_animacion != animacion_actual:
        animacion_actual = nombre_animacion
        cuadro_actual = 0
        ultimo_cambio_cuadro = pygame.time.get_ticks()

    ahora = pygame.time.get_ticks()
    if ahora - ultimo_cambio_cuadro >= 100:
        cuadro_actual = (cuadro_actual + 1) % len(sprites_actuales)
        ultimo_cambio_cuadro = ahora

    # Dibujar
    pantalla.blit(fondo, (0, 0))
    for p in plataformas:
        area_original = pantalla.get_clip()
        pantalla.set_clip(p)
        for x in range(p.left, p.right, tile_terreno.get_width()):
            for y in range(p.top, p.bottom, tile_terreno.get_height()):
                pantalla.blit(tile_terreno, (x, y))
        pantalla.set_clip(area_original)
    sprite = sprites_actuales[cuadro_actual]
    if mirando_izquierda:
        sprite = pygame.transform.flip(sprite, True, False)
    posicion_sprite = sprite.get_rect(midtop=(mono.centerx, mono.bottom - 80))
    pantalla.blit(sprite, posicion_sprite)
    for b in bananas:
        pygame.draw.circle(pantalla, (255, 220, 60), b.center, 10)
    for enemigo in enemigos:
        en_pausa = pygame.time.get_ticks() < enemigo["pausa_hasta"]
        sprites_enemigo = sprites_hongo_idle if en_pausa else sprites_hongo_correr
        nombre_animacion_enemigo = "idle" if en_pausa else "correr"
        ahora = pygame.time.get_ticks()
        if nombre_animacion_enemigo != enemigo["animacion"]:
            enemigo["animacion"] = nombre_animacion_enemigo
            enemigo["cuadro"] = 0
            enemigo["ultimo_cambio"] = ahora
        if ahora - enemigo["ultimo_cambio"] >= 100:
            enemigo["cuadro"] = (enemigo["cuadro"] + 1) % len(sprites_enemigo)
            enemigo["ultimo_cambio"] = ahora
        sprite_enemigo = sprites_enemigo[enemigo["cuadro"]]
        if enemigo["direccion"] > 0:
            sprite_enemigo = pygame.transform.flip(sprite_enemigo, True, False)
        posicion_enemigo = sprite_enemigo.get_rect(midtop=(enemigo["rect"].centerx, enemigo["rect"].bottom - 64))
        pantalla.blit(sprite_enemigo, posicion_enemigo)
    segundos = tiempo_final if tiempo_final is not None else (pygame.time.get_ticks() - inicio_tiempo) // 1000
    texto_tiempo = fuente.render(f"Tiempo: {segundos} segundos", True, (20, 20, 20))
    pantalla.blit(texto_tiempo, (20, 20))
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, (20, 20, 20))
    pantalla.blit(texto_vidas, (20, 55))
    texto_nivel = fuente.render(f"Nivel: {nivel_actual + 1}", True, (20, 20, 20))
    pantalla.blit(texto_nivel, (20, 90))
    if tiempo_final is not None:
        texto_fin = fuente.render("¡Juntaste todas las bananas!", True, (20, 20, 20))
        pantalla.blit(texto_fin, (220, 70))
    elif vidas == 0:
        texto_fin = fuente.render("Game Over", True, (150, 20, 20))
        pantalla.blit(texto_fin, (340, 70))
    pygame.display.set_caption(f"El Mono - Bananas: {juntas}")
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()
sys.exit()
