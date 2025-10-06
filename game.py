import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# --- CONFIGURACIÓN ---
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recicla y gana")

# --- COLORES ---
VERDE = (50, 200, 50)
AZUL = (80, 160, 255)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
ROJO = (220, 50, 50)

fuente = pygame.font.SysFont("Arial", 28)

# --- VARIABLES ---
TAM_OBJETO = 40
velocidad = 8
tiempo_nuevo = 1000
reloj = pygame.time.Clock()

# --- FUNCIÓN PRINCIPAL DEL JUEGO ---
def jugar():
    # Reiniciar estado del juego
    contenedor = pygame.Rect(350, 520, 100, 50)
    objetos = []
    puntos = 0
    ultimo_tiempo = pygame.time.get_ticks()

    # --- INICIAR MÚSICA ---
    pygame.mixer.music.load("musica.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Repite en bucle

    # --- BUCLE DEL JUEGO ---
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and contenedor.left > 0:
            contenedor.x -= velocidad
        if teclas[pygame.K_RIGHT] and contenedor.right < ANCHO:
            contenedor.x += velocidad

        # --- Generar objetos ---
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - ultimo_tiempo > tiempo_nuevo:
            x = random.randint(0, ANCHO - TAM_OBJETO)
            tipo = random.choice(["reciclable", "basura"])
            color = VERDE if tipo == "reciclable" else ROJO
            objetos.append({
                "rect": pygame.Rect(x, 0, TAM_OBJETO, TAM_OBJETO),
                "tipo": tipo,
                "color": color
            })
            ultimo_tiempo = tiempo_actual

        # --- Mover objetos ---
        for obj in objetos:
            obj["rect"].y += 5

        # --- Colisiones ---
        for obj in objetos[:]:
            if contenedor.colliderect(obj["rect"]):
                if obj["tipo"] == "reciclable":
                    puntos += 1
                else:
                    puntos -= 1
                objetos.remove(obj)

        # --- Condición de derrota ---
        if puntos < -3:
            pygame.mixer.music.stop()  # Detener música
            return  # Salir del bucle y volver al menú

        # --- Eliminar los que salen de pantalla ---
        objetos = [o for o in objetos if o["rect"].y < ALTO]

        # --- Dibujar ---
        pantalla.fill(AZUL)
        pygame.draw.rect(pantalla, VERDE, (0, 570, ANCHO, 30))
        pygame.draw.rect(pantalla, GRIS, contenedor)

        for obj in objetos:
            pygame.draw.circle(pantalla, obj["color"], obj["rect"].center, TAM_OBJETO // 2)

        texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        pantalla.blit(texto, (10, 10))

        pygame.display.flip()
        reloj.tick(60)

# --- MENÚ PRINCIPAL ---
def menu():
    while True:
        pantalla.fill((0, 100, 180))
        texto_titulo = fuente.render("Recicla y Gana", True, BLANCO)
        texto_jugar = fuente.render("Presiona ESPACIO para jugar", True, BLANCO)
        texto_salir = fuente.render("Presiona ESC para salir", True, BLANCO)

        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 200))
        pantalla.blit(texto_jugar, (ANCHO // 2 - texto_jugar.get_width() // 2, 300))
        pantalla.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, 350))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugar()  # Comienza el juego
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# --- INICIO ---
menu()
