"""Merge companion hooks without replacing existing definitions or trust."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
import uuid
from task_hook import STATES as ALL_STATES
STATES={k:v for k,v in ALL_STATES.items() if k!="StopFailure"}

def configure(home, remove=False):
    path=home/'settings.json'
    original=path.read_bytes() if path.exists() else None
    if remove and original is None:return path
    config=json.loads(original.decode('utf-8-sig')) if original else {'hooks':{}}
    hooks=config.setdefault('hooks',{})
    if not isinstance(hooks,dict):raise ValueError('Existing hooks must be an object')
    if getattr(sys,'frozen',False):
        executable=Path(sys.executable).parent/'helpers/CodexPetsHook/CodexPetsHook.exe'
        if not executable.is_file():raise FileNotFoundError('Task integration helper is missing')
        arguments=[executable.as_posix()]
        legacy_commands={subprocess.list2cmdline([str(executable)]),'"'+executable.as_posix()+'"'}
    else:
        script=Path(__file__).with_name('task_hook.py').resolve()
        arguments=[Path(sys.executable).as_posix(),script.as_posix()]
        legacy_commands={subprocess.list2cmdline([sys.executable,str(script)])}
    if any(any(char in value for char in ('\0','\r','\n')) for value in arguments):
        raise ValueError('Invalid command path')
    command=shlex.join(arguments)
    bases=legacy_commands|{command}
    owned=bases|{base+" --event "+name for name in STATES for base in bases}
    for event in STATES:
        groups=hooks.setdefault(event,[])
        if not isinstance(groups,list):raise ValueError('Invalid existing hook groups')
        cleaned=[]
        for group in groups:
            if not isinstance(group,dict):raise ValueError('Invalid existing hook group')
            handlers=group.get('hooks',[])
            kept=[h for h in handlers if h.get('command') not in owned]
            if kept:cleaned.append({**group,'hooks':kept})
            elif not handlers:cleaned.append(group)
        if not remove:
            group={'hooks':[{'type':'command','command':command+' --event '+event,'timeout':3}]}
            if event in ('PreToolUse','PostToolUse','PermissionRequest'):group['matcher']='.*'
            cleaned.append(group)
        hooks[event]=cleaned
    if remove and json.loads(original.decode('utf-8-sig'))==config:return path
    home.mkdir(parents=True,exist_ok=True)
    if original is not None:
        shutil.copyfile(path,home/('settings.json.backup-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]))
    temporary=path.with_name('settings.json.'+uuid.uuid4().hex+'.tmp')
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
    parser.add_argument('--home',type=Path,default=Path(os.environ.get('WORKBUDDY_HOME',str(Path.home()/'.workbuddy'))))
    args=parser.parse_args()
    print(configure(args.home,args.remove))
    print('Hooks removed.' if args.remove else 'Registered. Restart/resume WorkBuddy and review/trust the new hooks before expecting task events. Trust is not changed by this installer.')
