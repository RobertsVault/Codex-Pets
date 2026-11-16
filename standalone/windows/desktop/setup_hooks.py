"""Merge companion hooks without replacing existing definitions or trust."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid
from task_hook import STATES

def configure(home, remove=False):
    path=home/'hooks.json'
    original=path.read_bytes() if path.exists() else None
    config=json.loads(original.decode('utf-8-sig')) if original else {'hooks':{}}
    hooks=config.setdefault('hooks',{})
    if not isinstance(hooks,dict):raise ValueError('Existing hooks must be an object')
    script=str(Path(__file__).with_name('task_hook.py').resolve())
    command=subprocess.list2cmdline([sys.executable,script])
    for event in STATES:
        groups=hooks.setdefault(event,[])
        if not isinstance(groups,list):raise ValueError('Invalid existing hook groups')
        cleaned=[]
        for group in groups:
            if not isinstance(group,dict):raise ValueError('Invalid existing hook group')
            handlers=group.get('hooks',[])
            kept=[h for h in handlers if h.get('command')!=command]
            if kept:cleaned.append({**group,'hooks':kept})
            elif not handlers:cleaned.append(group)
        if not remove:
            group={'hooks':[{'type':'command','command':command,'timeout':3}]}
            if event in ('PreToolUse','PostToolUse','PermissionRequest'):group['matcher']='.*'
            cleaned.append(group)
        hooks[event]=cleaned
    home.mkdir(parents=True,exist_ok=True)
    if original is not None:
        shutil.copyfile(path,home/('hooks.json.backup-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]))
    temporary=path.with_name('hooks.json.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Avoid silently overwriting a concurrent configuration edit.
    if (path.read_bytes() if path.exists() else None)!=original:
        temporary.unlink()
        raise RuntimeError('Hooks changed during installation; retry after reviewing them')
    os.replace(temporary,path)
    return path

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--remove',action='store_true')
    parser.add_argument('--home',type=Path,default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex'))))
    args=parser.parse_args()
    print(configure(args.home,args.remove))
    print('Hooks removed.' if args.remove else 'Registered. Restart/resume Codex and review/trust the new hooks before expecting task events. Trust is not changed by this installer.')
