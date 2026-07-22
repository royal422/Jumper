import pygame
import sys

pygame.init()

WIDTH=800
HEIGHT=500
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Jumper")
clock=pygame.time.Clock()

GROUND_Y=380

class Player:
    def __init__(self):
        self.x=100
        self.y=380
        self.vel_y=0
        self.on_ground=True
        
    def jump(self):
        if self.on_ground is True:
            self.vel_y=-14
            self.on_ground=False
            
    def update(self):
        self.vel_y+=0.6
        self.y+=self.vel_y
        if self.y>380:
            self.y=380
            self.on_ground=True
            
    def draw(self,surface):
        pygame.draw.rect(surface,(50,120,220),(self.x,self.y,40,50))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 50)


class Obstacle:
    def __init__(self,speed):
        self.x=800
        self.y=380
        self.speed=speed
        self.width=25
        self.height=45
        
    def update(self):
        self.x-=self.speed
    
    def draw(self,surface):
        pygame.draw.rect(surface,(220, 70, 70),(self.x,self.y,25,45))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    
def show_game_over(surface, score):
    end_font = pygame.font.SysFont("Arial", 48, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)
    
    surface.fill((30, 30, 30))
    title = end_font.render("GAME OVER", True, (220, 70, 70))
    sc = small_font.render(f"Score: {score // 60}", True, (240, 240, 240))
    restart = small_font.render("SPACE to play again  |  ESC to quit", True, (120, 120, 140))
    
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 160))
    surface.blit(sc, (WIDTH//2 - sc.get_width()//2, 230))
    surface.blit(restart, (WIDTH//2 - restart.get_width()//2, 280))
    

def show_start_screen(surface):
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    small_font = pygame.font.SysFont("Arial", 24)
    
    surface.fill((30, 30, 30))
    title = title_font.render("JUMPER", True, (50, 120, 220))
    start = small_font.render("Press SPACE to start", True, (240, 240, 240))
    
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 160))
    surface.blit(start, (WIDTH//2 - start.get_width()//2, 230))

def draw_background(surface, score):
    surface.fill((135, 206, 235))
    pygame.draw.line(surface, (60, 180, 60), (0, 430), (WIDTH, 430), 4)
    pygame.draw.rect(surface, (40, 120, 40), (0, 430, WIDTH, HEIGHT - 430))
    score_font = pygame.font.SysFont("Arial", 28, bold=True)
    score_text = score_font.render(f"Score: {score // 60}", True, (30, 30, 30))
    surface.blit(score_text, (20, 20))
    
 
player=Player()
obstacles=[]
score=0
speed=5
spawn_timer=0
state="start"

while True:
    clock.tick(60)
  
    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if state == "start":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = "playing"
            
        if state=="playing":
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    player.jump()
       
        if state == "lost":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player = Player()
                    obstacles = []
                    score = 0
                    spawn_timer = 0
                    state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()             
                    
                    
                    
    if state == "playing":
         player.update()
            
         spawn_timer += 1
         if spawn_timer >= 90:
            obstacles.append(Obstacle(speed))
            spawn_timer = 0
                
         for obs in obstacles:
            obs.update()
            if player.get_rect().colliderect(obs.get_rect()):
                state = "lost"
            
         obstacles = [obs for obs in obstacles if obs.x + obs.width > 0]
            
         score += 1
         
                    
    
    draw_background(screen, score)
    player.draw(screen)
    
    for obs in obstacles:
        obs.draw(screen)
        
    if state == "lost":
        show_game_over(screen, score)
        
    if state == "start":
        show_start_screen(screen)
    
    pygame.display.flip()
                    
