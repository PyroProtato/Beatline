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

PERFECT_COLOR = (255, 255, 50)
EXCELLENT_COLOR = (255, 100, 255)
GOOD_COLOR = (100, 100, 255)
MISS_COLOR = (255, 50, 50)




class Key:
  def __init__(self, key, key_str, coords):
    self.x = coords[0]
    self.y = coords[1]

    self.key_str = key_str
    self.notes = []

    self.width = 100
    self.height = 100

    self.outline = pygame.Rect(self.x, self.y, self.width, self.height)
    self.centery = self.outline.centery

    self.key_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.text = self.key_font.render(key_str, True, (255, 255, 255))
    self.text_rect = self.text.get_rect()
    self.text_rect.center = (self.x+self.width//2, self.y+self.height//2)

    self.key = key
    self.key_pressed = False

    self.perfect_tolerance = 5
    self.excellent_tolerance = 20
    self.good_tolerance = 40

    self.color = (255, 255, 255)
    self.hold_frames = 0
  

  def update(self, key_presses):
    self.centery = self.outline.centery
    self.text_rect.center = (self.outline.x+self.width//2, self.outline.y+self.height//2)

    if self.hold_frames != 0:
      if self.hold_frames == 1:
        self.color = (255, 255, 255)
      self.hold_frames -= 1

    self.key_pressed = False
    for event in key_presses:
      if event.key == self.key:
        self.key_pressed = True

    deleted_notes = []
    for i, note in enumerate(self.notes):
      if note.update():
        deleted_notes.append(i)
    
    for note in deleted_notes[::-1]:
      del self.notes[note]

    for i, note in enumerate(self.notes):
      if self.key_pressed:
        if note.rect.centery > self.centery - self.perfect_tolerance and note.rect.centery < self.centery + self.perfect_tolerance:
          note.perfect()
          self.beat("Perfect")
          return "Perfect"
        elif note.rect.centery > self.centery - self.excellent_tolerance and note.rect.centery < self.centery + self.excellent_tolerance:
          note.excellent()
          self.beat("Excellent")
          return "Excellent"
        elif note.rect.centery > self.centery - self.good_tolerance and note.rect.centery < self.centery + self.good_tolerance:
          note.good()
          self.beat("Good")
          return "Good"

    
    if self.key_pressed:
      self.beat("Miss")
      return "Miss"

    return None


  def beat(self, type):
    if type == "Perfect":
      self.color = PERFECT_COLOR
    elif type == "Excellent":
      self.color = EXCELLENT_COLOR
    elif type == "Good":
      self.color = GOOD_COLOR
    elif type == "Miss":
      self.color = MISS_COLOR
    self.hold_frames = 6



  def draw(self, surface):
    for note in self.notes:
      note.draw(surface)
    pygame.draw.rect(surface, self.color, self.outline, 5)
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
    self.end_frames = round(self.measure_len*(FPS/1000)*self.measures)+FPS*2
    print(self.end_frames)

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
      elif self.frames == self.end_frames:
        return "End"

      for key_btn, data in self.data.items():
        if len(data) != 0 and self.frames == int(data[0][0]-DELAY_SECONDS*FPS):
          for key in self.keys:
            if key.key_str == key_btn:
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
    self.centerx = centerx
    self.rect.centerx = centerx
    self.centery = self.rect.centery

    self.perfect_anim = False
    self.excellent_anim = False
    self.good_anim = False
    self.color = (255, 255, 255)
    self.end_anim = False
    self.end_anim_frames = 0
    self.end_anim_frame_limit = 5
  
  def update(self):
    if not self.end_anim:
      self.rect.centery += self.speed
    
    self.centery = self.rect.centery
    
    if self.end_anim:
      print("RAN")
      if self.perfect_anim:
        self.color = PERFECT_COLOR
      elif self.excellent_anim:
        self.color = EXCELLENT_COLOR
      elif self.good_anim:
        self.color = GOOD_COLOR
      
      self.rect = pygame.Rect(0, 0, self.width*self.end_anim_frames*0.15, self.height*self.end_anim_frames*0.15)
      self.rect.centery = self.centery
      self.rect.centerx = self.centerx
      
      self.end_anim_frames += 1
      
      if self.end_anim_frames >= self.end_anim_frame_limit:
        return True

    return False

  def perfect(self):
    self.perfect_anim = True
    self.end_anim = True

  def excellent(self):
    self.excellent_anim = True
    self.end_anim = True

  def good(self):
    self.good_anim = True
    self.end_anim = True
  
  def draw(self, surface):
    pygame.draw.rect(surface, self.color, self.rect, border_radius=25)



class FeedbackText:
  def __init__(self, type):
    self.type = type

    #Feedback Text
    self.feedback_text_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)
    if type == "Perfect":
      self.feedback_text = self.feedback_text_font.render("Perfect!", True, (PERFECT_COLOR))
    elif type == "Excellent":
      self.feedback_text = self.feedback_text_font.render("Excellent!", True, (EXCELLENT_COLOR))
    elif type == "Good":
      self.feedback_text = self.feedback_text_font.render("Good!", True, (GOOD_COLOR))
    elif type == "Miss":
      self.feedback_text = self.feedback_text_font.render("Miss", True, (MISS_COLOR))
    self.feedback_text_rect = self.feedback_text.get_rect()
    self.feedback_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

    #Anim
    self.anim_frames = 0
    self.max_anim_frames = 45

  def update(self):
    #Feedback Text
    if self.anim_frames < 15:
      self.feedback_text_rect.y -= 5
    
    if self.anim_frames >= self.max_anim_frames:
      return True
    self.anim_frames += 1

    return False
  
  def draw(self, surface):
    surface.blit(self.feedback_text, self.feedback_text_rect)








class game_screen:
  #Initializes all of the variables that are needed for the screen to work
  def __init__(self, level, data, keys):

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
    for key in keys:
      if key == "J":
        self.keys.append(Key(K_j, "J", (750, 800)))
      elif key == "K":
        self.keys.append(Key(K_k, "K", (850, 800)))
      elif key == "L":
        self.keys.append(Key(K_l, "L", (950, 800)))
      elif key == ";":
        self.keys.append(Key(K_SEMICOLON, ";", (1050, 800)))
      elif key == " ":
        self.keys.append(Key(K_SPACE, " ", (550, 800)))
      elif key == "A":
        self.keys.append(Key(K_a, "A", (50, 800)))
      elif key == "S":
        self.keys.append(Key(K_s, "S", (150, 800)))
      elif key == "D":
        self.keys.append(Key(K_d, "D", (250, 800)))
      elif key == "F":
        self.keys.append(Key(K_f, "F", (350, 800)))

    #Test
    self.data = data
    self.beatmap = Beatmap("Megalovania", self.keys, data)
    self.init = False

    #Top BG
    self.top_bg = pygame.Rect(0, 0, WINDOW_WIDTH, 150)

    #Streak Text
    self.streak_text_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)

    #Score Text
    self.score_text_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)

    

    #Begin Animation
    self.beginning_delay = FPS*3
    self.begin_anim = True
    self.begin_frames = 0
    self.begin_anim_interval = 10
    self.begin_anim_metainterval = 1
    self.keys_begin_anim = True

    #End Animation
    self.end_anim = False

    #Feedback text
    self.feedback_text = []

    #Misc
    self.hits = []
    self.score = 0
    self.streak = 0


  


  def run(self, events):
    key_presses = []
    
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
      if event.type == KEYDOWN:
        key_presses.append(event)

    

    """PROCESSING"""
    if self.beatmap.update() == "End":
      self.end_anim = True

    for key in self.keys:
      result = key.update(key_presses)
      if result != None:
        self.hits.append(result)

    if self.init:
      self.init = False
      self.beatmap.start()


    print(f"{self.beatmap.frames}, {self.end_anim}")


    #Begin Animation
    if self.begin_anim:
      print("HO")
      if self.begin_frames >= self.beginning_delay:
        self.begin_anim = False
        self.init = True
      self.begin_frames += 1
      if self.keys_begin_anim:
        if self.keys[0].outline.top > 650+self.begin_anim_interval:
          for key in self.keys:
            key.outline.top -= self.begin_anim_interval
          self.begin_anim_interval += self.begin_anim_metainterval
        else:
          for key in self.keys:
            key.outline.top = 650
            self.keys_begin_anim = False

    #Checks Scores
    for hit in self.hits:
      if hit == "Perfect":
        self.score = round((self.score + 500) * (1+(self.streak*0.05)))
        self.feedback_text.append(FeedbackText("Perfect"))
        self.streak += 1
      elif hit == "Excellent":
        self.score = round((self.score + 200) * (1+(self.streak*0.05)))
        self.feedback_text.append(FeedbackText("Excellent"))
        self.streak += 1
      elif hit == "Good":
        self.score = round((self.score + 75) * (1+(self.streak*0.05)))
        self.feedback_text.append(FeedbackText("Good"))
        self.streak += 1
      elif hit == "Miss":
        self.feedback_text.append(FeedbackText("Miss"))
        self.streak = 0
    self.hits = []

    #Streak Text
    self.streak_text = self.streak_text_font.render(f"Streak: {self.streak}", True, (255, 255, 255))
    self.streak_text_rect = self.streak_text.get_rect()
    self.streak_text_rect.center = (150, 50)

    #Score Text
    self.score_text = self.score_text_font.render(f"Score: {self.score}", True, (255, 255, 255))
    self.score_text_rect = self.score_text.get_rect()
    self.score_text_rect.center = (1050, 50)

    #Feedback Text
    delete = []
    for i, text in enumerate(self.feedback_text):
      if text.update():
        delete.append(i)
    
    for index in delete[::-1]:
      del self.feedback_text[index]

    




    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)

    for key in self.keys:
      key.draw(WINDOW)

    pygame.draw.rect(WINDOW, (0, 0, 0), self.top_bg)
    self.level.draw(WINDOW)
    WINDOW.blit(self.streak_text, self.streak_text_rect)
    WINDOW.blit(self.score_text, self.score_text_rect)
    for text in self.feedback_text:
      text.draw(WINDOW)
    


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