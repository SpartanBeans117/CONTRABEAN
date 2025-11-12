#Importamos la libreria Pygame
import pygame

# pantalla
pygame.init()
pantalla = pygame.display.set_mode((1280, 720))
fps = pygame.time.Clock()
juego = True


#plataforma
class plataforma:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 1280, 300)
        self.color = (0, 255, 0)
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

#personaje1
class personaje1:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x, y, 100, 100)#self se refiere asi mismo 
        self.color = (0, 0, 255)
        self.speed =5
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

#personaje2
class personaje2:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x, y, 100, 100)#self se refiere asi mismo 
        self.color = (255, 0, 0)
        self.speed = 5
    def draw(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

p1 = personaje1(400, 100) #posicion del personaje
p2 = personaje2(100, 100) #posicion del personaje
plataforma1 = plataforma(0,500) #posicion de la plataforma

while juego:
    # aqui es el bucle donde se iniciara el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

    # color del fondo
    pantalla.fill("black")

    ############# ESCENARIO #############
    pantalla.fill((0, 0, 0))
    
    #personajes
    p1.draw(pantalla) #dibuja el personaje2
    p2.draw(pantalla) #dibuja el personaje2

    #plataforma
    plataforma1.draw(pantalla) #dibuja la plataforma
    

    ############# ESCENARIO #############

    # actualiza la pantalla
    pygame.display.flip()
    fps.tick(60)  # FPS

pygame.quit()