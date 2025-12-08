import pygame
import sys
import subprocess  # para ejecutar otro archivo Python
import os


# Carpeta base y subcarpeta de música
BASE_DIR = os.path.dirname(__file__)
MUSICA_DIR = os.path.join(BASE_DIR, "musica")
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")
# pantalla del juego
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("menu")
menu = pygame.image.load(os.path.join(SPRITES_DIR, "menu.png")).convert()
fps = pygame.time.Clock()
juego = True

# Carpeta base y subcarpeta de música
BASE_DIR = os.path.dirname(__file__)
MUSICA_DIR = os.path.join(BASE_DIR, "musica")

# 🎵 Cargar música del menú
pygame.mixer.music.load(os.path.join(MUSICA_DIR, "menusong.mp3"))
pygame.mixer.music.set_volume(0.4)  # volumen entre 0.0 y 1.0
pygame.mixer.music.play(-1)         # -1 = loop infinito

# Fuente y botón
font = pygame.font.SysFont(None, 60)
color_boton = (0, 128, 255)
color_texto = (255, 255, 255)

# Rectángulo del botón
boton_rect = pygame.Rect(490, 400, 280, 100)
texto = font.render("J1vsJ2", True, color_texto)


screen_width = pantalla.get_width()
screen_height = pantalla.get_height()

while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
            
        # Click con el mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(event.pos):
                juego = False
                pygame.mixer.music.stop()   # 👈 detener música al salir                
                pygame.quit()   # 👈 cerrar ventana del menú
                subprocess.run(["python", "Contrabean.py"])
                sys.exit()
        # Presionar Enter
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                juego = False
                pygame.mixer.music.stop()   # 👈 detener música al salir                
                pygame.quit()   # 👈 cerrar ventana del menú
                subprocess.run(["python", "contrabean.py"])
                sys.exit()
    # Dibujar el sprite como fondo
    pantalla.blit(menu, (0, 0))
    # Dibujar el botón encima
    pygame.draw.rect(pantalla, color_boton, boton_rect)
    pantalla.blit(texto, (boton_rect.x + 70, boton_rect.y + 30))

    pygame.display.flip()
    fps.tick(60)
    

pygame.quit()
sys.exit()
