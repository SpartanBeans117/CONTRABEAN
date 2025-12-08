#Importamos la libreria Pygame
import pygame
import sqlite3 #importamos sqlite3 para guardar las rondas
import math
from particle_system import ParticleSystem
import sys
import subprocess  # para ejecutar otro archivo Python
import os


# Carpeta base
BASE_DIR = os.path.dirname(__file__)
MUSICA_DIR = os.path.join(BASE_DIR, "musica")
SONIDOS_DIR = os.path.join(BASE_DIR, "sonidos")
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")
# pantalla del juego
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("escenario")
escenario = pygame.image.load(os.path.join(SPRITES_DIR, "escenario.png")).convert()

juego = True


# 🎵 Música
pygame.mixer.music.load(os.path.join(MUSICA_DIR, "musicajvj.mp3"))
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # loop infinito

# 🔊 Sonidos
choque_sound = pygame.mixer.Sound(os.path.join(SONIDOS_DIR, "choquesong.mp3"))
choque_sound.set_volume(0.3)

golpe_sound = pygame.mixer.Sound(os.path.join(SONIDOS_DIR, "golpesong.mp3"))
golpe_sound.set_volume(0.3)

patada_sound = pygame.mixer.Sound(os.path.join(SONIDOS_DIR, "patadasong.mp3"))
patada_sound.set_volume(0.3)

haduken_sound = pygame.mixer.Sound(os.path.join(SONIDOS_DIR, "hadukensong.mp3"))
haduken_sound.set_volume(0.3)

# 🎨 Sprites
plataforma_img = pygame.image.load(os.path.join(SPRITES_DIR, "plataforma.png")).convert_alpha()

# Jugador 1
jugador1_img = pygame.image.load(os.path.join(SPRITES_DIR, "elbean1.png")).convert_alpha()
jugador1_dash_img = pygame.image.load(os.path.join(SPRITES_DIR, "elbean1dash.png")).convert_alpha()

# Jugador 2
jugador2_img = pygame.image.load(os.path.join(SPRITES_DIR, "elbean2.png")).convert_alpha()
jugador2_dash_img = pygame.image.load(os.path.join(SPRITES_DIR, "elbean2dash.png")).convert_alpha()

# Proyectil
haduken_img = pygame.image.load(os.path.join(SPRITES_DIR, "haduken.png")).convert_alpha()
# Plataforma

#particulas
particle_systems = []

##########Proyectiles#############
class ProyectilP1:
    def __init__(self, x, y, target_x, target_y):
        original_image = pygame.image.load(os.path.join(SPRITES_DIR, "haduken.png")).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (100, 100))

        # Calcular dirección
        dx = target_x - x
        dy = target_y - y
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = dx / mag * 12
            self.vel_y = dy / mag * 12
        else:
            self.vel_x, self.vel_y = 0, 0

        # Decidir orientación SOLO UNA VEZ
        if target_x < x:
            # enemigo está a la izquierda → flip horizontal
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            # enemigo está a la derecha → normal
            self.image = self.original_image

        self.rect = self.image.get_rect(center=(x, y))
        
        haduken_sound.play()


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)


class ProyectilP2:
    def __init__(self, x, y, target_x, target_y):
        original_image = pygame.image.load(os.path.join(SPRITES_DIR, "haduken.png")).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (100, 100))

        # Calcular dirección
        dx = target_x - x
        dy = target_y - y
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = dx / mag * 12
            self.vel_y = dy / mag * 12
        else:
            self.vel_x, self.vel_y = 0, 0

        # Decidir orientación SOLO UNA VEZ
        if target_x < x:
            # enemigo está a la izquierda → flip horizontal
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            # enemigo está a la derecha → normal
            self.image = self.original_image

        self.rect = self.image.get_rect(center=(x, y))
        haduken_sound.play()


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)

##########Proyectiles#############

###########JUGADORES###########

