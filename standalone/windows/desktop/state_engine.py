"""Deterministic presentation rules shared by both standalone pets."""
from dataclasses import dataclass
import time

HOLD = {'idle': 0, 'coding': 8, 'waiting': 8, 'review': 10, 'celebrate': 10,
        'failed': 10, 'petting': 5, 'eating': 5, 'ball': 6, 'begging': 5,
        'roll': 5, 'run': 6, 'trot': 6, 'sniff': 5, 'sleep': 10, 'curious': 5}
ALIASES = {'work':'coding','working':'coding','running':'coding','think':'curious',
           'thinking':'curious','done':'celebrate','success':'celebrate','rest':'sleep',
           'error':'failed','approval':'waiting'}

@dataclass
class Display:
    state: str = 'idle'
    until: float = 0
    source: str = 'idle'

class StateEngine:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.display = Display()
        self.tasks = {}
        self.manual = None
        self.follow = True
        self.last_task = None

    def task(self, key, state):
        state = ALIASES.get(state, state)
        if state not in HOLD: raise ValueError(state)
        self.tasks[key] = (state, self.clock())

    def interact(self, state, seconds=None):
        state = ALIASES.get(state, state)
        if state not in HOLD: raise ValueError(state)
        now = self.clock()
        self.manual = Display(state, now + max(HOLD[state], seconds or 0), 'manual')

    def reset(self):
        self.manual = None
        self.display = Display()
        self.last_task = None

    def update(self):
        now = self.clock()
        active = [(key,state,stamp) for key,(state,stamp) in self.tasks.items()
                  if self.follow and state in ('coding','waiting')]
        if active:
            key,state,stamp = max(active,key=lambda x:(x[1]=='waiting',x[2]))
            self.manual = None  # Task states never build a deferred interaction queue.
            if self.display.source != key or self.display.state != state:
                self.display = Display(state, now + HOLD[state], key)
            self.last_task = key
            return self.display
        # Completion/failure ends the task immediately; its own hold begins now.
        if self.last_task is not None:
            key = self.last_task
            self.last_task = None
            state,_ = self.tasks.get(key,('idle',now))
            self.display = Display(state,now+HOLD[state],key)
        # A newly completed short task must still appear even if no work frame was shown.
        terminal = [(key,state,stamp) for key,(state,stamp) in self.tasks.items()
                    if self.follow and state in ('celebrate','review','failed')
                    and stamp + HOLD[state] > now]
        if terminal:
            key,state,stamp = max(terminal,key=lambda x:x[2])
            if self.display.source != key or self.display.state != state:
                self.display = Display(state, now+HOLD[state], key)
        if self.follow and self.display.source not in ('idle','manual','auto') and now < self.display.until:
            self.manual = None
            return self.display
        if self.manual is not None:
            if now < self.manual.until:
                self.display = self.manual
                return self.display
            self.manual = None
        if now < self.display.until:
            return self.display
        self.display = Display()
        return self.display

    def roam(self, state):
        if self.update().state == 'idle':
            self.display = Display(state,self.clock()+HOLD[state],'auto')

    @property
    def busy(self):
        return self.follow and any(state in ('coding','waiting') for state,_ in self.tasks.values())
