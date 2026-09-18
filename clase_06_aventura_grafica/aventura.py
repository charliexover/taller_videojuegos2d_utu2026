import sys
import pygame

pygame.init()
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 26)
tiene_banana = False
vidas = 3
fondo_inicio = pygame.image.load("clase_06_aventura_grafica/assets/1.png").convert()
fondo_inicio = pygame.transform.scale(fondo_inicio, (ANCHO, ALTO))
fondo_cueva = pygame.image.load("clase_06_aventura_grafica/assets/3.png").convert()
fondo_cueva = pygame.transform.scale(fondo_cueva, (ANCHO, ALTO))
fondo_rio = pygame.image.load("clase_06_aventura_grafica/assets/4.png").convert()
fondo_rio = pygame.transform.scale(fondo_rio, (ANCHO, ALTO))
sonido_opcion = pygame.mixer.Sound("clase_06_aventura_grafica/assets/Select.mp3")

historia = {
 "inicio": {
    "texto": "Estás en la selva. Escuchás un ruido entre los árboles.",
    "opciones": [("Ir a investigar", "cueva"), ("Seguir el sendero","rio")],
 },
 "cueva": {
    "texto": "Dentro de la cueva hay un cofre dorado. Un mono lo custodia.",
        "opciones": [("Hablar con el mono", "mono"), ("Abrir el cofre a escondidas", "cofre")],
 },
 "rio": {
     "texto": "Estás en el río. Ves un pirata con cara de malvado.",
         "opciones": [("Rezar tres padres nuestros", "pirata"), ("Correr de regreso a la selva", "inicio")],
  },
 "mono": {
    "texto": "El mono habla: '¡Dame una banana y el tesoro será tuyo!'",
        "opciones": (
            [("Dar la banana", "tesoro"), ("Negarme", "inicio")]
            if tiene_banana
            else [("Salir corriendo", "inicio")]
        ),
 },
 "tesoro": {
    "texto": "¡Ganaste el tesoro legendario de la selva! Fin de la aventura.",
 "opciones": [],
 },
 "cofre": {
     "texto": "El cofre era un monstruo que te devoró. Fin de la aventura.",
    "opciones": [("Volver al inicio", "inicio")],
  },
  "pirata": {
     "texto": "El pirata te ofrece una banana y se va.",
    "opciones": [("Agarras la banana y vuelves a la selva", "inicio")],
    },
 

}
# ======================================================
escena = "inicio"
fin_aventura = False
def dibujar_botones(opciones):
    botones = []
    y = ALTO - 40 * len(opciones) - 20
    for texto, _ in opciones:
        rect = pygame.Rect(ANCHO // 2 - 200, y, 400, 34)
        pygame.draw.rect(pantalla, (60, 60, 130), rect)
        pantalla.blit(fuente.render(texto, True, (255, 255, 255)), (rect.x + 12, rect.y + 6))
        botones.append((rect, texto))
        y += 44
    return botones

def dibujar_texto(texto, limite=45):
 palabras = texto.split()
 lineas, actual = [], ""
 for p in palabras:
    if len(actual) + len(p) + 1 > limite:
        lineas.append(actual)
        actual = p
    else:
        actual = actual + " " + p
 lineas.append(actual)
 y = 150
 for linea in lineas:
    pantalla.blit(fuente.render(linea, True, (255, 255, 255)), (80,y))
    y += 34

colores_fondo = {
    "inicio": (20, 30, 20),      # Selva
    "cueva": (35, 25, 45),       # Cueva
    "rio": (30, 80, 130),        # Río
    "mono": (90, 55, 25),        # Interior de la cueva
    "tesoro": (150, 110, 20),    # Tesoro
    "cofre": (100, 100, 100),    # Cofre
    "pirata": (100, 100, 100),   # Pirata
}

ejecutando = True
while ejecutando:
 if fin_aventura:
     opciones = []
 elif escena == "mono":
    opciones = (
        [("Dar la banana", "tesoro"), ("Negarme", "inicio")]
        if tiene_banana
        else [("Salir corriendo", "inicio")]
    )
 else:
    opciones = historia[escena]["opciones"]
 botones = dibujar_botones(opciones)
 for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
        ejecutando = False
    elif evento.type == pygame.MOUSEBUTTONDOWN and opciones:
        mx, my = pygame.mouse.get_pos()
        for i, (rect, _) in enumerate(botones):
            if rect.collidepoint(mx, my):
                sonido_opcion.play()
                if escena == "pirata":
                    tiene_banana = True
                if escena == "mono" and opciones[i][1] == "tesoro":
                    tiene_banana = False
                if opciones[i][1] == "cofre":
                    vidas -= 1
                    escena = "cofre"
                    if vidas == 0:
                        fin_aventura = True
                else:
                    escena = opciones[i][1] # ir a la escena elegida
                if not historia[escena]["opciones"]:
                    print("La aventura terminó.")
                break

 if escena == "inicio":
     pantalla.blit(fondo_inicio, (0, 0))
 elif escena == "cueva":
     pantalla.blit(fondo_cueva, (0, 0))
 elif escena == "rio":
     pantalla.blit(fondo_rio, (0, 0))
 else:
     pantalla.fill(colores_fondo[escena])
 pantalla.blit(fuente.render("AVENTURA EN LA SELVA", True, (255, 200,
60)), (80, 60))
 texto_banana = fuente.render("Banana: " + ("Sí" if tiene_banana else "No"), True, (255, 200, 60))
 texto_vidas = fuente.render("Vidas: " + str(vidas), True, (255, 200, 60))
 pantalla.blit(texto_banana, texto_banana.get_rect(topright=(ANCHO - 20, 100)))
 pantalla.blit(texto_vidas, texto_vidas.get_rect(topright=(ANCHO - 20, 134)))
 dibujar_texto(historia[escena]["texto"])
 if fin_aventura:
     mensaje_fin = fuente.render("fin de la aventura", True, (255, 80, 80))
     pantalla.blit(mensaje_fin, mensaje_fin.get_rect(center=(ANCHO // 2, 300)))
 dibujar_botones(opciones)
 pygame.display.flip()
 reloj.tick(30)
pygame.quit()
sys.exit()