class jugador:
    def __init__(self, x, y):
        ########################################
        # Sprite normal
        original_image = pygame.image.load(os.path.join(SPRITES_DIR, "elbean1.png")).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (150, 150))

        # Sprite de dash
        dash_image = pygame.image.load(os.path.join(SPRITES_DIR, "elbean1dash.png")).convert_alpha()
        self.dash_image = pygame.transform.scale(dash_image, (150, 150))

        # Imagen actual
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        ################################
        # Variables de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False   # bandera para saber si está en el suelo
        # Dash
        self.is_dashing = False
        self.dash_timer = 0
        # Cooldown del dash
        self.last_dash_time = 0
        self.DASH_COOLDOWN = 500  # 1 segundo
        # Cooldown del dashB
        self.last_dashb_time = 0
        self.DASHb_COOLDOWN = 500  # 1 segundo
        #Contador
        self.out_of_bounds_count = 0  # contador de veces que se sale
        ####Cooldown de disparo
        self.last_shot_time = 0
        self.SHOT_COOLDOWN = 800  # milisegundos (ejemplo: 0.8 segundos)
    ####Movimiento###
    def handle_movement(self, keys):
        if not self.is_dashing:  # solo mover normal si no está en dash
            self.vel_x = 0
            if keys[pygame.K_a]:
                self.vel_x = -5
            if keys[pygame.K_d]:
                self.vel_x = 5
        self.rect.x += self.vel_x
    ####Salto####
    def jump(self):
        if self.on_ground:   # flag que actualizas en colisiones
            self.vel_y = -20
            self.on_ground = False
    ####AtaqueA###
    def dash_to_player(self, jugador2):
############Cooldown dash###########
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time < self.DASH_COOLDOWN:
            return  # todavía en cooldown, no hacer nada
############Cooldown dash########
        # Calcular dirección hacia el otro jugador
        dx = jugador2.rect.centerx - self.rect.centerx
        dy = jugador2.rect.centery - self.rect.centery

        # Normalizar dirección para que la velocidad sea constante
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = int(dx / mag * 15)   # velocidad horizontal
        else:
            self.vel_x, self.vel_y = 0, 0
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
        self.image = self.dash_image   # 👈 Cambiar sprite al de dash
        #############
        self.last_dash_time = current_time  # actualizar cooldown
        ###############
        golpe_sound.play()
    ####AtaqueB###
    def dash_to_playerb(self, jugador2):
############Cooldown dash###########
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dashb_time < self.DASHb_COOLDOWN:
            return  # todavía en cooldown, no hacer nada
