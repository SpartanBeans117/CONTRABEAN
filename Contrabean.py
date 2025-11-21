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


###########JUGADORES###########

class jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (255, 0, 0)
        # Variables de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False   # bandera para saber si está en el suelo
    ####Movimiento###
    def handle_movement(self, keys):
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
    ####Ataque###
    def dash_to_center(self, screen_width):
        center_x = screen_width // 2
        if self.rect.centerx < 640:
            self.vel_x = 15   # impulso hacia la derecha
        else:
            self.vel_x = -15  # impulso hacia la izquierda
    # opcional: un pequeño boost vertical
        self.vel_y = -5

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

########################JUEGO#####################

while juego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                jugador1.dash_to_center(pantalla.get_width())
    keys = pygame.key.get_pressed()
    jugador1.handle_movement(keys)  # mover jugador
    
    if keys[pygame.K_SPACE]:
        jugador1.jump()



    
    jugador1.apply_gravity()
    jugador1.check_collisions(plataforma1)
    #####limpiar pantalla##
    pantalla.fill((0,0,0))


    plataforma1.draw(pantalla)
    jugador1.draw(pantalla)

    pygame.display.flip()
    fps.tick(60)


########################JUEGO#####################

# Guardar puntuación de ejemplo
cursor.execute("INSERT INTO nderondas (personaje1, rondas) VALUES (?, ?)", ("personaje1", 100))
conn.commit()
conn.close()

pygame.quit()