#Importamos la libreria Pygame
import pygame
import sqlite3 #importamos sqlite3 para guardar las rondas
import math

# pantalla del juego
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True



##########Proyectiles#############
class ProyectilP1:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (255, 0, 0)  # rojo
        dx = target_x - x
        dy = target_y - y
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = dx / mag * 12
            self.vel_y = dy / mag * 12
        else:
            self.vel_x, self.vel_y = 0, 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)


class ProyectilP2:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (0, 0, 255)  # azul
        dx = target_x - x
        dy = target_y - y
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = dx / mag * 15
            self.vel_y = dy / mag * 15
        else:
            self.vel_x, self.vel_y = 0, 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
##########Proyectiles#############

###########JUGADORES###########

class jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.color = (255, 0, 0)
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
        # Control de color temporal
        self.color_change_time = 0  # guarda el momento en que cambió el color
        #Contador
        self.out_of_bounds_count = 0  # contador de veces que se sale
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
        #self.color = (0, 255, 0)  # verde
        self.color_change_time = pygame.time.get_ticks()  # momento del cambio
        #############
        self.last_dash_time = current_time  # actualizar cooldown
        ###############
    ####AtaqueB###
    def dash_to_playerb(self, jugador2):
        if self.on_ground:   # solo si está en el suelo
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
            self.on_ground = False
            #self.color = (0, 0, 255)  # azul
            self.color_change_time = pygame.time.get_ticks()
    #########actualizacion de ataque Dash####
    def update(self):
        # controlar duración del dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x = 0
        # cambio al color
        if self.color_change_time != 0:
            if pygame.time.get_ticks() - self.color_change_time >= 400:  # 1000 ms = 1 seg
                self.color = (255, 0, 0) #rojo
                self.color_change_time = 0  # reset para evitar que se repita
        # Teletransporte si sale de la pantalla
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.rect.center = (screen_width // 2, screen_height // 2)
            self.vel_x = 0
            self.vel_y = 0
            self.out_of_bounds_count += 1  # 🚀 sumar al contador


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
        else:
            self.on_ground = False

    ####Dibujar jugador####
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

class jugador2:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.color = (0, 255, 255)
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
        # Control de color temporal
        self.color_change_time = 0  # guarda el momento en que cambió el color
        #Contador
        self.out_of_bounds_count = 0  # contador de veces que se sale

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
        #self.color = (0, 255, 0)  # verde
        self.color_change_time = pygame.time.get_ticks()  # momento del cambio
        #############
        self.last_dash_time = current_time  # actualizar cooldown
        ###############
    ####AtaqueB###
    def dash_to_playerb(self, jugador1):
        if self.on_ground:   # solo si está en el suelo
            # Calcular dirección hacia el otro jugador
            dx = jugador1.rect.centerx - self.rect.centerx
            dy = jugador1.rect.centery - self.rect.centery

            # Normalizar dirección para que la velocidad sea constante
            mag = (dx**2) ** 0.5
            if mag != 0:
                self.vel_x = int(dx / mag * 30)   # velocidad horizontal

            else:
                self.vel_x, self.vel_y = 0, 0
            
            # Forzar un pequeño impulso hacia arriba
            self.vel_y -= 10   # valor negativo = salto
            
            self.is_dashing = True
            self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
            self.on_ground = False
            #self.color = (0, 0, 255)  # azul
            self.color_change_time = pygame.time.get_ticks()
    #########actualizacion de ataque Dash####
    def update(self):
        # controlar duración del dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x = 0
        # cambio al color
        if self.color_change_time != 0:
            if pygame.time.get_ticks() - self.color_change_time >= 400:  # 1000 ms = 1 seg
                self.color = (0, 255, 255) #rojo
                self.color_change_time = 0  # reset para evitar que se repita
        # Teletransporte si sale de la pantalla
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.rect.center = (screen_width // 2, screen_height // 2)
            self.vel_x = 0
            self.vel_y = 0
        #contador
            self.out_of_bounds_count += 1  #  sumar al contador



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
        else:
            self.on_ground = False
    ####Dibujar jugador####
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

###########JUGADORES###########

#plataforma
class plataforma:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 1280, 500)
        self.color = (0, 255, 0)
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        

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

        # Eliminar proyectil tras impacto
        return True
    return False
########Colision de Proyectiles a J

########Colisiones Mecanica################

plataforma1 = plataforma(0,500) #posicion de la plataforma

jugador1 = jugador(610, 100)
jugador2 = jugador2(610, 100)
screen_width = pantalla.get_width()
screen_height = pantalla.get_height()

#almacen de proyectiles
proyectiles_p1 = []
proyectiles_p2 = []

########################JUEGO#####################
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        ######Controles del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                jugador1.dash_to_player(jugador2)
            if event.key == pygame.K_n:
                jugador1.dash_to_playerb(jugador2)
            if event.key == pygame.K_m:  # ejemplo: tecla M para jugador1
                proyectiles_p1.append(ProyectilP1(jugador1.rect.centerx, jugador1.rect.centery,
                                                    jugador2.rect.centerx, jugador2.rect.centery))
            #if event.key == pygame.K_m:

        ######COntroles del jugador 2
            if event.key == pygame.K_KP1:
                jugador2.dash_to_player(jugador1)
            if event.key == pygame.K_KP2:
                jugador2.dash_to_playerb(jugador1)
            if event.key == pygame.K_KP3:  # ejemplo: tecla NumPad3 para jugador2
                proyectiles_p2.append(ProyectilP2(jugador2.rect.centerx, jugador2.rect.centery,
                                                    jugador1.rect.centerx, jugador1.rect.centery))
            #if event.key == pygame.K_KP3:
                
    keys = pygame.key.get_pressed()
    jugador1.handle_movement(keys)  # mover jugador
    jugador2.handle_movement(keys)  # mover jugador
    
    if keys[pygame.K_w]:
        jugador1.jump()
    if keys[pygame.K_UP]:
        jugador2.jump()
    




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

#####limpiar pantalla##
    pantalla.fill((0,0,0))

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
    font = pygame.font.SysFont(None, 36)

    # Texto jugador1
    texto_j1 = font.render(f"Jugador1: {jugador1.out_of_bounds_count}", True, (255,0,0))
    pantalla.blit(texto_j1, (540, 20))

    # Texto jugador2
    texto_j2 = font.render(f"Jugador2: {jugador2.out_of_bounds_count}", True, (0,255,255))
    pantalla.blit(texto_j2, (540, 60))


    plataforma1.draw(pantalla)
    jugador1.draw(pantalla)
    jugador2.draw(pantalla)

    pygame.display.flip()
    fps.tick(60)


########################JUEGO#####################



pygame.quit()