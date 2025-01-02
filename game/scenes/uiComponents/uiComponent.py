# import pygame
from game.core.game_resources import GameResources
from game.settings import BLACK, RED
import os

class UIComponent:
    def __init__(self, name, width, height, x_coordinate, y_coordinate, 
                 background_image=None, background_color=None,  
                 text=None, text_font=None, text_size=24, text_color=BLACK, text_position=None, 
                 active=True, need_to_update=True, debug_color=BLACK, 
                 parent=None, children=[]):
        self.pygame = GameResources.pygame
        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.height = height
        self.width = width
        self.name = name
        self.background_color = background_color
        self.rect = self.pygame.Rect(self.x_coordinate, self.y_coordinate, self.width, self.height)
        self.surface = self.pygame.Surface((self.width, self.height), self.pygame.SRCALPHA)
        self.debug_color = debug_color
        self.need_to_update = need_to_update
        self.children = children
        self.parent = parent
        self.active = active
        self.image_url = background_image

        self.text = text
        self.text_font = self.pygame.font.Font(text_font, text_size) if text_font else self.pygame.font.SysFont(None, text_size)
        self.text_color = text_color
        self.text_position = text_position if text_position else (self.width // 2, self.height // 2)

        if background_image is not None:
            self.background_image = self.pygame.image.load(background_image).convert()
            self.background_image = self.pygame.transform.scale(self.background_image, (self.width, self.height))
        else:
            self.background_image = None


    def render_text(self):
        if self.text:
            text_surface = self.text_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            if self.text_position == "center":
                text_rect.center = (self.width // 2, self.height // 2)
            else:
                text_rect.topleft = self.text_position
            self.surface.blit(text_surface, text_rect)

    def add_child(self, child):
        child.rect.x += self.rect.x
        child.rect.y += self.rect.y
        child.parent = self
        self.children.append(child)
        print(f"Added {child.name} to {self.name}")
    
    def remove_child(self, child):
        self.children.remove(child)

    def remove_parent(self):
        self.parent = None

    def get_rect(self):
        return self.rect

    def in_rect(self, coordinates):
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        hover = self.in_rect(self.pygame.mouse.get_pos())
        return hover
    
    def clicked(self):
        if not self.hovering():
            return False
        for child in self.children:
            if child.active and child.hovering():
                return False
        for event in self.pygame.event.get():
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                return True
    
    def handle_events_(self):
        if self.clicked():
            if self.debug:
                print("clicked: " + self.name)
        for child in self.children:
            if child.active:
                child.handle_events()

    def handle_events(self):
        if self.active:
            return self.handle_events_()
        return None

    def update_(self):
        if self.debug and self.debug_color is not None:
            if self.hovering() and self.debug_color == BLACK:
                self.need_to_update = True
                self.debug_color = RED
            elif not self.hovering() and self.debug_color == RED:
                self.need_to_update = True
                self.debug_color = BLACK
        for child in self.children:
            if child.active:
                child.update()
                if child.need_to_update:
                    self.need_to_update = True

    def delete(self):
        # Use a copy here
        children_copy = list(self.children)
        for child in children_copy:
            child.delete()

        # Clear children at the end
        self.children = []
        self.active = False

        if self.parent:
            if self.debug:
                print(f"Removing {self.name} from parent {self.parent.name}")
            self.parent.need_to_update = True
            self.parent.remove_child(self)
        else:
            if self.debug:
                print("Parent is None")

        self.need_to_update = True
        self.parent = None
        if self.debug:
            print(f"Deleted {self.name}")

    def update(self):
        if self.active:
            return self.update_()
        return None

    def draw_(self):

        if self.need_to_update and self.background_image is not None and self.background_color is None:
            self.surface.blit(self.background_image, (0, 0))

        # Fill with background color if available
        elif self.need_to_update and self.background_color is not None and self.background_image is None:
            self.surface.fill(self.background_color)
            
        # Otherwise, make it transparent
        elif self.need_to_update and self.background_color is None and self.background_image is None:
            self.surface.fill((0, 0, 0, 0))  # Fully transparent (RGBA)
           
        # Render text
        self.render_text()

        # Redraw children selectively
        for child in self.children:
            
            if self.need_to_update or child.need_to_update:
                
                child_surface = child.draw()
                if child_surface is not None:
                    x = child.get_rect().x - self.rect.x
                    y = child.get_rect().y - self.rect.y
                    self.surface.blit(child_surface,(x, y))
                # Reset the child's update flag
                child.need_to_update = False

        # Draw the debug border if necessary
       
        if self.debug and self.debug_color is not None and self.need_to_update:
            self.pygame.draw.rect(self.surface, self.debug_color, (0, 0, self.width, self.height), 5)
            
        # Reset the UI Component's need to update flag
        if self.need_to_update:
            self.need_to_update = False
           
        return self.surface

    def draw(self):
        if self.active:
            return self.draw_()
        return None
