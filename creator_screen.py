import pygame, sys, random, asyncio
from pygame.locals import *
from reference.classes_v2 import Button, Dropdown, Slider
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



class Song():
  def __init__(self, song):
    self.song = pygame.mixer.music.load(song)
    self.song_str = song.removesuffix(".ogg").removeprefix("songs/")

    if self.song_str == "Megalovania":
      self.BPM = 120

    self.position = 0
    self.offset = 0

  def play_song(self):
    pygame.mixer.music.play(1, start=round(self.position/1000.0, 5))

  def pause_song(self):
    self.position = pygame.mixer.music.get_pos() + self.offset
    self.offset = pygame.mixer.music.get_pos()
    pygame.mixer.music.stop()

  def set_position(self, position):
    self.position = position




class creator_screen:
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

    #Song
    self.song = None

    #Play Button
    self.paused = True
    self.play_btn = Button((570, 720), (60, 60), (0, 0, 0))
    self.play_btn.add_border(5, (255, 255, 255))

    #Song Dropdown
    self.dropdown_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)
    self.song_dropdown = Dropdown((400, 100), (400, 25), "Song", ["Megalovania", "Field of Hopes and Dreams", "Hunger"], self.dropdown_font)
    self.song_chosen = False

    #Song Bar
    self.measures = 164
    self.song_slider = Slider((1000, 20), (100, 690), (20, 40), 1, self.measures, 1)
    self.song_slider.change_slider(slider_rect_color=(255, 255, 255))

    #Measure Bar
    self.measure_slider = Slider((800, 15), (200, 650), (20, 40), 1, self.measures, 1)
    self.measure_slider.change_slider(slider_rect_color=(255, 255, 255))
    
    
  


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
    self.play_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
    if self.play_btn.check_press(self.mousePos, self.mouseUp):
      if self.paused:
        self.paused = False
        self.song.play_song()
      else:
        self.paused = True
        self.song.pause_song()

    self.song_dropdown.update(self.mousePos, self.mouseDown, self.mouseUp)
    if self.song == None and self.song_dropdown.value != "Song":
      self.song_chosen = True
      self.song = Song(f"songs/{self.song_dropdown.value}.ogg")
    elif self.song == None:
      pass
    elif self.song.song_str != self.song_dropdown.value:
      self.song = Song(f"songs/{self.song_dropdown.value}.ogg")
    
    self.song_slider.update(self.mousePos, self.mouseDown, self.mouseUp)
    self.measure_slider.update(self.mousePos, self.mouseDown, self.mouseUp)



    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)
    self.song_dropdown.draw(WINDOW)
    if self.song_chosen:
      self.play_btn.draw(WINDOW)
      pygame.draw.line(WINDOW, (255, 255, 255), (100, 700), (1100, 700), 5)
      self.song_slider.draw(WINDOW)
      self.measure_slider.draw(WINDOW)
    







'''


 
# The main function that controls the game
async def main () :

  """INITIATE THE SCREENS"""
  s1 = creator_screen()
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