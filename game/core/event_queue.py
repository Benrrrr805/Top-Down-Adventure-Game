class EventQueue:
    def __init__(self, pygame, debug, max_events=1000):
        self.pygame = pygame
        self.debug = debug
        self.max_events = max_events

        self.event_queue = None
        self.last_mouse_pos = None

        # Map raw pygame event types to handling methods
        self.event_mapping = {
            self.pygame.MOUSEBUTTONDOWN: self.MOUSEBUTTONDOWN,
            self.pygame.MOUSEBUTTONUP: self.MOUSEBUTTONUP,
            self.pygame.KEYDOWN: self.KEYDOWN,
            self.pygame.KEYUP: self.KEYUP,
            self.pygame.QUIT: self.QUIT,
            self.pygame.MOUSEMOTION: self.MOUSEMOTION,
            self.pygame.MOUSEWHEEL: self.MOUSEWHEEL,
        }

        # List of event 'type' strings that this queue handles
        self.handled_events = [
            "MOUSEBUTTONDOWN",
            "MOUSEBUTTONUP",
            "KEYDOWN",
            "KEYUP",
            "QUIT",
            "MOUSEMOTION",
            "MOUSEWHEEL",
        ]

    def init_queue(self):
        """
        Initialize the internal event queue (list).
        """
        self.event_queue = []

    def validate_queue(self, recursive=False):
        """
        Validate that the queue is a list and optionally validate each event.
        """
        if self.event_queue is None:
            raise ValueError("Event queue is None")

        if not isinstance(self.event_queue, list):
            raise ValueError("Event queue is not a list")

        if recursive:
            for event in self.event_queue:
                self.validate_event(event)

        return True

    def validate_event(self, event):
        """
        Validate a single event dictionary for required keys.
        """
        if not isinstance(event, dict):
            raise ValueError("Event is not a dictionary")

        if "type" not in event:
            raise ValueError("Event does not have a type")

        if "timestamp" not in event:
            raise ValueError("Event does not have a timestamp")

        if event["type"] not in self.handled_events:
            raise ValueError(f"Event type not handled: {event['type']}")

        return True

    def add_event(self, event):
        """
        Add a validated event to the internal queue.
        """
        self.validate_event(event)
        self.event_queue.append(event)

    def get_last_event(self):
        """
        Retrieve and remove the first event (FIFO) from the queue.
        Returns None if the queue is empty.
        """
        if self.event_queue:
            return self.event_queue.pop(0)
        return None

    def has_event(self, event_type, extras=None):
        """
        Check if an event of the given type (and optional extras) exists in the queue.
        """
        if event_type not in self.handled_events:
            return False

        for e in self.event_queue:
            if e["type"] == event_type:
                if extras is None:
                    return True
                # All extras must match
                if all(e.get(k) == v for k, v in extras.items()):
                    return True
        return False

    def remove_event(self, event_type):
        """
        Remove all events of a given type from the queue.
        """
        self.event_queue = [e for e in self.event_queue if e["type"] != event_type]

    def handle_events(self):
        """
        Poll raw pygame events and transform them into the internal queue using event mappings.
        """
        raw_pygame_events = self.pygame.event.get()

        for event in raw_pygame_events:
            if event.type in self.event_mapping:
                # For mouse movement, just store the position, don't queue it
                if event.type == self.pygame.MOUSEMOTION:
                    self.last_mouse_pos = event.pos
                else:
                    converted = self.event_mapping[event.type](event)
                    self.add_event(converted)

        # Enforce max_events limit
        while len(self.event_queue) > self.max_events:
            self.event_queue.pop(0)

    def base_event(self, extras):
        """
        Create a base event dict with a timestamp and any additional extras.
        """
        event = {"timestamp": self.pygame.time.get_ticks()}
        event.update(extras)
        return event

    def MOUSEBUTTONDOWN(self, event):
        extras = {
            "type": "MOUSEBUTTONDOWN",
            "button": event.button,
            "pos": event.pos,
        }
        return self.base_event(extras)

    def MOUSEBUTTONUP(self, event):
        extras = {
            "type": "MOUSEBUTTONUP",
            "button": event.button,
            "pos": event.pos,
        }
        return self.base_event(extras)

    def KEYDOWN(self, event):
        extras = {
            "type": "KEYDOWN",
            "key": event.key,
            "mod": event.mod,
            "unicode": event.unicode,
        }
        return self.base_event(extras)

    def KEYUP(self, event):
        extras = {
            "type": "KEYUP",
            "key": event.key,
            "mod": event.mod,
        }
        return self.base_event(extras)

    def QUIT(self, event):
        extras = {"type": "QUIT"}
        return self.base_event(extras)

    def MOUSEMOTION(self, event):
        extras = {
            "type": "MOUSEMOTION",
            "pos": event.pos,
            "rel": event.rel,
            "buttons": event.buttons,
        }
        return self.base_event(extras)

    def MOUSEWHEEL(self, event):
        extras = {
            "type": "MOUSEWHEEL",
            "flipped": event.flipped,
            "pos": event.pos,
        }
        return self.base_event(extras)
