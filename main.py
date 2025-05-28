import pygame, sys, random, asyncio
from pygame.locals import *
from start_screen import start_screen
from menu_screen import menu_screen
pygame.init()
 

# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Window')




    



 
# The main function that controls the game
async def main () :
  
  state = "start"

  """INITIATE THE SCREENS"""
  start = start_screen()
  start.running = True

  menu = menu_screen()
  menu.running = False


  """MAIN GAME LOOP"""
  while True :

 
    """USER INPUT"""
    events = []
    for event in pygame.event.get() :
      events.append(event)
    

    """ACTIVATE SCREENS"""
    if start.running:
      state = start.run(events)
    
    if menu.running:
      state = menu.run(events)

    
    #State
    if state == "start":
      start.running = True
      menu.running = False
    elif state == "menu":
      start.running = False
      menu.running = True




 
    """UPDATE and FPS"""
    pygame.display.update()
    fpsClock.tick(FPS)

    await asyncio.sleep(0)

asyncio.run(main())