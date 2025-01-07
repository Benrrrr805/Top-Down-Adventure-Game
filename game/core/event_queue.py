class EventQueue:
    def __init__(self):
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
        self.event_mapping = {
                self.pygame.MOUSEBUTTONDOWN: self.MOUSEBUTTONDOWN,
                self.pygame.MOUSEBUTTONUP: self.MOUSEBUTTONUP,
                self.pygame.KEYDOWN: self.KEYDOWN,
                self.pygame.KEYUP: self.KEYUP,
                self.pygame.QUIT: self.QUIT,
                self.pygame.MOUSEMOTION: self.MOUSEMOTION,
                self.pygame.MOUSEWHEEL: self.MOUSEWHEEL
        }
        self.last_mouse_pos = None
        self.initialized = True

    def add_event(self, event):
        if self.event_queue is None:
            self.event_queue = []
        self.event_queue.append(event)

    def get_last_event(self):
        if len(self.event_queue) > 0:
            return self.event_queue.pop(0)
        else:
            return None

    def has_event(self, event_type, extras=None):
        for e in self.event_queue:
            if e['type'] == event_type:
                print(e)
                if extras is None:
                    return True
                for key, value in extras.items():
                    if e[key] != value:
                        return False
                return True
        return False

    def remove_event(self, event_type):
        self.event_queue = [e for e in self.event_queue if e['type'] != event_type]

    def clear_events(self):
        self.event_queue = None
        
    def handle_events(self):
        for event in self.pygame.event.get():
            if event.type in self.event_mapping:
                if event.type == self.pygame.MOUSEMOTION:
                    self.last_mouse_pos = event.pos
                else:
                    self.add_event(self.event_mapping[event.type](event))


    def base_event(self, extras):
        event = {
            'timestamp': self.pygame.time.get_ticks()
        }
        for key, value in extras.items():
            event[key] = value
        return event

    def MOUSEBUTTONDOWN(self, event):
        extras = {
            'button': event.button,
            'pos': event.pos,
            'type': 'MOUSEBUTTONDOWN'
        }
        return self.base_event(extras)
    
    def MOUSEBUTTONUP(self, event):
        extras = {
            'button': event.button,
            'pos': event.pos,
            'type': 'MOUSEBUTTONUP'
        }
        return self.base_event(extras)
        
    
    def KEYDOWN(self, event):
        extras = {
            'key': event.key,
            'mod': event.mod,
            'unicode': event.unicode,
            'type': 'KEYDOWN'
        }
        return self.base_event(extras)

    def KEYUP(self, event):
        extras = {
            'key': event.key,
            'mod': event.mod,
            'type': 'KEYUP'
        }
        return self.base_event(extras)
    
    def QUIT(self, event):
        extras = {
            'type': 'QUIT'
        }
        return self.base_event(extras)

    def MOUSEMOTION(self, event):
        extras = {
            'pos': event.pos,
            'rel': event.rel,
            'buttons': event.buttons,
            'type': 'MOUSEMOTION'
        }
        return self.base_event(extras)
    
    def MOUSEWHEEL(self, event):
        extras = {
            'flipped': event.flipped,
            'pos': event.pos,
            'type': 'MOUSEWHEEL'
        }
        return self.base_event(extras)