############Cooldown dash########
        # Calcular dirección hacia el otro jugador
        dx = jugador2.rect.centerx - self.rect.centerx
        dy = jugador2.rect.centery - self.rect.centery

        # Normalizar dirección para que la velocidad sea constante
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = int(dx / mag * 30)   # velocidad horizontal
        else:
            self.vel_x, self.vel_y = 0, 0
            
            # Forzar un pequeño impulso hacia arriba
        self.vel_y -= 10   # valor negativo = salto
            
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
        self.image = self.dash_image
        #############
        self.last_dashb_time = current_time  # actualizar cooldown
        ###############
        patada_sound.play()
    #########actualizacion de ataque Dash####
    def update(self):
        # controlar duración del dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x = 0
                self.image = self.original_image   # 👈 Volver al sprite normal

        # Teletransporte si sale de la pantalla
        if (self.rect.right < 0 or self.rect.left > screen_width):
            self.rect.center = (screen_width // 2, screen_height // 2)
            self.vel_x = 0
            self.vel_y = 0
            self.out_of_bounds_count += 1  # 🚀 sumar al contador
##########actualizacion del sentido del sprite
    def update_orientation(self, otro_jugador):
        # Si está en dash, no cambiar sprite
        if self.is_dashing:
            if otro_jugador.rect.centerx < self.rect.centerx:
                # Otro jugador está a la izquierda → dash normal
                self.image = self.dash_image
            else:
                # Otro jugador está a la derecha → dash volteado
                self.image = pygame.transform.flip(self.dash_image, True, False)
            return
        # Comparar horizontal
        if otro_jugador.rect.centerx < self.rect.centerx:
            # Otro jugador está a la izquierda → flip horizontal
            self.image = self.original_image
            
        else:
            # Otro jugador está a la derecha → normal
            self.image = pygame.transform.flip(self.original_image, True, False)


    ####Gravedad####
    def apply_gravity(self):
        # gravedad constante
        self.vel_y += 0.8
        # límite para no caer demasiado rápido
        if self.vel_y > 15:
            self.vel_y = 15
        self.rect.y += self.vel_y

    ####Colisiones####
    def check_collisions(self, plataforma):
        # si el jugador toca la plataforma por abajo
        if self.rect.colliderect(plataforma.rect):
            # solo corregimos si está cayendo
            if self.vel_y >= 0:
                self.rect.bottom = plataforma.rect.top
                self.vel_y = 0
                self.on_ground = True
                # Crear partículas 
                ps = ParticleSystem(
                    x=self.rect.centerx,
                    y=self.rect.bottom,
                    count=25,          # cantidad de partículas
                    lifetime=30,       # duración en frames
                    speed=2,           # velocidad inicial
                    color=(0,255,255) # azul
                )
                particle_systems.append(ps)
        
        else:
            self.on_ground = False

    ####Dibujar jugador####
    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)



class jugador2:
    def __init__(self, x, y):
        ########################################
        # Sprite normal
        original_image = pygame.image.load(os.path.join(SPRITES_DIR, "elbean2.png")).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (150, 150))

        # Sprite de dash
        dash_image = pygame.image.load(os.path.join(SPRITES_DIR, "elbean2dash.png")).convert_alpha()
        self.dash_image = pygame.transform.scale(dash_image, (150, 150))

        # Imagen actual
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        ################################
        # Variables de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False   # bandera para saber si está en el suelo
        # Dash
        self.is_dashing = False
        self.dash_timer = 0
        # Cooldown del dash
        self.last_dash_time = 0
        self.DASH_COOLDOWN = 500  # 1 segundo
        # Cooldown del dashB
        self.last_dashb_time = 0
        self.DASHb_COOLDOWN = 500  # 1 segundo
        #Contador
        self.out_of_bounds_count = 0  # contador de veces que se sale
        ####Cooldown de disparo
        self.last_shot_time = 0
        self.SHOT_COOLDOWN = 800  # milisegundos (ejemplo: 0.8 segundos)
    ####Movimiento###
    def handle_movement(self, keys):
        if not self.is_dashing:  # solo mover normal si no está en dash
            self.vel_x = 0
            if keys[pygame.K_LEFT]:
                self.vel_x = -5
            if keys[pygame.K_RIGHT]:
                self.vel_x = 5

        self.rect.x += self.vel_x
    ####Salto####
    def jump(self):
        if self.on_ground:   # flag que actualizas en colisiones
            self.vel_y = -20
            self.on_ground = False
    ####AtaqueA###
    def dash_to_player(self, jugador1):
############Cooldown dash###########
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dash_time < self.DASH_COOLDOWN:
            return  # todavía en cooldown, no hacer nada
############Cooldown dash########
        # Calcular dirección hacia el otro jugador
        dx = jugador1.rect.centerx - self.rect.centerx
        dy = jugador1.rect.centery - self.rect.centery

        # Normalizar dirección para que la velocidad sea constante
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = int(dx / mag * 15)   # velocidad horizontal
        else:
            self.vel_x, self.vel_y = 0, 0
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
        self.image = self.dash_image   # 👈 Cambiar sprite al de dash
        #############
        self.last_dash_time = current_time  # actualizar cooldown
        ###############
        golpe_sound.play()
    ####AtaqueB###
    def dash_to_playerb(self, jugador1):
