
class EventQueue:
    def __init__(self, pygame, debug):
        self.event_queue = None
        self.pygame = None
        self.debug = None
        self.event_mapping = None
        self.initialized = False

    def initialize(self, pygame, debug):
        if self.initialized:
            raise Exception("EventQueue already initialized")
        self.pygame = pygame
        self.debug = debug
        self.event_queue = []
        self.event_set = set()
        self.event_mapping = {
                self.pygame.MOUSEBUTTONDOWN: self.MOUSEBUTTONDOWN,
                self.pygame.MOUSEBUTTONUP: self.MOUSEBUTTONUP,
                self.pygame.KEYDOWN: self.KEYDOWN,
                self.pygame.KEYUP: self.KEYUP,
                self.pygame.QUIT: self.QUIT,
                self.pygame.MOUSEMOTION: self.MOUSEMOTION,
                self.pygame.MOUSEWHEEL: self.MOUSEWHEEL
        }
        self.initialized = True

    def add_event(self, event):
        if self.event_queue is None:
            self.event_queue = []
            self.event_set = set()
        self.event_queue.append(event)
        self.event_set.add(event['type'])

    def get_last_event(self):
        if len(self.event_queue) > 0:
            return self.event_queue.pop(0)
        else:
            return None

    def has_event(self, event):
        return event in self.event_set

    def remove_event(self, event):
        if event in self.event_set:
            self.event_set.remove(event)

    def clear_events(self):
        self.event_queue = None
        self.event_set = set()
        
    def handle_events(self):
        for event in self.pygame.event.get():
            if event.type in self.event_mapping:
                self.add_event(self.event_mapping[event.type](event))

    def base_event(self, event, extras):
        event = {
            'type': event.type,
            'timestamp': self.pygame.time.get_ticks()
        }
        for key, value in extras.items():
            event[key] = value
        return event

    def MOUSEBUTTONDOWN(self, event):
        extras = {
            'button': event.button,
            'pos': event.pos,
        }
        return self.base_event(event, extras)
    
    def MOUSEBUTTONUP(self, event):
        extras = {
            'button': event.button,
            'pos': event.pos
        }
        return self.base_event(event, extras)
        
    
    def KEYDOWN(self, event):
        extras = {
            'key': event.key,
            'mod': event.mod,
            'unicode': event.unicode,
        }
        return self.base_event(event, extras)

    def KEYUP(self, event):
        extras = {
            'key': event.key,
            'mod': event.mod
        }
        return self.base_event(event, extras)
    
    def QUIT(self, event):
        extras = {}
        return self.base_event(event, extras)

    def MOUSEMOTION(self, event):
        extras = {
            'pos': event.pos,
            'rel': event.rel,
            'buttons': event.buttons,
        }
        return self.base_event(event, extras)
    
    def MOUSEWHEEL(self, event):
        extras = {
            'flipped': event.flipped,
            'pos': event.pos
        }
        return self.base_event(event, extras)