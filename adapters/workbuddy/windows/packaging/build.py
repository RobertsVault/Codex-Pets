"""Build the self-contained Windows application and per-user installer."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import hashlib
from PIL import Image

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',required=True)
    parser.add_argument('--work-dir',type=Path,default=Path('build'))
    parser.add_argument('--output-dir',type=Path,default=Path('dist'))
    args=parser.parse_args()
    package=Path(__file__).resolve().parent
    windows=package.parent
    root=next(parent for parent in package.parents if (parent/'VERSION').is_file() and (parent/'native/pets').is_dir())
    work=args.work_dir.resolve();output=args.output_dir.resolve()
    work.mkdir(parents=True,exist_ok=True);output.mkdir(parents=True,exist_ok=True)
    desktop=windows/'desktop'
    with Image.open(root/'native/pets/doubao/spritesheet.png') as source:
        icon=source.crop((0,0,192,208)).convert('RGBA')
    square=Image.new('RGBA',(256,256));icon.thumbnail((220,220),Image.Resampling.LANCZOS)
    square.alpha_composite(icon,((256-icon.width)//2,(256-icon.height)//2))
    icon_file=work/'CodexPets.ico';square.save(icon_file,sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    for name,entry in (('CodexPets','app.py'),('CodexPetsHook','hook_entry.py')):
        command=[sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onedir','--windowed',
            '--name',name,'--specpath',str(work/'specs'),'--distpath',str(work/'frozen'),
            '--workpath',str(work/'analysis'/name),'--version-file',str(package/'version_info.txt'),
            '--icon',str(icon_file),'--exclude-module','fontTools']
        if name=='CodexPets':command.extend(['--add-data',str(desktop/'assets')+':assets'])
        command.append(str(desktop/entry))
        with (work/(name+'-build.log')).open('w',encoding='utf-8') as log:
            subprocess.run(command,check=True,stdout=log,stderr=subprocess.STDOUT)
        print(name+' bundle completed',flush=True)
    bundle=work/'frozen/CodexPets'
    helper=bundle/'helpers/CodexPetsHook';helper.parent.mkdir(exist_ok=True)
    shutil.copytree(work/'frozen/CodexPetsHook',helper,dirs_exist_ok=True)
    shutil.copyfile(icon_file,bundle/'CodexPets.ico')
    for name in ('LICENSE','VERSION'):
        shutil.copyfile(root/name,bundle/name)
    shutil.copyfile(windows/'INSTALL.md',bundle/'README.md')
    licenses=bundle/'licenses';licenses.mkdir(exist_ok=True)
    python_license=Path(sys.base_prefix)/'LICENSE.txt'
    if not python_license.exists():raise FileNotFoundError('CPython license is required')
    shutil.copyfile(python_license,licenses/'CPython-LICENSE.txt')
    pillow=importlib.metadata.distribution('Pillow')
    for file in pillow.files:
        if 'licenses/' in str(file).replace('\\','/'):
            destination=licenses/'Pillow'/Path(str(file).split('licenses/',1)[1])
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(pillow.locate_file(file),destination)
    for dependency in ('defusedxml','PyInstaller'):
        distribution=importlib.metadata.distribution(dependency)
        for file in distribution.files:
            if Path(str(file)).name.lower().startswith(('license','copying')):
                destination=licenses/dependency/Path(str(file)).name
                destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(distribution.locate_file(file),destination)
    versions={'CPython':'.'.join(map(str,sys.version_info[:3])),'Pillow':importlib.metadata.version('Pillow'),
        'PyInstaller':importlib.metadata.version('PyInstaller'),'defusedxml':importlib.metadata.version('defusedxml')}
    (bundle/'THIRD-PARTY-NOTICES.txt').write_text('Codex Pets 1.0.1\n\nBundled components:\n'+
        ''.join(name+' '+version+'\n' for name,version in versions.items())+
        '\nCPython, Pillow, defusedxml and PyInstaller license notices are included in licenses/. Tcl/Tk license.terms files are retained in the bundled runtime.\nPets CJK is a modified subset of Noto Sans SC. Its SIL Open Font License is included in _internal/assets/fonts/OFL.txt.\n',encoding='utf-8')
    with (work/'installer-build.log').open('w',encoding='utf-8') as log:
        subprocess.run([args.compiler,'/DBundleDir='+str(bundle),'/DOutputDir='+str(output),str(package/'installer.iss')],check=True,stdout=log,stderr=subprocess.STDOUT)
    portable=output/'Codex-Pets-WorkBuddy-1.0.1-Windows-x64-Portable.zip'
    with zipfile.ZipFile(portable,'w',zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(bundle.rglob('*')):
            if file.is_file():
                relative='Codex-Pets-WorkBuddy/'+file.relative_to(bundle).as_posix()
                info=zipfile.ZipInfo(relative,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644<<16;archive.writestr(info,file.read_bytes())
    files=sorted(output.glob('*.exe'))+[portable]
    (output/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(file.read_bytes()).hexdigest()+'  '+file.name+'\n' for file in files),encoding='ascii')
    print(json.dumps({'version':'1.0.1','components':versions,'artifacts':[{'name':file.name,'bytes':file.stat().st_size} for file in files]}))

if __name__=='__main__':main()