############Cooldown dash###########
        current_time = pygame.time.get_ticks()
        if current_time - self.last_dashb_time < self.DASHb_COOLDOWN:
            return  # todavía en cooldown, no hacer nada
############Cooldown dash########
        # Calcular dirección hacia el otro jugador
        dx = jugador1.rect.centerx - self.rect.centerx
        dy = jugador1.rect.centery - self.rect.centery

        # Normalizar dirección para que la velocidad sea constante
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = int(dx / mag * 30)   # velocidad horizontal
        else:
            self.vel_x, self.vel_y = 0, 0
            
            # Forzar un pequeño impulso hacia arriba
        self.vel_y -= 10   # valor negativo = salto
            
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
        self.image = self.dash_image
        #############
        self.last_dashb_time = current_time  # actualizar cooldown
        ###############
        patada_sound.play()
    #########actualizacion de ataque Dash####
    def update(self):
        # controlar duración del dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x = 0

        # Teletransporte si sale de la pantalla
        if (self.rect.right < 0 or self.rect.left > screen_width):
            self.rect.center = (screen_width // 2, screen_height // 2)
            self.vel_x = 0
            self.vel_y = 0
        #contador
            self.out_of_bounds_count += 1  #  sumar al contador
##########actualizacion del sentido del sprite
    def update_orientation(self, otro_jugador):
        #sprite del dashing
        if self.is_dashing:
            if otro_jugador.rect.centerx < self.rect.centerx:
                # Otro jugador está a la izquierda → dash normal
                self.image = self.dash_image
            else:
                # Otro jugador está a la derecha → dash volteado
                self.image = pygame.transform.flip(self.dash_image, True, False)
            return
        # Comparar horizontal
        if otro_jugador.rect.centerx < self.rect.centerx:
            # Otro jugador está a la izquierda → flip horizontal
            self.image = self.original_image
        else:
            # Otro jugador está a la derecha → normal
            self.image = pygame.transform.flip(self.original_image, True, False)




    ####Gravedad####
    def apply_gravity(self):
        # gravedad constante
        self.vel_y += 0.8
        # límite para no caer demasiado rápido
        if self.vel_y > 15:
            self.vel_y = 15
        self.rect.y += self.vel_y

    ####Colisiones####
    def check_collisions(self, plataforma):
        # si el jugador toca la plataforma por abajo
        if self.rect.colliderect(plataforma.rect):
            # solo corregimos si está cayendo
            if self.vel_y >= 0:
                self.rect.bottom = plataforma.rect.top
                self.vel_y = 0
                self.on_ground = True
                # Crear partículas 
                ps = ParticleSystem(
                    x=self.rect.centerx,
                    y=self.rect.bottom,
                    count=25,          # cantidad de partículas
                    lifetime=30,       # duración en frames
                    speed=2,           # velocidad inicial
                    color=(255,0,0) # rojo
                )
                particle_systems.append(ps)

        else:
            self.on_ground = False
    ####Dibujar jugador####
    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)


###########JUGADORES###########

#plataforma
class plataforma:
    def __init__(self, x, y):
        # Cargar sprite de la plataforma
        original_image = pygame.image.load(os.path.join(SPRITES_DIR, "plataforma.png")).convert_alpha()
        self.image = pygame.transform.scale(original_image, (1280, 216))
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def draw(self, pantalla):
        pantalla.blit(self.image, self.rect)
        

