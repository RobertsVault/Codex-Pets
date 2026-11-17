"""Local, content-free lifecycle events. No transcript or network access."""
from pathlib import Path
import hashlib
import json
import os
import time
import uuid
import math
import re

def data_dir():
    return Path(os.environ.get('CODEX_PETS_DATA',str(Path(os.environ.get('LOCALAPPDATA',str(Path.home()/'.local/share')))/'CodexPets')))

def write_event(state, session='manual', turn=''):
    folder=data_dir()/'events'
    folder.mkdir(parents=True,exist_ok=True)
    event={'id':uuid.uuid4().hex,'state':state,'task':hashlib.sha256((session+'|'+turn).encode()).hexdigest()[:24],
           'session':hashlib.sha256(session.encode()).hexdigest()[:24], 'at':time.time()}
    target=folder/(str(time.time_ns())+'-'+event['id']+'.json')
    temporary=target.with_suffix('.tmp')
    temporary.write_text(json.dumps(event),encoding='utf-8')
    os.replace(temporary,target)
    return event

class EventReader:
    def __init__(self):
        self.folder=data_dir()/'events'
        self.since=time.time()  # Never replay historical task states at startup.
        self.seen={path.name for path in self.folder.glob('*.json')}

    def poll(self):
        result=[]
        for path in self.folder.glob('*.json'):
            if path.name in self.seen: continue
            try:
                with path.open(encoding='utf-8') as stream: raw=stream.read(4097)
                if len(raw)>4096:continue
                value=json.loads(raw)
                if not isinstance(value,dict): continue
                stamp=value.get('at')
                if not isinstance(stamp,(int,float)) or isinstance(stamp,bool) or not math.isfinite(stamp):continue
                if not all(isinstance(value.get(key),str) and re.fullmatch(pattern,value[key])
                           for key,pattern in (('id',r'[0-9a-f]{32}'),('task',r'[0-9a-f]{24}'),('session',r'[0-9a-f]{24}'))):continue
                if stamp>=self.since and value.get('state') in {
                    'idle','coding','waiting','review','celebrate','failed'}:
                    if isinstance(value.get('task'),str): result.append(value)
                self.seen.add(path.name)
            except (OSError,ValueError,TypeError,RecursionError): pass
        return sorted(result,key=lambda x:(x['at'],x['id']))
