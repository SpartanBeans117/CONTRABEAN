#Importamos la libreria Pygame
import pygame
import sqlite3 #importamos sqlite3 para guardar las rondas

# pantalla del juego
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True

########################## base de datos #################
#rondas
# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect("nderondas")
cursor = conn.cursor()
# Crear tabla rondas
cursor.execute("""
CREATE TABLE IF NOT EXISTS nderondas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personaje1 TEXT,
    rondas INTEGER
)
""")

cursor.execute("SELECT SUM(rondas) FROM nderondas WHERE personaje1 = ?", ("personaje1",))
total = cursor.fetchone()[0]
print("Total de rondas:", total)

conn.commit()
#################################### base de datos ###################

##########Proyectiles#############
class Proyectil:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = (0, 255, 0)
        # Calcular dirección normalizada hacia el centro
        dx = target_x - x
        dy = target_y - y
        mag = (dx**2 + dy**2) ** 0.5
        if mag != 0:
            self.vel_x = dx / mag * 8   # velocidad constante
            self.vel_y = dy / mag * 8
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
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (255, 0, 0)
        # Variables de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False   # bandera para saber si está en el suelo
        # Dash
        self.is_dashing = False
        self.dash_timer = 0
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
            self.vel_y = -12
            self.on_ground = False
    ####AtaqueA###
    def dash_to_center(self, screen_width):
        center_x = screen_width // 2
        if self.rect.centerx < center_x:
            self.vel_x = 15   # velocidad moderada
        else:
            self.vel_x = -15
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
    ####AtaqueB###
    def dash_to_centerb(self, screen_width):
        center_x = screen_width // 2
        if self.rect.centerx < center_x:
            self.vel_x = 15
            self.vel_y = -15 # velocidad moderada
        else:
            self.vel_x = -15
            self.vel_y = -15
        self.is_dashing = True
        self.dash_timer = 10   # frames que dura el dash (~1/3 seg a 60fps)
    #########actualizacion de ataque Dash####
    def update(self):
        # controlar duración del dash
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x = 0
    ##############Proyectiles##########
    def shoot_to_center(self, screen_width, screen_height, proyectiles):
        center_x = screen_width // 2
        center_y = screen_height // 2
        # Crear proyectil desde el centro del jugador
        nuevo = Proyectil(self.rect.centerx, self.rect.centery, center_x, center_y)
        proyectiles.append(nuevo)


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
        self.rect = pygame.Rect(x, y, 1280, 300)
        self.color = (0, 255, 0)
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
        
plataforma1 = plataforma(0,600) #posicion de la plataforma

jugador1 = jugador(100, 100)
screen_width = pantalla.get_width()
screen_height = pantalla.get_height()

########################JUEGO#####################
proyectiles = []
while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                jugador1.dash_to_center(pantalla.get_width())
            if event.key == pygame.K_LCTRL:
                jugador1.dash_to_centerb(pantalla.get_width())
            if event.key == pygame.K_x:
                jugador1.shoot_to_center(screen_width, screen_height, proyectiles)
    keys = pygame.key.get_pressed()
    jugador1.handle_movement(keys)  # mover jugador
    
    if keys[pygame.K_SPACE]:
        jugador1.jump()
    
    ######Proyectil################

    # Actualizar proyectiles
    for p in proyectiles:
        p.update()
        if (p.rect.right < 0 or p.rect.left > screen_width or 
            p.rect.bottom < 0 or p.rect.top > screen_height):
            proyectiles.remove(p)

    ######Proyectil###############




    jugador1.handle_movement(keys)
    jugador1.apply_gravity()
    jugador1.update()
    jugador1.check_collisions(plataforma1)
    #####limpiar pantalla##
    pantalla.fill((0,0,0))


    plataforma1.draw(pantalla)
    jugador1.draw(pantalla)
    for p in proyectiles:
        p.draw(pantalla)

    pygame.display.flip()
    fps.tick(60)


########################JUEGO#####################

# Guardar puntuación de ejemplo
cursor.execute("INSERT INTO nderondas (personaje1, rondas) VALUES (?, ?)", ("personaje1", 100))
conn.commit()
conn.close()

pygame.quit()