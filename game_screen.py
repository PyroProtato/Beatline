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

DELAY_SECONDS = 1
NOTE_SPEED = 10




class Key:
  def __init__(self, key, key_str, coords):
    self.x = coords[0]
    self.y = coords[1]

    self.key_str = key_str
    self.notes = []

    self.width = 100
    self.height = 100

    self.outline = pygame.Rect(self.x, self.y, self.width, self.height)

    self.key_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.text = self.key_font.render(key_str, True, (255, 255, 255))
    self.text_rect = self.text.get_rect()
    self.text_rect.center = (self.x+self.width//2, self.y+self.height//2)

    self.key = key
  

  def update(self):
    for note in self.notes:
      note.update()



  def draw(self, surface):
    for note in self.notes:
      note.draw(surface)
    pygame.draw.rect(surface, (255, 255, 255), self.outline, 5)
    surface.blit(self.text, self.text_rect)






class Beatmap:
  def __init__(self, song_str, keys, data):
    self.data = {}
    self.keys = keys
    for key in keys:
      self.data[key.key_str] = []
    self.song_str = song_str
    self.frames = -int(DELAY_SECONDS*FPS)

    #MOD
    if self.song_str == "Megalovania":
      self.song_path = "songs/Megalovania.ogg"
      self.BPM = 120
      self.measures = 78
      self.time_signature = 4
    elif self.song_str == "Field of Hopes and Dreams":
      self.song_path = "songs/Field of Hopes and Dreams.ogg"
      self.BPM = 125
      self.measures = 84
      self.time_signature = 4
    elif self.song_str == "Hunger":
      self.song_path = "songs/Hunger.ogg"
      self.BPM = 86
      self.measures = 64 
      self.time_signature = 4

    self.measure_len = self.time_signature/(self.BPM/60)*1000

    self.playing = False

    #Processing the data
    for measure in data:
      subdivision = measure[0] 
      notelist = measure[1]
      if subdivision != None:
        for i, beat in enumerate(notelist):
          time = round(self.measure_len/subdivision*i*(FPS/1000))
          for note in beat:
            key = note["key"]
            type = note["type"]
            self.data[key].append([time, type])
    
    print(self.data)


  def start(self):
    pygame.mixer.music.load(self.song_path)
    self.playing = True

  def update(self):
    if self.playing:

      if self.frames == 0:
        pygame.mixer.music.play()

      for key_btn, data in self.data.items():
        if len(data) != 0:
          print(int(DELAY_SECONDS*FPS+data[0][0]))
        if len(data) != 0 and self.frames == int(data[0][0]-DELAY_SECONDS*FPS):
          for key in self.keys:
            key.notes.append(Note(NOTE_SPEED, key.outline.centerx))
          del self.data[key_btn][0]

      self.frames += 1





class Note:
  def __init__(self, speed, centerx):
    self.speed = speed
    self.width = 50
    self.height = 75

    self.rect = pygame.Rect(0, 0, self.width, self.height)
    self.rect.centery = 75
    self.rect.centerx = centerx
  
  def update(self):
    self.rect.centery += self.speed
  
  def draw(self, surface):
    pygame.draw.rect(surface, (255, 255, 255), self.rect, 5)


  








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
    self.keys = []
    self.keys.append(Key(K_j, "J", (500, 625)))
    self.keys.append(Key(K_k, "K", (600, 625)))
    self.keys.append(Key(K_l, "L", (700, 625)))
    self.keys.append(Key(K_SEMICOLON, ";", (800, 625)))

    #Test
    data = [[4, [[{'key': 'K', 'type': 1}], [], [{'key': 'J', 'type': 1}, {'key': 'L', 'type': 1}], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]], [None, [[], [], [], []]]]
    self.beatmap = Beatmap("Megalovania", self.keys, data)
    self.init = True
  


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
    self.beatmap.update()

    for key in self.keys:
      key.update()

    if self.init:
      self.init = False
      self.beatmap.start()
    print(self.beatmap.data)



    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)

    self.level.draw(WINDOW)

    for key in self.keys:
      key.draw(WINDOW)


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