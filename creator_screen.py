import pygame, sys, random, asyncio, math
from pygame.locals import *
from reference.classes_v2 import Button, Dropdown, Slider, MultilineText
from menu_screen import Level
pygame.init()
 
# Colours
COLOR_BACKGROUND = (0, 0, 0)
 
# Game Setup
FPS = 30
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




class Key:
  def __init__(self, key, key_str, coords):
    self.x = coords[0]
    self.y = coords[1]

    self.width = 100
    self.height = 100

    self.key_str = key_str

    self.activated_color = (255, 255, 255)
    self.deactivated_color = (150, 150, 150)
    self.chosen_color = (255, 255, 50)

    self.outline = Button((self.x, self.y), (self.width, self.height), (0, 0, 0))
    self.key_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.outline.add_text(self.key_font, key_str, self.deactivated_color)
    self.outline.add_border(5, self.deactivated_color)

    self.key = key
    self.beat1 = False

    self.activated = False

    self.playing = False

  
  def beat(self):
    self.beat1 = True

  def has_beat(self):
    self.outline.add_border(5, self.chosen_color)

  def no_beat(self):
    self.outline.add_border(5, self.activated_color)


  def update(self, mousePos, mousePressed):
    self.outline.update((100, 100, 100), (50, 50, 50), mousePos, mousePressed)
  
  def check_press(self, mousePos, mouseUp):
    if self.outline.check_press(mousePos, mouseUp):
      self.activated = True
      self.outline.add_text(self.key_font, self.key_str, self.activated_color)
      return True
    return False

  def draw(self, surface):
    if self.activated:
      if self.beat1:
        self.beat1 = False
        self.outline.add_border(5, self.chosen_color)
    self.outline.draw(surface)




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

    #Previous Measure Icon
    self.prev_measure_btn = Button((25, 670), (60, 60), (0, 0, 0))
    self.prev_measure_btn.add_border(5, (255, 255, 255))
    self.prev_measure_btn_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/next_icon.png"), (40, 40)), True, False)
    self.prev_measure_btn_image_rect = self.prev_measure_btn_image.get_rect()
    self.prev_measure_btn_image_rect.center = (55, 700)

    #Next Measure Icon
    self.next_measure_btn = Button((1115, 670), (60, 60), (0, 0, 0))
    self.next_measure_btn.add_border(5, (255, 255, 255))
    self.next_measure_btn_image = pygame.transform.scale(pygame.image.load("images/next_icon.png"), (40, 40))
    self.next_measure_btn_image_rect = self.next_measure_btn_image.get_rect()
    self.next_measure_btn_image_rect.center = (1145, 700)

    #Previous Song Icon
    self.prev_song_btn = Button((25, 600), (60, 60), (0, 0, 0))
    self.prev_song_btn.add_border(5, (255, 255, 255))
    self.prev_song_btn_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/next_icon.png"), (40, 40)), True, False)
    self.prev_song_btn_image_rect = self.prev_song_btn_image.get_rect()
    self.prev_song_btn_image_rect.center = (55, 630)

    #Next Song Icon
    self.next_song_btn = Button((1115, 600), (60, 60), (0, 0, 0))
    self.next_song_btn.add_border(5, (255, 255, 255))
    self.next_song_btn_image = pygame.transform.scale(pygame.image.load("images/next_icon.png"), (40, 40))
    self.next_song_btn_image_rect = self.next_song_btn_image.get_rect()
    self.next_song_btn_image_rect.center = (1145, 630)

    #Test Icon
    self.test_btn = Button((1115, 250), (60, 60), (0, 0, 0))
    self.test_btn.add_border(5, (255, 255, 255))
    self.test_btn_image = pygame.transform.scale(pygame.image.load("images/game_icon.png"), (40, 40))
    self.test_btn_image_rect = self.test_btn_image.get_rect()
    self.test_btn_image_rect.center = (1145, 280)

    #Song Dropdown
    self.dropdown_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)
    self.song_dropdown = Dropdown((400, 100), (400, 25), "Song", ["Megalovania", "Field of Hopes and Dreams", "Hunger"], self.dropdown_font)
    self.song_chosen = False
    self.previous_song = "Song"

    #Song Bar
    self.measures = 164
    self.song_slider = Slider((1000, 20), (100, 690), (20, 40), 1, self.measures, 1)
    self.song_slider.change_slider(slider_rect_color=(255, 255, 255))
    self.prev_song_slider = self.song_slider.step

    #Song Indicator
    self.measure_indicator = pygame.Rect(0, 600, 5, 55)

    #Measure Bar
    self.measure_slider = Slider((800, 5), (200, 625), (20, 40), 0, 4, 0)
    self.measure_slider.change_slider(slider_rect_color=(0, 0, 0), slider_border_color=(255, 255, 255))
    self.measure_slider.change_background(background_rect_border_color=(255, 255, 255))
    self.measure_init_empty = True

    #Measure Indicator
    self.measure_indicator = pygame.Rect(0, 600, 5, 55)
    self.measure = 1

    #Back Button
    self.back_btn = Button((20, 20), (60, 60), (0, 0, 0))
    self.back_btn.add_border(5, (255, 255, 255))
    self.back_btn_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("images/next_icon.png"), (40, 40)), True, False)
    self.back_btn_image_rect = self.back_btn_image.get_rect()
    self.back_btn_image_rect.center = (50, 50)


    #Subdivisions Dropdown
    self.subdivision = 4
    self.previous_sub_value = "Snap To..."
    self.subdropdown_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 15)
    self.sub_dropdown = Dropdown((200, 50), (125, 25), "Snap To...", ["1/2 Beat", "1/3 Beat", "1/4 Beat", "1/6 Beat", "1/8 Beat", "1/12 Beat", "1/16 Beat"], self.subdropdown_font)

    #Data
    self.data = [[None, [[] for x in range(self.subdivision)]] for y in range(self.measures)]

    #measure Text
    self.measure_text_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)
    self.measure_text = self.measure_text_font.render(f"Measure: {self.measure}", True, (255, 255, 255))
    self.measure_text_rect = self.measure_text.get_rect()
    self.measure_text_rect.midleft = (600,50)

    #Keys
    self.keys = []
    #self.keys.append(Key(K_j, "J", (200, 300)))
    #self.keys.append(Key(K_k, "K", (400, 300)))
    #self.keys.append(Key(K_l, "L", (600, 300)))

    self.keys.append(Key(K_j, "J", (750, 400)))
    self.keys.append(Key(K_k, "K", (850, 400)))
    self.keys.append(Key(K_l, "L", (950, 400)))
    self.keys.append(Key(K_SEMICOLON, ";", (1050, 400)))
    self.keys.append(Key(K_a, "A", (50, 400)))
    self.keys.append(Key(K_s, "S", (150, 400)))
    self.keys.append(Key(K_d, "D", (250, 400)))
    self.keys.append(Key(K_f, "F", (350, 400)))

    #Misc
    self.selected_subdivision = 4


    #warning
    boundary_rect = pygame.Rect(100, 200, 1000, 300)
    self.warning = MultilineText("This creator unfortunately doesn't work that well in the web version, check the github (https://github.com/PyroProtato/Beatline/tree/main) to watch the youtube demo for it or download the github folder and run the main.exe file to try it!", self.measure_text_font, (255, 255, 255), boundary_rect, 40)
    
    
  


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


    #Measure Button
    self.measure_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
    if self.measure_btn.check_press(self.mousePos, self.mouseUp):
      self.song.play_measure(self.measure)
    

    #Back Button
    self.back_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
    if self.back_btn.check_press(self.mousePos, self.mouseUp):
      pygame.mixer.music.stop()
      return "menu_init", None, None, None

    
    

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
      self.data = [[None, [[] for x in range(self.subdivision)]] for y in range(self.song.measures)]
    self.previous_song = self.song_dropdown.value

    if self.song_chosen:
      self.song_slider.update(self.mousePos, self.mouseDown, self.mouseUp)
      self.measure = self.song_slider.step
    

    #Previous Measure Button
    if self.song_chosen:
      self.prev_measure_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
      if self.prev_measure_btn.check_press(self.mousePos, self.mouseUp) and self.measure != 1:
        self.measure -= 1
    
    #Next Measure Button
      self.next_measure_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
      if self.next_measure_btn.check_press(self.mousePos, self.mouseUp) and self.measure != self.song.measures:
        self.measure += 1
    
    

    #Test Button
      self.test_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
      if self.test_btn.check_press(self.mousePos, self.mouseUp):
        key_strs = []
        for key in self.keys:
          key_strs.append(key.key_str)
        file = ""
        author = ""
        if self.song_dropdown.value == "Megalovania":
          file = "images/HD-wallpaper-sans-undertale (1).png"
          author = "Toby Fox"
        elif self.song_dropdown.value == "Field of Hopes and Dreams":
          file = "images/deltarune_fileselect.png"
          author = "Toby Fox"
        elif self.song_dropdown.value == "Hunger":
          file = "images/theFatRat-Hunger.png"
          author = "TheFatRat"
        return "test_init", Level(self.song_dropdown.value, file, author, "Custom", 5), self.data, key_strs

    self.sub_dropdown.update(self.mousePos, self.mouseDown, self.mouseUp)
    if self.song_chosen and self.previous_sub_value != self.sub_dropdown.value: #When subdivision is changed
      self.subdivision = int(self.sub_dropdown.value.removeprefix("1/").removesuffix(" Beat"))
      self.measure_slider = Slider((800, 5), (200, 625), (20, 40), 0, self.subdivision, 0)
      self.measure_slider.change_slider(slider_rect_color=(0, 0, 0), slider_border_color=(255, 255, 255))
      self.measure_slider.change_background(background_rect_border_color=(255, 255, 255))    
      if self.sub_dropdown.changed:
        self.data[self.measure-1] = [self.subdivision, [[] for x in range(self.subdivision)]]
        self.selected_subdivision = self.subdivision
    self.previous_sub_value = self.sub_dropdown.value

    if self.song_chosen:
    #Previous Song Button
      self.prev_song_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
      pressed = self.prev_song_btn.check_press(self.mousePos, self.mouseUp)
      if pressed and self.measure_slider.step != 0:
        self.measure_slider.step -= 1
      elif pressed and self.measure_slider.step == 0 and self.measure != 1:
        self.measure_slider.step = self.subdivision-1
        self.measure -= 1

    #next Song Button
      self.next_song_btn.update((100, 100, 100), (50, 50, 50), self.mousePos, self.mouseIsDown)
      pressed = self.next_song_btn.check_press(self.mousePos, self.mouseUp)
      if pressed and self.measure_slider.step != self.subdivision-1:
        self.measure_slider.step += 1
      elif pressed and self.measure_slider.step == self.subdivision - 1 and self.measure != self.song.measures:
        self.measure_slider.step = 0
        self.measure += 1
    


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

    #Whenever Song Slider Changes
    if self.song_chosen:
      if self.song_slider.step != self.prev_song_slider:
        self.measure_init_empty = True
        for beat in self.data[self.measure-1][1]:
          if beat != []:
            self.measure_init_empty = False  
        if self.measure_init_empty:
          self.data[self.measure-1] = [self.selected_subdivision, [[] for x in range(self.subdivision)]]
      self.prev_song_slider = self.song_slider.step
    

    self.song_slider.step = self.measure


    #Measure Text
    self.measure_text = self.measure_text_font.render(f"Measure: {self.measure}", True, (255, 255, 255))
    self.measure_text_rect = self.measure_text.get_rect()
    self.measure_text_rect.midleft = (900,50)
    
    #Keys
    if self.song_chosen and self.measure_slider.step != self.subdivision:
      if self.data[self.measure-1][0] != self.subdivision and self.data[self.measure-1][0] != None and not self.measure_init_empty:
        self.sub_dropdown.set_value(f"1/{self.data[self.measure-1][0]} Beat")

      if self.data[self.measure-1][0] == None:
        self.data[self.measure-1][0] = self.subdivision
        self.data[self.measure-1][1] = [[] for x in range(self.subdivision)]

      for key in self.keys:
        key.update(self.mousePos, self.mouseIsDown)
        temp = False
        for note in self.data[self.measure-1][1][self.measure_slider.step]:
          if note["key"] == key.key_str:
            temp = True
        if temp:
          key.has_beat()
          if key.check_press(self.mousePos, self.mouseUp):
            self.data[self.measure-1][1][self.measure_slider.step] = [data for data in self.data[self.measure-1][1][self.measure_slider.step] if data["key"] != key.key_str]
        else:
          key.no_beat()
          if key.check_press(self.mousePos, self.mouseUp):
            self.data[self.measure-1][1][self.measure_slider.step].append({"key":key.key_str, "type":1})
    





    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)
    self.song_dropdown.draw(WINDOW)
    WINDOW.blit(self.measure_text, self.measure_text_rect)
    if self.song_chosen:
      for i in range(self.subdivision):
        x = 200+i*self.measure_slider.width/self.subdivision
        pygame.draw.line(WINDOW, (255, 255, 255), (x, 650), (x, 665), 5)
      self.play_btn.draw(WINDOW)
      if not self.paused:
        WINDOW.blit(self.pause_btn_image, self.pause_btn_image_rect)
      else:
        WINDOW.blit(self.play_btn_image, self.play_btn_image_rect)
      self.prev_measure_btn.draw(WINDOW)
      WINDOW.blit(self.prev_measure_btn_image, self.prev_measure_btn_image_rect)
      self.next_measure_btn.draw(WINDOW)
      WINDOW.blit(self.next_measure_btn_image, self.next_measure_btn_image_rect)
      self.prev_song_btn.draw(WINDOW)
      WINDOW.blit(self.prev_song_btn_image, self.prev_song_btn_image_rect)
      self.next_song_btn.draw(WINDOW)
      WINDOW.blit(self.next_song_btn_image, self.next_song_btn_image_rect)
      self.test_btn.draw(WINDOW)
      WINDOW.blit(self.test_btn_image, self.test_btn_image_rect)

      self.measure_btn.draw(WINDOW)
      WINDOW.blit(self.measure_btn_image, self.measure_btn_image_rect)
      self.sub_dropdown.draw(WINDOW)
      self.song_slider.draw(WINDOW)
      self.measure_slider.draw(WINDOW)
      pygame.draw.rect(WINDOW, (255, 255, 255), self.measure_indicator)
      for key in self.keys:
        key.draw(WINDOW)

      self.back_btn.draw(WINDOW)
      WINDOW.blit(self.back_btn_image, self.back_btn_image_rect)

      self.warning.draw(WINDOW)
    
    return "creator", None, None, None
      
    







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