########Colisiones Mecanica##################
####Colision de jugadores
def check_player_collision(j1, j2):
    if j1.rect.colliderect(j2.rect):
        # Vector entre jugadores
        dx = j2.rect.centerx - j1.rect.centerx
        dy = j2.rect.centery - j1.rect.centery
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

            KNOCKBACK = 10  # fuerza del dash

            # Jugador 1 retrocede en dirección contraria
            j1.vel_x = -dx * KNOCKBACK
            j1.vel_y = -dy * KNOCKBACK

            # Jugador 2 retrocede en dirección contraria
            j2.vel_x = dx * KNOCKBACK
            j2.vel_y = dy * KNOCKBACK

            # Activar estado de dash temporal
            j1.is_dashing = True
            j1.dash_timer = 8
            j2.is_dashing = True
            j2.dash_timer = 8

            # 🔥 Crear partículas de choque en el punto medio
            cx = (j1.rect.centerx + j2.rect.centerx) // 2
            cy = (j1.rect.centery + j2.rect.centery) // 2
            ps = ParticleSystem(
                x=cx,
                y=cy,
                count=30,          # cantidad de partículas
                lifetime=20,       # duración en frames
                speed=10,           # velocidad inicial
                color=(255, 255, 0) # color rojo/naranja tipo chispa
            )
            particle_systems.append(ps)
            # Reproduce el sonido del choque
            choque_sound.play()

########Colision de jugadores
########Colision de Proyectiles a J
def check_projectile_collision(player, projectile, knockback=10):
    if player.rect.colliderect(projectile.rect):
        # Vector entre jugador y proyectil
        dx = projectile.rect.centerx - player.rect.centerx
        dy = projectile.rect.centery - player.rect.centery
        distancia = (dx**2 + dy**2) ** 0.5

        if distancia != 0:
            dx /= distancia
            dy /= distancia

            # Aplicar knockback al jugador
            player.vel_x = -dx * knockback
            player.vel_y = -dy * knockback

            # Activar estado de dash temporal (igual que en colisión de jugadores)
            player.is_dashing = True
            player.dash_timer = 8
            # 🔥 Crear partículas de choque en el punto medio
            cx = (player.rect.centerx + projectile.rect.centerx) // 2
            cy = (player.rect.centery + projectile.rect.centery) // 2
            ps = ParticleSystem(
                x=cx,
                y=cy,
                count=30,          # cantidad de partículas
                lifetime=20,       # duración en frames
                speed=10,           # velocidad inicial
                color=(0, 200, 255) # color rojo/naranja tipo chispa
            )
            particle_systems.append(ps)  # 👈 añadir a la lista global
            choque_sound.play()
        # Eliminar proyectil tras impacto
        return True

    return False
########Colision de Proyectiles a J

########Colisiones Mecanica################
#########Reiniciar juego
def reiniciar_juego():
    # Reiniciar posiciones iniciales
    jugador1.rect.topleft = (100, 300)   # posición inicial jugador 1
    jugador2.rect.topleft = (1100, 300)   # posición inicial jugador 2

    # Reiniciar puntuaciones
    jugador1.out_of_bounds_count = 0
    jugador2.out_of_bounds_count = 0

    # Reiniciar velocidades
    jugador1.vel_x = 0
    jugador1.vel_y = 0
    jugador2.vel_x = 0
    jugador2.vel_y = 0
    #eliminar proyectiles
    proyectiles_p1.clear()
    proyectiles_p2.clear()
############


plataforma1 = plataforma(0,500) #posicion de la plataforma

jugador1 = jugador(610, 100)
jugador2 = jugador2(610, 100)
screen_width = pantalla.get_width()
screen_height = pantalla.get_height()

