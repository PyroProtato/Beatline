import pygame, sys, random, asyncio
from pygame.locals import *
from menu_screen import Level
pygame.init()
 
# Colours
COLOR_BACKGROUND = (0, 0, 0)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Window')




class Key:
  def __init__(self, key, key_str, coords):
    self.x = coords[0]
    self.y = coords[1]

    self.width = 100
    self.height = 100

    self.outline = pygame.Rect(self.x, self.y, self.width, self.height)

    self.key_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.text = self.key_font.render(key_str, True, (255, 255, 255))
    self.text_rect = self.text.get_rect()
    self.text_rect.center = (self.x+self.width//2, self.y+self.height//2)

    self.key = key



  def draw(self, surface):
    pygame.draw.rect(surface, (255, 255, 255), self.outline, 5)
    surface.blit(self.text, self.text_rect)

  








class game_screen:
  #Initializes all of the variables that are needed for the screen to work
  def __init__(self, level):

    #STATE
    self.running = False
    
    #COLORS
    self.color_bg = COLOR_BACKGROUND


    #USERINPUTS
    self.mouseIsDown = False
    self.mouseUp = False
    self.mouseDown = False
    self.mousePos = None

    #Param
    self.level = level

    #Keys
    self.j_key = Key(K_j, "J", (500, 500))
    self.k_key = Key(K_k, "K", (600, 500))
    self.l_key = Key(K_l, "L", (700, 500))
    self.semi_key = Key(K_SEMICOLON, ";", (800, 500))
  


  def run(self, events):
    
    """GETS USER INPUTS"""
    self.mouseDown = False
    self.mouseUp = False
    self.mousePos = pygame.mouse.get_pos()
    for event in events:
      if event.type == QUIT :
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        self.mouseIsDown = True
        self.mouseDown = True
      if event.type == MOUSEBUTTONUP:
        self.mouseIsDown = False
        self.mouseUp = True
    

    """PROCESSING"""



    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)

    self.level.draw(WINDOW)

    self.j_key.draw(WINDOW)
    self.k_key.draw(WINDOW)
    self.l_key.draw(WINDOW)
    self.semi_key.draw(WINDOW)


    return "game"








'''
 
# The main function that controls the game
async def main () :

  """INITIATE THE SCREENS"""
  s1 = game_screen(Level("Field of Hopes an...", "images/deltarune_fileselect.png", "Toby Fox", 2, 1))
  s1.running = True


  """MAIN GAME LOOP"""
  while True :


    """USER INPUT"""
    events = []
    for event in pygame.event.get() :
      events.append(event)
    

    """ACTIVATE SCREENS"""
    if s1.running:
      s1.run(events)




 
    """UPDATE and FPS"""
    pygame.display.update()
    fpsClock.tick(FPS)

    await asyncio.sleep(0)

asyncio.run(main())

'''