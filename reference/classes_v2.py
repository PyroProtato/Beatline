import pygame, asyncio, sys
from pygame.locals import *
pygame.init()

class Button: 
    def __init__(self,position:tuple,size:tuple,color:tuple): 

        # init self
        self.button_type = 'rectangle'
        self.normal_color = color
        self.border_width = 0
        self.text_added = False
        self.border_added = False
        self.x = position[0]
        self.y = position[1]
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.y_offset = 0
        
        # init rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def image(self, image, scale=1):
        self.button_type = 'image'
        self.picture = pygame.image.load(image).convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (self.picture.get_width()*scale, self.picture.get_height()*scale))
        self.rect = self.picture.get_rect()
        self.rect.center = (self.x, self.y)
        self.width *= scale
        self.height *= scale
    
    def update(self, hover_color:tuple, pressed_color:tuple, mousePos:tuple, MousePressed:bool): #Changes the color according to action
        if MousePressed and self.rect.collidepoint(mousePos):
            self.color = pressed_color
        elif self.rect.collidepoint(mousePos):
            self.color = hover_color
        else:
            self.color = self.normal_color

    def draw(self,surface): #Draws everything to surface
        # Checks what type of button it is
        if self.button_type == 'rectangle':
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, self.color, self.rect)
        elif self.button_type == 'image':
            surface.blit(self.picture, (self.x, self.y))

        if self.border_width != 0: #Creates border if it has been specified
            self.border = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
            pygame.draw.rect(surface, self.border_color, self.border, self.border_width)
        if self.text_added == True: #Prints Text if it has been specified
            self.text_rect.center = self.rect.center
            self.text_rect.y += self.y_offset
            surface.blit(self.text, self.text_rect)
     
    def check_press(self, mousePos:tuple, MouseUp:bool): #Returns True if the button has been pressed
        if self.rect.collidepoint(mousePos) and MouseUp:
            return True
        return False
    
    def add_border(self, width:int, color:tuple): #Optional to add a border
        self.border_added = True
        self.border = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.border_width = width
        self.border_color = color
        
    def add_text(self, font,text:str,text_color:tuple,y_offset:int=None): # Adds text in front of the button
        if y_offset != None:
            self.y_offset = y_offset
        self.text_added = True
        self.text = font.render(text, True, text_color, None)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center
    
    def is_hovering(self, mousePos:tuple, MouseIsDown:bool): # Checks if the button is being hovered over
        if MouseIsDown == False and self.rect.collidepoint(mousePos):
            return True
        return False
    
    def is_pressed(self, mousePos:tuple, MouseIsDown:bool): # Checks if the button is being pressed
        if MouseIsDown and self.rect.collidepoint(mousePos):
            return True
        return False
    
    def change_center(self, position:tuple):
        self.x = position[0]-self.width//2
        self.y = position[1]-self.height//2




