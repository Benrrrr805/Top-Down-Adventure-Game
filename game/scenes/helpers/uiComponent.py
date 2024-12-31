import pygame
from game.core.game_resources import GameResources
from game.settings import BLACK, RED

class UIComponent:
    def __init__(self, name, width, height, x_coordinate, y_coordinate, background_image=None, active=True, need_to_update=True, debug_color=BLACK, parent=None, children=[]):
        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.height = height
        self.width = width
        self.name = name

        self.rect = pygame.Rect(self.x_coordinate, self.y_coordinate, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))
        self.debug_color = debug_color
        self.need_to_update = need_to_update
        self.children = children
        self.parent = parent
        self.active = active

        if background_image is not None:
            self.background_image = pygame.image.load(background_image).convert()
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        else:
            self.background_image = background_image


    def add_child(self, child):
        child.rect.x += self.rect.x
        child.rect.y += self.rect.y

        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def get_rect(self):
        return self.rect

    def in_rect(self, coordinates):
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        hover = self.in_rect(pygame.mouse.get_pos())
        return hover
    
    def clicked(self):
        if not self.hovering():
            return False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
    
    def handle_events(self):
        if self.clicked():
            print("clicked: " + self.name)
        for child in self.children:
            if child.active:
                child.handle_events()
                 

    def update(self):
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
            

    def draw(self):
        if self.need_to_update and self.background_image is not None:
            self.surface.blit(self.background_image, (0, 0))

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
            print(f"Drawing: {self.name}")
            pygame.draw.rect(self.surface, self.debug_color, (0, 0, self.width, self.height), 5)

        # Reset the UI Component's need to update flag
        if self.need_to_update:
            self.need_to_update = False
        
        return self.surface
