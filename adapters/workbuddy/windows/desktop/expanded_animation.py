"""Sprite animation manifest and timeline selection."""
import json
from pathlib import Path

def load_manifest(assets,pet):
    path=Path(assets)/'animations/expanded.json'
    if not path.exists():return {}
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('version')!=1 or data.get('cell')!=[192,208]:raise ValueError('Unsupported animation manifest')
    result=data['pets'][pet]
    for state,clip in result.items():
        file=Path(clip['file'])
        if file.is_absolute() or '..' in file.parts or not file.parts or file.parts[0]!=pet:
            raise ValueError('Animation file must stay inside its pet directory')
        count=clip['frames'];durations=clip['durationsMs'];start=clip['loopStart']
        if count!=len(durations) or count<2 or not 0<=start<count or not all(isinstance(x,int) and x>0 for x in durations):
            raise ValueError('Invalid animation timing')
    return result

def frame_index(clip,elapsed):
    timing=clip['durationsMs']
    start=clip['loopStart']
    position=max(0,elapsed)*1000
    intro=sum(timing[:start])
    if position>=intro:position=intro+(position-intro)%sum(timing[start:])
    for index,duration in enumerate(timing):
        if position<duration:return index
        position-=duration
    return len(timing)-1