#almacen de proyectiles
proyectiles_p1 = []
proyectiles_p2 = []
#FPS
fps = pygame.time.Clock()
FPS = 60 
########################JUEGO#####################
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        ######Atajos de reiniciar y menu
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_m:
            if event.key == pygame.K_r:  # Tecla R reinicia puntuación y posición
                reiniciar_juego()
                    # Presionar Enter
            #volver al menu
            if event.key == pygame.K_t:
                juego = False
                pygame.mixer.music.stop()   # 👈 detener música al salir                
                pygame.quit()   # 👈 cerrar ventana del menú
                subprocess.run(["python", "menu.py"])
                sys.exit()
        ######Controles del jugador
            if event.key == pygame.K_b:
                jugador1.dash_to_player(jugador2)
            if event.key == pygame.K_n:
                jugador1.dash_to_playerb(jugador2)
            if event.key == pygame.K_m:
                current_time = pygame.time.get_ticks()
                if current_time - jugador1.last_shot_time >= jugador1.SHOT_COOLDOWN:
                    proyectiles_p1.append(ProyectilP1(jugador1.rect.centerx, jugador1.rect.centery,
                                                    jugador2.rect.centerx, jugador2.rect.centery))
                    jugador1.last_shot_time = current_time



        ######COntroles del jugador 2
            if event.key == pygame.K_KP1:
                jugador2.dash_to_player(jugador1)
            if event.key == pygame.K_KP2:
                jugador2.dash_to_playerb(jugador1)
            # Jugador 2 dispara
            if event.key == pygame.K_KP3:
                current_time = pygame.time.get_ticks()
                if current_time - jugador2.last_shot_time >= jugador2.SHOT_COOLDOWN:
                    proyectiles_p2.append(ProyectilP2(jugador2.rect.centerx, jugador2.rect.centery,
                                                    jugador1.rect.centerx, jugador1.rect.centery))
                    jugador2.last_shot_time = current_time

            #if event.key == pygame.K_KP3:
                
    keys = pygame.key.get_pressed()
    jugador1.handle_movement(keys)  # mover jugador
    jugador2.handle_movement(keys)  # mover jugador
    
    if keys[pygame.K_w]:
        jugador1.jump()
    if keys[pygame.K_UP]:
        jugador2.jump()
    



    # Dibujar el sprite como fondo
    pantalla.blit(escenario, (0, 0))
    # Actualizar y dibujar partículas
    for ps in particle_systems[:]:
        ps.update()
        ps.draw(pantalla)
        if not ps.is_alive():
            particle_systems.remove(ps)
#######Jugador 1
    jugador1.handle_movement(keys)
    jugador1.apply_gravity()
    jugador1.update()
    jugador1.check_collisions(plataforma1)

#######Jugador 2
    jugador2.handle_movement(keys)
    jugador2.apply_gravity()
    jugador2.update()
    jugador2.check_collisions(plataforma1)
    
######Mecanica de colisiones
    check_player_collision(jugador1, jugador2)

########Sentidos del sprite
    jugador1.update_orientation(jugador2)
    jugador2.update_orientation(jugador1)
########Sentidos del sprite haduken


    ######Proyectil################
    for p in proyectiles_p1:
        p.update()
        p.draw(pantalla)
        if check_projectile_collision(jugador2, p, knockback=12):
            # knockback jugador2
            jugador2.vel_x += p.vel_x * 0.5
            jugador2.vel_y += p.vel_y * 0.5
            proyectiles_p1.remove(p)

    for p in proyectiles_p2:
        p.update()
        p.draw(pantalla)
        if check_projectile_collision(jugador1, p, knockback=12):
            # knockback jugador1
            jugador1.vel_x += p.vel_x * 0.5
            jugador1.vel_y += p.vel_y * 0.5
            proyectiles_p2.remove(p)
    ######Proyectil###############
    

#####Contador
    # Crear fuente
    font = pygame.font.SysFont(None, 100)

    # Texto jugador1
    texto_j1 = font.render(f" {jugador1.out_of_bounds_count}", True, (255,0,0))
    pantalla.blit(texto_j1, (640, 20))
###texto divsor
    divisor = font.render(f"-", True, (0,0,0))
    pantalla.blit(divisor, (615, 20))

    # Texto jugador2
    texto_j2 = font.render(f" {jugador2.out_of_bounds_count}", True, (0,0,255))
    pantalla.blit(texto_j2, (500, 20))


    plataforma1.draw(pantalla)
    jugador1.draw(pantalla)
    jugador2.draw(pantalla)

    pygame.display.flip()
    fps.tick(FPS)


########################JUEGO#####################

pygame.quit()
sys.exit()