class Textbox:
    def __init__(self, rect, color:tuple, font, font_color, text_x_offset:int=0, text_y_offset:int=0, whitelist:list=[], blacklist:list=[], prefix:str=""):
        self.rect = rect
        self.og_color = color
        self.color = self.og_color
        self.font = font
        self.font_color = font_color
        self.active = False
        self.text = ""
        self.text_display = None
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        self.border_added = False
        self.whitelist = None
        self.blacklist = None
        if whitelist != []:
            self.whitelist = whitelist
        elif blacklist != []:
            self.blacklist = blacklist
        self.prefix = prefix
        self.text += self.prefix
        self.user_input = ""
        self.active = False
        self.description_added = False
        self.desc = None
        self.desc_shown = True

        self.text_display = self.font.render(self.text, True, self.font_color, None)
        self.text_display_rect = self.text_display.get_rect()


    # Checks the state of the box and accounts for user typing
    def update(self, mousePos:tuple, mousePressed:bool, highlight_color:tuple, event):
        if mousePressed and self.rect.collidepoint(mousePos):
            self.desc_shown = False
            self.active = True
            self.color = highlight_color
        elif mousePressed and self.rect.collidepoint(mousePos) != True:
            self.active = False
            self.color = self.og_color

        if self.active:
            if self.prefix != "" and self.user_input == "":
                self.text = self.prefix
        
        if self.active == False and self.description_added and self.user_input == "":
            self.desc_shown = True
            self.text = self.desc

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text) != len(self.prefix):
                    self.text = self.text[:-1]
            else:
                if self.whitelist != None and event.unicode in self.whitelist:
                    self.text += event.unicode
                elif self.blacklist != None and event.unicode not in self.blacklist:
                    self.text += event.unicode
                elif self.whitelist == None and self.blacklist == None:
                    self.text += event.unicode
        
        self.text_display = self.font.render(self.text, True, self.font_color, None)
        self.text_display_rect = self.text_display.get_rect()
        while self.text_display_rect.width > self.rect.width - 2*self.text_x_offset:
            self.text = self.text[:-1]
            self.text_display = self.font.render(self.text, True, self.font_color, None)
            self.text_display_rect = self.text_display.get_rect()
        self.text_display_rect.midleft = self.rect.midleft
        self.text_display_rect.left += self.text_x_offset
        self.text_display_rect.top += self.text_y_offset

        if self.text == self.desc:
            self.user_input = ""
        else:
            self.user_input = self.text[len(self.prefix):]

    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.description_added:
            if self.desc_shown:
                self.text_display = self.font.render(self.text, True, self.font_color, None)
                self.text_display_rect = self.text_display.get_rect()
                self.text_display_rect.center = self.rect.center
                self.text_display_rect.y += self.text_y_offset
        surface.blit(self.text_display, self.text_display_rect)
        if self.border_added:
            self.border = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
            pygame.draw.rect(surface, self.border_color, self.border, self.border_width)

    
    def add_border(self, width:int, color:tuple): #Optional to add a border
        self.border_added = True
        self.border = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.border_width = width
        self.border_color = color
    
    def add_description(self, description:str=""):
        self.desc = description
        self.description_added = True
        self.text = description
    
    def return_input(self):
        return self.user_input










class MultilineText:
    def __init__(self, text, font, color, boundary_rect, line_spacing, Xalignment="center", Yalignment="top"):
        self.xalignment = Xalignment
        self.yalignment = Yalignment
        self.text = text.split(" ")
        self.text_lines = []
        self.color = color
        self.boundary_rect = boundary_rect
        self.font = font
        self.line_spacing = line_spacing

        line = ""
        while len(self.text) != 0:
            entry = self.text[0]
            if line == "":
                line = entry
            else:
                line += f" {entry}"
            del self.text[0]
            test_line = self.font.render(line, True, self.color)
            test_line_rect = test_line.get_rect()
            if test_line_rect.width > self.boundary_rect.width:
                line = line.split(" ")
                self.text.insert(0, entry)
                del line[len(line)-1]
                line = " ".join(line)
                if line != "":
                    self.text_lines.append(line)
                    line = ""
                else:
                    line = ""
                    word = self.text[0]
                    del self.text[0]
                    while len(word) != 0:
                        line += word[0]
                        word = word[1:]
                        test_line = self.font.render(line, True, self.color)
                        test_line_rect = test_line.get_rect()
                        if test_line_rect.width > self.boundary_rect.width:
                            line = [char for char in line]
                            entry = line[len(line)-1]
                            word = entry + word
                            del line[len(line)-1]
                            line = "".join(line)
                            self.text_lines.append(line)
                            line = ""
                            self.text.insert(0, word)
                            word = ""
            elif len(self.text) == 0:
                self.text_lines.append(line)
                line = ""

    
    def draw(self, surface):

        #Y Spacing
        totalY = len(self.text_lines*self.line_spacing)
        if self.yalignment == "center":
            yoffset = (self.boundary_rect.height-totalY)/2
        elif self.yalignment == "top":
            yoffset = 0
        elif self.yalignment == "bottom":
            yoffset = self.boundary_rect.height-totalY

        for index, line in enumerate(self.text_lines):
            line_text = self.font.render(line, True, self.color)
            line_text_rect = line_text.get_rect()

            #X Spacing
            if self.xalignment == "center":
                line_text_rect.centerx = self.boundary_rect.width//2+self.boundary_rect.x
            elif self.xalignment == "left":
                line_text_rect.x = self.boundary_rect.x
            elif self.xalignment == "right":
                line_text_rect.x = self.boundary_rect.x+self.boundary_rect.width-line_text_rect.width

            line_text_rect.y = self.boundary_rect.y+yoffset+index*self.line_spacing

            surface.blit(line_text, line_text_rect)





