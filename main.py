import pygame, sys, random, asyncio
from pygame.locals import *
from start_screen import start_screen
from menu_screen import menu_screen
from game_screen import game_screen
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
  level = ""

  """INITIATE THE SCREENS"""
  start = start_screen()
  start.running = True

  menu = menu_screen()
  menu.running = False

  game = game_screen(level)
  game.running = False


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
      state, level = menu.run(events)
    
    if game.running:
      state = game.run(events)

    
    #Init State
    if state == "game_init":
      game = game_screen(level)
      state = "game"

    #State
    if state == "start":
      start.running = True
      menu.running = False
      game.running = False
    elif state == "menu":
      start.running = False
      menu.running = True
      game.running = False
    elif state == "game":
      start.running = False
      menu.running = False
      game.running = True




 
    """UPDATE and FPS"""
    pygame.display.update()
    fpsClock.tick(FPS)

    await asyncio.sleep(0)

asyncio.run(main())