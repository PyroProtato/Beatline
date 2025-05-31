import pygame, sys, random, asyncio, math
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
      self.measures = 78
      self.time_signature = 4
    elif self.song_str == "Field of Hopes and Dreams":
      self.BPM = 125
      self.measures = 84
      self.time_signature = 4
    elif self.song_str == "Hunger":
      self.BPM = 86
      self.measures = 64 
      self.time_signature = 4
    self.measure_len = self.time_signature/(self.BPM/60)*1000

    self.position = 0
    self.offset = 0

    self.playing_measure = False
    self.playing = False
  
  def update(self):
    if self.playing_measure:
      if pygame.mixer.music.get_pos() > self.measure_len:
        self.pause_measure()
        self.playing_measure = False
    
    if not pygame.mixer.music.get_busy():
        self.playing = False
        self.position = 0
        self.offset = 0
    


  def play_song(self, measure=-1):
    self.playing = True
    print(measure)
    if measure == -1:
      pygame.mixer.music.play(1, start=round(self.position/1000.0, 5))
    else:
      self.position = (measure-1)*self.measure_len
      self.offset = self.position
      pygame.mixer.music.play(1, start=round(self.position/1000.0, 5))

  def pause_song(self):
    self.playing = False
    self.position = pygame.mixer.music.get_pos() + self.offset
    pygame.mixer.music.stop()

  def set_position(self, position):
    self.position = position
    self.offset = position
  
  def play_measure(self, measure):
    if self.playing_measure == False:
      self.position = (measure-1)*self.measure_len
      self.play_song()
      self.playing_measure = True
  
  def pause_measure(self):
    pygame.mixer.music.stop()




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
    self.play_btn_image = pygame.transform.scale(pygame.image.load("images/play_symbol.png"), (30, 30))
    self.play_btn_image_rect = self.play_btn_image.get_rect()
    self.play_btn_image_rect.center = (600, 750)
    self.pause_btn_image = pygame.transform.scale(pygame.image.load("images/pause_symbol.png"), (30, 30))
    self.pause_btn_image_rect = self.pause_btn_image.get_rect()
    self.pause_btn_image_rect.center = (600, 750)

    #Measure Button
    self.measure_btn = Button((650, 720), (60, 60), (0, 0, 0))
    self.measure_btn.add_border(5, (255, 255, 255))
    self.measure_btn_image = pygame.transform.scale(pygame.image.load("images/measure_play_symbol.png"), (50, 50))
    self.measure_btn_image_rect = self.measure_btn_image.get_rect()
    self.measure_btn_image_rect.center = (680, 750)

    #Song Dropdown
    self.dropdown_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)
    self.song_dropdown = Dropdown((400, 100), (400, 25), "Song", ["Megalovania", "Field of Hopes and Dreams", "Hunger"], self.dropdown_font)
    self.song_chosen = False
    self.previous_song = "Song"

    #Song Bar
    self.measures = 164
    self.song_slider = Slider((1000, 20), (100, 690), (20, 40), 1, self.measures, 1)
    self.song_slider.change_slider(slider_rect_color=(255, 255, 255))

    #Song Indicator
    self.measure_indicator = pygame.Rect(0, 600, 5, 55)

    #Measure Bar
    self.measure_slider = Slider((800, 5), (200, 625), (20, 40), 0, 4, 0)
    self.measure_slider.change_slider(slider_rect_color=(0, 0, 0), slider_border_color=(255, 255, 255))
    self.measure_slider.change_background(background_rect_border_color=(255, 255, 255))

    #Measure Indicator
    self.measure_indicator = pygame.Rect(0, 600, 5, 55)
    self.measure = 1


    #Subdivisions Dropdown
    self.subdivision = 4
    self.previous_sub_value = "Snap To..."
    self.subdropdown_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 15)
    self.sub_dropdown = Dropdown((200, 50), (25, 25), "Snap To...", ["1/2 Beat", "1/3 Beat", "1/4 Beat", "1/6 Beat", "1/8 Beat", "1/12 Beat", "1/16 Beat"], self.subdropdown_font)
    
    
  


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
        if self.measure == 0:
          self.song.play_song(-1)
        else:
          self.song_slider.step = self.measure
          self.song.play_song(self.measure)
      else:
        self.paused = True
        self.song.pause_song()

    #Updates Song
    if self.song_chosen:
      self.song.update()


    print(self.measure)
    #Measure Button
    self.measure_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
    if self.measure_btn.check_press(self.mousePos, self.mouseUp):
      self.song.play_measure(self.measure)
    

    #Song Dropdown
    self.song_dropdown.update(self.mousePos, self.mouseDown, self.mouseUp)
    if self.song == None and self.song_dropdown.value != "Song":
      self.song_chosen = True
      self.song = Song(f"songs/{self.song_dropdown.value}.ogg")
    elif self.song == None:
      pass
    elif self.song.song_str != self.song_dropdown.value:
      self.song = Song(f"songs/{self.song_dropdown.value}.ogg")
    if self.song_dropdown.value != self.previous_song: #Initializes
      self.song_slider = Slider((1000, 20), (100, 690), (20, 40), 1, self.song.measures, 1)
      self.song_slider.change_slider(slider_rect_color=(255, 255, 255))
    self.previous_song = self.song_dropdown.value

    self.sub_dropdown.update(self.mousePos, self.mouseDown, self.mouseUp)
    if self.song_chosen and self.previous_sub_value != self.sub_dropdown.value:
      self.subdivision = int(self.sub_dropdown.value.removeprefix("1/").removesuffix(" Beat"))
      self.measure_slider = Slider((800, 5), (200, 625), (20, 40), 0, self.subdivision, 0)
      self.measure_slider.change_slider(slider_rect_color=(0, 0, 0), slider_border_color=(255, 255, 255))
      self.measure_slider.change_background(background_rect_border_color=(255, 255, 255))
    self.previous_sub_value = self.sub_dropdown.value
    
    if self.song_chosen:
      self.song_slider.update(self.mousePos, self.mouseDown, self.mouseUp)
      self.measure = self.song_slider.step


    self.measure_slider.update(self.mousePos, self.mouseDown, self.mouseUp)
    if self.measure_slider.step == self.subdivision and self.measure_slider.on_mouse == False:
      if self.song_slider.step < self.song.measures:
        self.measure += 1
      self.measure_slider.step = 0

    #Makes Bars Move
    if self.song_chosen:
      if self.song.playing_measure:
        self.measure_indicator.centerx = self.measure_slider.x + round(pygame.mixer.music.get_pos()/self.song.measure_len*self.measure_slider.width)
      elif self.song.playing:
        self.measure = math.floor(((pygame.mixer.music.get_pos()+self.song.offset)/self.song.measure_len))+1
        self.measure_indicator.centerx = self.measure_slider.x + round(((pygame.mixer.music.get_pos()+self.song.offset)%self.song.measure_len)/self.song.measure_len*self.measure_slider.width)
      else:
        self.measure_indicator.centerx = self.measure_slider.x
    

    self.song_slider.step = self.measure



    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)
    self.song_dropdown.draw(WINDOW)
    if self.song_chosen:
      for i in range(self.subdivision):
        x = 200+i*self.measure_slider.width/self.subdivision
        pygame.draw.line(WINDOW, (255, 255, 255), (x, 650), (x, 665), 5)
      self.play_btn.draw(WINDOW)
      if not self.paused:
        WINDOW.blit(self.pause_btn_image, self.pause_btn_image_rect)
      else:
        WINDOW.blit(self.play_btn_image, self.play_btn_image_rect)
      self.measure_btn.draw(WINDOW)
      WINDOW.blit(self.measure_btn_image, self.measure_btn_image_rect)
      self.sub_dropdown.draw(WINDOW)
      self.song_slider.draw(WINDOW)
      self.measure_slider.draw(WINDOW)
      pygame.draw.rect(WINDOW, (255, 255, 255), self.measure_indicator)
      
    







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