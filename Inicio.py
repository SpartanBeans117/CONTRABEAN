#Importamos la libreria Pygame
import pygame
import sqlite3 #importamos sqlite3 para guardar las rondas

# pantalla
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True
############# base de datos #################
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
####################### base de datos ###################

#plataforma
class plataforma:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 1280, 300)
        self.color = (0, 255, 0)
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

#personaje1
class personaje1:
    def __init__(self,x,y, suelo_y):
        self.rect = pygame.Rect(x, y, 100, 100)#self se refiere asi mismo 
        self.color = (0, 0, 255)
        self.speed = 1
        self.velocidad_y = 0        # vertical
        self.gravedad = 0.009         # fuerza de gravedad
        self.suelo_y = suelo_y  
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
    ### Movimiento ##
    def movimientop(self, objetos):
        keys = pygame.key.get_pressed()  # detecta teclas presionadas
        if keys[pygame.K_LEFT]:   # mover izquierda
            self.rect.x -= self.speed
            #colision
            for obj in objetos:
                if self.rect.colliderect(obj.rect):
                    self.rect.left = obj.rect.right
                    
        if keys[pygame.K_RIGHT]:  # mover derecha
            self.rect.x += self.speed
            ##colision
            for obj in objetos:
                if self.rect.colliderect(obj.rect):
                    self.rect.right = obj.rect.left
        ##colision vertical
        
        
    def salto(self):
        if self.velocidad_y == 0:   # solo si está en el suelo
            self.velocidad_y = -2
### gravedad ###
    def gravedadp(self, objetos):
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

    # colisión con el suelo
        if self.rect.y >= self.suelo_y:
            self.rect.y = self.suelo_y
            self.velocidad_y = 0
    # colisión con plataformas
        for obj in objetos:
            if self.rect.colliderect(obj.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = obj.rect.top
                    self.velocidad_y = 0
                elif self.velocidad_y < 0:
                    self.rect.top = obj.rect.bottom
                    self.velocidad_y = 0



#personaje2
class personaje2:
    def __init__(self,x,y, suelo_y):
        self.rect = pygame.Rect(x, y, 100, 100)#self se refiere asi mismo 
        self.color = (255, 0, 0)
        self.speed = 1
        self.velocidad_y = 0 # vertical
        self.velocidad_x = 0 #horizontal
        self.gravedad = 0.009         # fuerza de gravedad
        self.suelo_y = suelo_y  
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)
    ### Movimiento ##
    def movimientop(self, objetos):
        keys = pygame.key.get_pressed()  # detecta teclas presionadas
        if keys[pygame.K_a]:   # mover izquierda
            self.rect.x -= self.speed
            for obj in objetos:
                if self.rect.colliderect(obj.rect):
                    self.rect.left = obj.rect.right
        if keys[pygame.K_d]:  # mover derecha
            self.rect.x += self.speed
            ###colision
            for obj in objetos:
                if self.rect.colliderect(obj.rect):
                    self.rect.right = obj.rect.left
    def salto(self):
        if self.velocidad_y == 0:   # solo si está en el suelo
            self.velocidad_y = -2
### gravedad ###
    def gravedadp(self,objetos):
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y

    # colisión con el suelo
        if self.rect.y >= self.suelo_y:
            self.rect.y = self.suelo_y
            self.velocidad_y = 0
##colision de objetos
        for obj in objetos:
            if self.rect.colliderect(obj.rect):
                if self.velocidad_y > 0:
                    self.rect.bottom = obj.rect.top
                    self.velocidad_y = 0
                elif self.velocidad_y < 0:
                    self.rect.top = obj.rect.bottom
                    self.velocidad_y = 0

p1 = personaje1(200, 50, suelo_y=500)
p2 = personaje2(100, 50, suelo_y=500) #posicion del personaje
plataforma1 = plataforma(0,600) #posicion de la plataforma

while juego:
    # aqui es el bucle donde se iniciara el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p1.salto()   # aquí sí sobre la instancia
            if event.key == pygame.K_w:
                p2.salto()   # aquí sí sobre la instancia


    # color del fondo
    pantalla.fill("black")

    ############# ESCENARIO #############
    pantalla.fill((0, 0, 0))
    
    #personajes
    p1.draw(pantalla) #dibuja el personaje2
    p2.draw(pantalla) #dibuja el personaje2
    
    # actualizar movimiento del personaje1
    
    #cOLISIONES
    p1.movimientop([plataforma1, p2])
    p1.gravedadp([plataforma1, p2])
    p2.movimientop([plataforma1, p1])
    p2.gravedadp([plataforma1, p1])


    #plataforma
    plataforma1.draw(pantalla) #dibuja la plataforma
    

    ############# ESCENARIO #############

    # actualiza la pantalla
    pygame.display.flip()
    


# Guardar puntuación de ejemplo
cursor.execute("INSERT INTO nderondas (personaje1, rondas) VALUES (?, ?)", ("personaje1", 100))
conn.commit()
conn.close()

pygame.quit()