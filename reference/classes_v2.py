import pygame, asyncio, sys, math
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

    def image(self, image):
        self.button_type = 'image'
        self.picture = pygame.image.load(image).convert_alpha()
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
        self.rect = self.picture.get_rect()
        self.rect.topleft = (self.x, self.y)
    
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
        self.phrases = text.split("\n")
        self.text = []
        for i, phrase in enumerate(self.phrases):
            self.phrases[i] = self.phrases[i].split(" ")
        self.text_lines = []
        self.color = color
        self.boundary_rect = boundary_rect
        self.font = font
        self.line_spacing = line_spacing


        line = ""
        for phrase in self.phrases:
            self.text = phrase
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




class Slider:
    def __init__(self, dimensions:tuple, position:tuple, slider_dimensions:tuple, min_step:int = 1, max_step:int = 5, current_step:int = 1):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = position[1]
        self.min_steps = min_step
        self.max_steps = max_step
        self.step = current_step

        self.on_mouse = False
        self.text_added = False
        self.bar_filling = False


        #Colors
        self.background_rect_color = (255, 255, 255)

        self.background_rect_radius = 0

        #Borders
        self.background_rect_border_color = (0, 0, 0)
        self.background_rect_border_width = 5

        self.interval = self.width / self.max_steps

        #Slider Settings
        self.slider_radius = 0
        self.slider_border_color = (0, 0, 0)
        self.slider_rect_color = (255, 255, 255)
        self.slider_border_width = 5

        #Creates the Background Rect
        self.back_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        #Creates the slider
        self.slider_width = slider_dimensions[0]
        self.slider_height = slider_dimensions[1]
        self.slider_x = self.x+self.interval*self.step
        self.slider_y = self.y-self.slider_height//4
        self.slider = pygame.Rect(self.slider_x, self.slider_y, self.slider_width, self.slider_height)

    
    def change_background(self, background_rect_color:tuple = None, background_rect_border_width:int = None, background_rect_border_color:int = None, background_rect_radius:int = None):
        if background_rect_color != None:
            self.background_rect_color = background_rect_color
        if background_rect_border_width != None:
            self.background_rect_border_width = background_rect_border_width
        if background_rect_border_color != None:
            self.background_rect_border_color = background_rect_border_color
        if background_rect_radius != None:
            self.background_rect_radius = background_rect_radius
    
    def change_slider(self, slider_rect_color:tuple = None, slider_border_color:tuple = None, slider_border_width:tuple = None, slider_radius:int = None):
        if slider_rect_color != None:
            self.slider_rect_color = slider_rect_color
        if slider_border_color != None:
            self.slider_border_color = slider_border_color
        if slider_border_width != None:
            self.slider_border_width = slider_border_width
        if slider_radius != None:
            self.slider_radius = slider_radius
    
    def add_text(self, font, color):
        self.text_added = True
        self.text_font = font
        self.text_color = color
    
    def enableBarFilling(self, color):
        self.bar_filling = True
        self.bar_filling_color = color
        
    
    def update(self, mousePos, mouseDown, mouseUp):
        

        #Determines whether the mouse is dragging it
        if mousePos[0] >= self.slider_x and mousePos[0] <= self.slider_x+self.slider_width and mousePos[1] >= self.slider_y and mousePos[1] <= self.slider_y+self.slider_height and mouseDown:
            self.on_mouse = True
            self.inital_x = mousePos[0]
            self.inital_step = self.step
        
        if self.on_mouse == True:
            self.step = round(self.inital_step + (mousePos[0] - self.inital_x)//self.interval)
            if self.step > self.max_steps:
                self.step = self.max_steps
            elif self.step < self.min_steps:
                self.step = self.min_steps
            
        if mouseUp == True:
            self.on_mouse = False
        

        #Figures out what step the slider should be on

        #Updates Features
        self.back_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.slider_x = self.x+self.interval*self.step-self.slider_width//2
        self.slider_y = self.y-self.slider_height//4
        self.slider = pygame.Rect(self.slider_x, self.slider_y, self.slider_width, self.slider_height)


    def draw(self, surface):
        #Bar
        pygame.draw.rect(surface, self.background_rect_color, self.back_rect, 0, border_radius=self.background_rect_radius)

        #Bar Filling
        if self.bar_filling:
            rect = pygame.Rect(self.x, self.y, self.slider.x-self.x, self.height)
            pygame.draw.rect(surface, self.bar_filling_color, rect)

        #Bar Border
        pygame.draw.rect(surface, self.background_rect_border_color, self.back_rect, self.background_rect_border_width, border_radius=self.background_rect_radius)

        #Slider
        pygame.draw.rect(surface, self.slider_rect_color, self.slider, border_radius=self.slider_radius)
        pygame.draw.rect(surface, self.slider_border_color, self.slider, self.slider_border_width, border_radius=self.slider_radius)

        #Text
        if self.text_added:
            text = self.text_font.render(str(self.step), True, self.text_color)
            text_rect = text.get_rect()
            text_rect.center = self.slider.center
            surface.blit(text, text_rect)
        
        



class Dropdown:
    def __init__(self, dimensions:tuple, position:tuple, display_rect_text:str, options:list, font):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = position[1]

        self.options = options
        self.font = font
        self.value = display_rect_text

        self.open = False
        self.on_mouse = False

        self.triangle_points = None

        #Display Rect
        self.display_rect_color = (255, 255, 255)
        self.display_rect_text_color = (0, 0, 0)
        self.display_rect_text = font.render(display_rect_text, True, self.display_rect_text_color)
        self.display_rect_border_width = 5
        self.display_rect_border_color = (0, 0, 0)
        self.display_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        #Option Rects
        self.option_rect_color = (150, 150, 150)
        self.option_border_width = 3
        self.option_text_color = (0, 0, 0)
    
    def update(self, mousePos, mouseDown, mouseUp):
        #Detects when the button is being pressed
        if mousePos[0] >= self.x and mousePos[0] <= self.x+self.width and mousePos[1] >= self.y and mousePos[1] <= self.y+self.height and mouseUp and self.on_mouse:
            if self.open:
                self.open = False
            else:
                self.open = True
            self.on_mouse = False
        elif mousePos[0] >= self.x and mousePos[0] <= self.x+self.width and mousePos[1] >= self.y and mousePos[1] <= self.y+self.height and mouseDown:
            self.on_mouse = True
        elif mouseUp:
            self.on_mouse = False        
        
        #Detects when the user clicks an option
        if self.open:
            for i, entry in enumerate(self.options):
                if mousePos[0] >= self.x and mousePos[0] <= self.x+self.width and mousePos[1] >= self.y+self.height*(i+1) and mousePos[1] <= self.y+self.height+self.height*(i+1) and mouseUp:
                    self.display_rect_text = self.font.render(entry, True, self.display_rect_text_color)
                    self.value = entry
                    self.open = False

    
    def changeDisplayRect(self, display_rect_color:tuple = None, display_rect_border_width:int = None, display_rect_border_color:tuple = None, display_rect_text_color:tuple = None):
        if display_rect_color != None:
            self.display_rect_color = display_rect_color
        if display_rect_border_width != None:
            self.display_rect_border_width = display_rect_border_width
        if display_rect_border_color != None:
            self.display_rect_border_color = display_rect_border_color
        if display_rect_text_color != None:
            self.display_rect_text_color = display_rect_text_color
    
    def changeOptionRect(self, option_border_width:int = None, option_text_color:tuple = None):
        if option_border_width != None:
            self.option_border_width = option_border_width
        if option_text_color != None:
            self.option_text_color = option_text_color
    
    def addTriangle(self, side_length:int, distance_from_right:int, color:tuple = (255, 255, 255), border_width:int = 0, border_color:tuple = (0, 0, 0)):
        self.triangle_points = []
        triangle_height = side_length/2*math.sqrt(3)
        distance_from_top = (self.height-triangle_height)/2
        self.triangle_points.append((self.x+self.width-distance_from_right, self.y+distance_from_top))
        self.triangle_points.append((self.x+self.width-distance_from_right-side_length, self.y+distance_from_top))
        self.triangle_points.append((self.x+self.width-distance_from_right-side_length/2, self.y+distance_from_top+triangle_height))
        self.triangle_color = color
        self.triangle_border_width = border_width
        self.triangle_border_color = border_color


    def draw(self, surface):
        #Display Rect
        pygame.draw.rect(surface, self.display_rect_color, self.display_rect)
        pygame.draw.rect(surface, self.display_rect_border_color, self.display_rect, self.display_rect_border_width)
        text_rect = self.display_rect_text.get_rect()
        text_rect.center = self.display_rect.center
        surface.blit(self.display_rect_text, text_rect)

        #Sub Rects
        if self.open:
            for i,entry in enumerate(self.options):
                #Draws each rect
                option_rect = pygame.Rect(self.x, self.y+self.height*(i+1)-self.option_border_width*(i+1), self.width, self.height)
                pygame.draw.rect(surface, self.display_rect_color, option_rect)
                pygame.draw.rect(surface, self.display_rect_border_color, option_rect, self.display_rect_border_width)
                
                #Blits the Text
                text = self.font.render(entry, True, self.option_text_color)
                text_rect = text.get_rect()
                text_rect.center = option_rect.center
                surface.blit(text, text_rect)
        
        #Triangle
        if self.triangle_points != None:
            pygame.draw.polygon(surface, self.triangle_color, self.triangle_points)
            pygame.draw.polygon(surface, self.triangle_border_color, self.triangle_points, self.triangle_border_width)
        


class RadioButtons:
    def __init__(self, number, radius, coords, inital_selected_index:int = 0):
        self.number = number
        self.radius = radius
        self.coords = coords

        self.default_color = (255, 255, 255)
        self.selected_color = (0, 0, 255)

        self.border_color = (0, 0, 0)
        self.border_width = 5

        self.selected_index = inital_selected_index

        self.on_mouse = False

        self.labels = []
    
    def update(self, mousePos, mouseUp, mouseDown):
        for i, coords in enumerate(self.coords):
            if mousePos[0] >= coords[0]-self.radius and mousePos[0] <= coords[0]+self.radius and mousePos[1] >= coords[1]-self.radius and mousePos[1] <= coords[1]+self.radius and mouseUp and self.on_mouse:
                self.selected_index = i
            elif mousePos[0] >= coords[0]-self.radius and mousePos[0] <= coords[0]+self.radius and mousePos[1] >= coords[1]-self.radius and mousePos[1] <= coords[1]+self.radius and mouseDown:
                self.on_mouse = True
        if mouseUp:
            self.on_mouse = False  
    
    def add_labels(self, font, xoffset, yoffset, color, labels:list):
        self.labels = []
        for i, label in enumerate(labels):
            text = font.render(label, True, color)
            text_rect = text.get_rect()
            text_rect.center = (self.coords[i][0]+xoffset, self.coords[i][1]+yoffset)
            self.labels.append([text, text_rect])
    
    def draw(self, surface):
        for i, coord in enumerate(self.coords):
            color = self.default_color
            if i == self.selected_index:
                color = self.selected_color
            pygame.draw.circle(surface, color, coord, self.radius)
            pygame.draw.circle(surface, self.border_color, coord, self.radius, self.border_width)
        
        for label in self.labels:
            surface.blit(label[0], label[1])

            
                
        


                
                



