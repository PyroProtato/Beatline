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



class Level:
  def __init__(self, name, picture, author, difficulty, position):
    self.position = position - 1
    self.name = name
    self.picture = pygame.transform.scale(pygame.image.load(picture), (200, 150))
    self.difficulty = difficulty
    self.scroll_pos = 0
    self.author = author

    self.height = 150
    self.width = 650

    self.x = WINDOW_WIDTH

    self.spacing = 200

    self.level_title_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 50)
    self.level_difficulty_font = pygame.font.Font("fonts/CAT Rhythmus.ttf", 30)

    self.title_text = self.level_title_font.render(name, True, (255, 255, 255))
    self.title_text_rect = self.title_text.get_rect()
    self.difficulty_text = self.level_difficulty_font.render(f"Difficulty: {self.difficulty}", True, (255, 255, 255))
    self.difficulty_text_rect = self.difficulty_text.get_rect()
    self.author_text = self.level_difficulty_font.render(f"{self.author}", True, (255, 255, 255))
    self.author_text_rect = self.author_text.get_rect()

    self.outline = pygame.Rect(self.x, 0, self.width, self.height)

    self.anim_begin = False
    self.free = False

    self.chosen = False
    self.anim_end = False

    self.running_animation = False


  def update(self, scroll_pos, mousePos):
    if not self.running_animation:
        self.scroll_pos = scroll_pos

    if self.free and not self.running_animation:
      if mousePos[0] > 400 and mousePos[1] > self.position*self.spacing+25 and mousePos[1] < self.position*self.spacing+self.height+75:
        self.x = 450
      else:
        self.x = 500
    
    if self.anim_begin:
      if self.x <= 500 or self.x-self.begin_interval <= 500:
        self.x = 500
        self.anim_begin = False
        self.free = True
      else:
        self.begin_interval -= self.begin_metainterval
        self.x -= self.begin_interval
    
    if self.anim_end:
      if self.scroll_pos < 0-self.end_interval:
        self.scroll_pos += self.end_interval
      else:
        self.scroll_pos = 0
        self.anim_end = False
        return True
    
    return False


  def b_anim(self):
    self.anim_begin = True
    self.begin_interval = 40
    self.begin_metainterval = 1.1

  def e_anim(self):
    self.running_animation = True
    if self.chosen:
        self.anim_end = True
        self.end_interval = 20
        self.x = 275
        self.scroll_pos = -self.height

  def checkPress(self, mousePos, mouseUp):
    if mouseUp and self.outline.collidepoint(mousePos[0], mousePos[1]):
      self.chosen = True
      return True
    return False


  def draw(self, surface):
    if not self.running_animation or self.chosen == False:
        top = 50+self.spacing*self.position-self.scroll_pos
    else:
      top = self.scroll_pos
    self.outline = pygame.Rect(self.x, top, self.width, self.height)
    self.title_text_rect.topleft = (self.x+200+25, top+25)
    self.author_text_rect.bottomleft = (self.x+200+25, top+self.height-12)
    self.difficulty_text_rect.bottomleft = (self.x+200+(self.width-200)//2+25, top+self.height-12)

    if self.running_animation and not self.chosen:
      pass
    else:
        surface.blit(self.picture, (self.x, top))
        pygame.draw.line(WINDOW, (255, 255, 255), (self.x+200, top), (self.x+200, top+self.height-1), 5)
        pygame.draw.line(WINDOW, (255, 255, 255), (self.x+200, top+self.title_text_rect.height+35), (self.x+self.width-1, top+self.title_text_rect.height+35), 5)
        pygame.draw.line(WINDOW, (255, 255, 255), (self.x+200+(self.width-200)//2, top+self.title_text_rect.height+35), (self.x+200+(self.width-200)//2, top+self.height-1), 5)
        pygame.draw.rect(surface, (255, 255, 255), self.outline, 5)
        surface.blit(self.title_text, self.title_text_rect)
        surface.blit(self.author_text, self.author_text_rect)
        surface.blit(self.difficulty_text, self.difficulty_text_rect)





class menu_screen:
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

    #Title Bg
    self.title_bg = pygame.Rect(-400, 0, 400, 800)

    #Animation
    self.title_x = 600
    self.titleanim = True
    self.flipped = False
    self.interval = 1
    self.meta_interval = 1.25

    #Levels Animation
    self.levelsanim = False
    

    #Chose Animation
    self.chose_anim = False
    self.chose_y_offset = 0
    self.chose_interval = 1
    self.chose_metainterval = 1.1


    #Levels
    self.levels = []
    self.levels.append(Level("Field of Hopes an...", "images/deltarune_fileselect.png", "Toby Fox", 2, 1))
    self.levels.append(Level("Hunger", "images/theFatRat-Hunger.png", "TheFatRat", 4, 2))
    self.levels.append(Level("Megalovania", "images/HD-wallpaper-sans-undertale (1).png", "Toby Fox", 5, 3))
  


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
    if self.titleanim:
      if self.title_x <= 206:
        self.titleanim = False
        self.levelsanim = True
        self.title_x = 200
      elif self.title_x > 400:
        self.interval *= self.meta_interval
      else:
        self.flipped = True
        self.interval /= self.meta_interval
        self.title = self.title_font.render("Menu", True, (0, 0, 0))
        self.title_rect = self.title.get_rect()
        self.title_rect.centery = 125
      self.title_x -= self.interval
      self.title_bg.x += self.interval
    self.title_rect.centerx = self.title_x


    if self.levelsanim:
      for level in self.levels:
        level.b_anim()
        self.levelsanim = False
    
    for level in self.levels:
      if level.update(0, self.mousePos):
        return "game_init", level
      if level.checkPress(self.mousePos, self.mouseUp):
        self.chose_anim = True

    
    if self.chose_anim:
        if self.chose_y_offset < 120000.0:
            self.chose_y_offset *= self.chose_metainterval
            self.chose_y_offset += self.chose_interval

            self.title_rect.centery-=self.chose_y_offset
            self.title_bg.centery -= self.chose_y_offset

            for level in self.levels:
                level.scroll_pos += self.chose_y_offset
        else:
          self.chose_anim = False
          for level in self.levels:
            level.e_anim()
      
    





    """DRAW TO SCREEN"""
    WINDOW.fill(self.color_bg)

    pygame.draw.rect(WINDOW, (255, 255, 255), self.title_bg)


    WINDOW.blit(self.title, self.title_rect)

    for level in self.levels:
      level.draw(WINDOW)
    

    return "menu", ""






'''


 
# The main function that controls the game
async def main () :

  """INITIATE THE SCREENS"""
  s1 = menu_screen()
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