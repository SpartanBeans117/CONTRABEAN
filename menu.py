"""El codigo fue hecho por mi y IA
Mi nombre es Juan Diego Jauregui Bonilla
Librerias utilizadas, pygame, math, particleSystem, sys, subprocess y os.
Hecho en python 3.13.2"""
#Aqui creamos el menu del juego, tiene como objetivo mandarnos al juego
import pygame #base del juego
import sys
import subprocess #cargar otro programa
import os #buscar archivos


# Carpeta base y subcarpeta de musica
BASE_DIR = os.path.dirname(__file__)
MUSICA_DIR = os.path.join(BASE_DIR, "musica")
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")
# pantalla del juego
pygame.init()
pantalla = pygame.display.set_mode((1280, 720)) #resolucion de la pantalla
pygame.display.set_caption("menu")
menu = pygame.image.load(os.path.join(SPRITES_DIR, "menu.png")).convert() #elige el sprite menu y lo busca
fps = pygame.time.Clock()
juego = True

# Carpeta base y subcarpeta de musica
BASE_DIR = os.path.dirname(__file__)
MUSICA_DIR = os.path.join(BASE_DIR, "musica") #busca la musica en la carpeta

# Cargar musica del menu
pygame.mixer.music.load(os.path.join(MUSICA_DIR, "menusong.mp3"))
pygame.mixer.music.set_volume(0.4)  # volumen entre 0.0 y 1.0
pygame.mixer.music.play(-1)         # -1 = loop infinito

# Fuente y boton
font = pygame.font.SysFont(None, 60)
color_boton = (0, 128, 255) #color del boton
color_texto = (255, 255, 255) #color del texto

# Rectángulo del boton
boton_rect = pygame.Rect(490, 400, 280, 100) #tamaño y posicion
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
                pygame.mixer.music.stop()   # detener musica al salir                
                pygame.quit()   #cerrar ventana del menu
                subprocess.run(["python", "Contrabean.py"])
                sys.exit()
        # Presionar Enter
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                juego = False
                pygame.mixer.music.stop()   #detener musica al salir                
                pygame.quit()   #cerrar ventana del menu
                subprocess.run(["python", "contrabean.py"])
                sys.exit()
    # Dibujar el sprite como fondo
    pantalla.blit(menu, (0, 0))
    # Dibujar el boton encima
    pygame.draw.rect(pantalla, color_boton, boton_rect)
    pantalla.blit(texto, (boton_rect.x + 70, boton_rect.y + 30))
    pygame.display.flip()
    fps.tick(60) #fotogramas del juego

pygame.quit()
sys.exit()
