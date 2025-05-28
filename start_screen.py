import pygame, sys, random, asyncio
from pygame.locals import *
from reference.classes_v2 import Button
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


class start_screen:
  #Initializes all of the variables that are needed for the screen to work
  def __init__(self):

    #STATE
    self.running = False
    
    #COLORS
    self.color_bg = COLOR_BACKGROUND


    #USERINPUTS
    self.mouseIsDown = False
    self.mouseUp = False
    self.mouseDown = False
    self.mousePos = None

    #Title
    self.title_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 100)
    self.title = self.title_font.render("BEATLINE", True, (255, 255, 255))
    self.title_rect = self.title.get_rect()
    self.title_rect.center = (600, 125)

    #Play Button
    self.play_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.play_button = Button((450, 400), (300, 100), (0, 0, 0))
    self.play_button.add_border(5, (255, 255, 255))
    self.play_button.add_text(self.play_font, "Play", (255, 255, 255))
  


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
    self.play_button.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
    if self.play_button.check_press(self.mousePos, self.mouseUp):
      return "menu"



    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)

    pygame.draw.line(WINDOW, (255, 255, 255), (400, 160), (825, 160), 1)
    pygame.draw.line(WINDOW, (255, 255, 255), (400, 135), (825, 135), 1)
    pygame.draw.line(WINDOW, (255, 255, 255), (400, 110), (825, 110), 1)
    pygame.draw.line(WINDOW, (255, 255, 255), (400, 85), (825, 85), 1)
    WINDOW.blit(self.title, self.title_rect)
    pygame.draw.line(WINDOW, (255, 255, 255), (825, 75), (825, 200), 5)
    pygame.draw.line(WINDOW, (255, 255, 255), (400, 175), (850, 175), 5)

    self.play_button.draw(WINDOW)

    return "start"










'''
 
# The main function that controls the game
async def main () :

  """INITIATE THE SCREENS"""
  s1 = start_screen()
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