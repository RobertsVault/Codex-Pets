from __future__ import annotations
import argparse
import ctypes
import json
import math
from pathlib import Path
import random
import sys
import time
import tkinter as tk
from events import EventReader, data_dir
from state_engine import StateEngine, HOLD
from i18n import tr, STATE_LABELS
from expanded_animation import load_manifest,frame_index
from alpha_window import AlphaWindow,register_private_fonts

# Layered-window pixels and Tk geometry must use the same physical coordinates.
if sys.platform=='win32':
    ctypes.windll.user32.SetProcessDPIAware()

APP=Path(__file__).resolve().parent
LABELS={'idle':'待机陪伴','coding':'任务处理中','waiting':'等待输入／批准','review':'检查结果',
        'celebrate':'完成啦','failed':'遇到问题','petting':'摸摸头','eating':'吃点零食','ball':'一起玩球',
        'begging':'握个爪','roll':'摸摸肚皮','run':'奔跑','trot':'散步','sniff':'看看周围','sleep':'睡觉充电','curious':'思考一下'}
ROWS={'idle':0,'run':1,'trot':1,'petting':3,'begging':3,'ball':4,'celebrate':4,
      'failed':5,'sleep':5,'waiting':6,'coding':7,'review':8,'eating':0,'roll':3,'sniff':8,'curious':0}
COUNTS=[6,8,8,4,5,8,6,6,6,8,8]
DOG={'idle':'idle','coding':'coding','celebrate':'celebrate','sleep':'sleep','petting':'petting',
     'eating':'eating','ball':'ball','begging':'begging','run':'run','trot':'trot','sniff':'sniff',
     'roll':'roll','waiting':'begging','review':'sniff','failed':'sleep','curious':'sniff'}

class Companion:
    def __init__(self,pet='doubao',hidden=False,language=None):
        self.pet=pet
        self.ui_font=register_private_fonts()
        self.root=tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg='#ff00ff')
        self.root.attributes('-topmost',True)
        self.canvas=tk.Canvas(self.root,width=340,height=350,bg='#ff00ff',highlightthickness=0)
        self.canvas.pack()
        self.engine=StateEngine()
        self.reader=EventReader()
        self.received_event=False
        self.settings_path=data_dir()/(pet+'-settings.json')
        self.settings={}
        try:
            obj=json.loads(self.settings_path.read_text(encoding='utf-8'))
            if isinstance(obj,dict): self.settings=obj
        except (OSError,ValueError): pass
        preferred=language or self.settings.get('language','zh')
        self.language=tk.StringVar(value=preferred if preferred in ('zh','en') else 'zh')
        saved_scale=self.settings.get('scale',2.0)
        self.scale=tk.DoubleVar(value=saved_scale if saved_scale in (1,1.5,2) else 2.0)
        self.root.title(self.text('window',name=self.text('name_'+pet)))
        self.roaming=tk.BooleanVar(value=bool(self.settings.get('roaming',False)))
        self.expanded=tk.BooleanVar(value=bool(self.settings.get('expanded',True)))
        self.gaze=tk.BooleanVar(value=bool(self.settings.get('gaze',True)))
        self.follow=tk.BooleanVar(value=True)
        self.topmost=tk.BooleanVar(value=True)
        self.direction=1
        self.dragging=False
        self.drag_start=None
        self.affection=int(self.settings.get('affection',0))
        self.started=time.monotonic()
        self.clip_epoch=self.started
        self.next_roam=self.started+10
        self.previous=None
        self.notice_key='hint'
        self.notice_until=0
        self.hover_job=None
        self.closed=False
        self.after_jobs=[]
        self.images={}
        self.frames=[]
        self.motion={}
        self.expanded_clips=load_manifest(APP/'assets',pet)
        self.expanded_frames={}
        for state,clip in self.expanded_clips.items():
            strip=tk.PhotoImage(file=str(APP/'assets/animations'/clip['file']))
            frames=[]
            for index in range(clip['frames']):
                frame=tk.PhotoImage(width=192,height=208)
                frame.tk.call(frame,'copy',strip,'-from',index*192,0,(index+1)*192,208,'-to',0,0)
                frames.append(frame)
            self.expanded_frames[state]=frames
        self.look_current=0
        self.look_changed=0
        self.look_seen=0
        for kind,count in (('run',8),('run-left',8),('look',16)):
            strip=tk.PhotoImage(file=str(APP/'assets/animations'/pet/(kind+'.png')))
            frames=[]
            for index in range(count):
                frame=tk.PhotoImage(width=192,height=208)
                frame.tk.call(frame,'copy',strip,'-from',index*192,0,(index+1)*192,208,'-to',0,0)
                frames.append(frame)
            self.motion[kind]=frames
        if pet=='doubao':
            for name in {pose for state,pose in DOG.items() if state not in ('run','trot')}|{'sniff-left'}:
                image=tk.PhotoImage(file=str(APP/'assets/poses/doubao'/(name+'.png')))
                self.images[name]=image
        else:
            atlas=tk.PhotoImage(file=str(APP/'assets/atlas/mikan.png'))
            for row,count in enumerate(COUNTS):
                frames=[]
                for col in range(count):
                    frame=tk.PhotoImage(width=192,height=208)
                    frame.tk.call(frame,'copy',atlas,'-from',col*192,row*208,(col+1)*192,(row+1)*208,'-to',0,0)
                    frames.append(frame)
                self.frames.append(frames)
        self.sprite=self.canvas.create_image(170,180,anchor='center')
        self.bubble_bg=self.canvas.create_rectangle(10,8,330,57,fill='',outline='',state='hidden')
        self.title=self.canvas.create_text(170,305,text='',fill='#543c30',font=(self.ui_font,12,'bold'))
        self.detail=self.canvas.create_text(170,330,text='',fill='#543c30',font=(self.ui_font,9))
        self.bubble=self.canvas.create_text(170,32,text='',width=320,fill='#543c30',font=(self.ui_font,10,'bold'))
        self.menu=self.make_menu()
        width,height=self.viewport_size()
        self.canvas.configure(width=width,height=height)
        x=max(0,min(int(self.settings.get('x',self.root.winfo_screenwidth()-width-30)),self.root.winfo_screenwidth()-width))
        y=max(0,min(int(self.settings.get('y',self.root.winfo_screenheight()-height-70)),self.root.winfo_screenheight()-height))
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.canvas.bind('<ButtonPress-1>',self.drag_begin)
        self.canvas.bind('<B1-Motion>',self.drag_move)
        self.canvas.bind('<ButtonRelease-1>',self.drag_end)
        self.canvas.bind('<Double-Button-1>',lambda e:self.interact('ball'))
        self.canvas.bind('<Button-2>',lambda e:self.interact('eating'))
        self.canvas.bind('<Button-3>',self.popup)
        self.canvas.bind('<Enter>',self.enter)
        self.canvas.bind('<Leave>',self.leave)
        self.root.bind('<Escape>',lambda e:self.close())
        self.root.bind('<space>',lambda e:self.interact('petting'))
        if hidden:self.root.withdraw()
        self.alpha_window=AlphaWindow(self.root,self.scale.get())
        self.tick()
        self.poll()

    def make_menu(self):
        menu=tk.Menu(self.root,tearoff=False,font=(self.ui_font,10))
        for state in ('petting','eating','ball','begging','roll','run','trot','sniff','sleep'):
            menu.add_command(label=self.text('minimum',name=self.text('state_'+state),seconds=HOLD[state]),command=lambda s=state:self.interact(s))
        demo=tk.Menu(menu,tearoff=False)
        for state in ('idle','coding','waiting','review','celebrate','failed'):
            demo.add_command(label=self.text('state_'+state),command=lambda s=state:self.demo(s))
        menu.add_cascade(label=self.text('demo_menu'),menu=demo)
        menu.add_separator()
        menu.add_checkbutton(label=self.text('follow'),variable=self.follow,command=self.set_follow)
        menu.add_checkbutton(label=self.text('roam'),variable=self.roaming)
        menu.add_checkbutton(label=self.text('gaze'),variable=self.gaze)
        menu.add_checkbutton(label=self.text('expanded'),variable=self.expanded,command=self.toggle_expanded)
        menu.add_checkbutton(label=self.text('topmost'),variable=self.topmost,command=lambda:self.root.attributes('-topmost',self.topmost.get()))
        sizes=tk.Menu(menu,tearoff=False)
        for value in (1,1.5,2):
            sizes.add_radiobutton(label=f'{value:g}×',value=value,variable=self.scale,command=self.apply_scale)
        menu.add_cascade(label=self.text('size'),menu=sizes)
        languages=tk.Menu(menu,tearoff=False)
        for value,label in (('zh','中文'),('en','English')):
            languages.add_radiobutton(label=label,value=value,variable=self.language,command=lambda:self.root.after_idle(self.apply_language))
        menu.add_cascade(label=self.text('language'),menu=languages)
        menu.add_command(label=self.text('reset'),command=self.reset)
        menu.add_command(label=self.text('exit'),command=self.close)
        return menu

    def text(self,key,**values):
        return tr(self.language.get(),key,**values)

    def viewport_size(self):
        return round(340*self.scale.get()),round(350*self.scale.get())

    def apply_scale(self):
        old=self.alpha_window.scale
        new=self.scale.get()
        width,height=self.viewport_size()
        x=round(self.root.winfo_x()+170*(old-new))
        y=round(self.root.winfo_y()+180*(old-new))
        x=max(0,min(x,self.root.winfo_screenwidth()-width))
        y=max(0,min(y,self.root.winfo_screenheight()-height))
        self.canvas.configure(width=width,height=height)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.alpha_window.set_scale(new)
        self.root.update_idletasks()
        if self.alpha_window.last_args:
            self.alpha_window.present(*self.alpha_window.last_args)
        self.save_settings()

    def toggle_expanded(self):
        self.clip_epoch=time.monotonic()
        self.save_settings()

    def apply_language(self):
        # Change presentation only: retain tasks, animation phase and hold timers.
        previous=self.menu
        self.menu=self.make_menu()
        previous.destroy()
        self.root.title(self.text('window',name=self.text('name_'+self.pet)))
        self.save_settings()

    def notice(self,key):
        self.notice_key=key
        self.notice_until=time.monotonic()+6

    def interact(self,state):
        if self.engine.busy:
            self.notice('busy')
            return
        display=self.engine.update()
        if display.source not in ('auto','idle','manual') and display.until>time.monotonic():
            self.notice('result_first')
            return
        self.engine.interact(state)
        self.clip_epoch=time.monotonic()
        self.affection+=1
        self.notice('state_'+state)

    def demo(self,state):
        self.follow.set(False)
        self.engine.follow=False
        self.engine.tasks.clear()
        self.engine.reset()
        if state in ('coding','waiting'): self.engine.interact(state,seconds=10**9)
        elif state!='idle': self.engine.interact(state)
        self.clip_epoch=time.monotonic()
        self.notice('demo_notice')

    def set_follow(self):
        self.engine.follow=self.follow.get()
        self.engine.reset()
        self.notice('follow_on' if self.follow.get() else 'follow_off')

    def reset(self):
        self.engine.tasks.clear()
        self.engine.reset()
        self.notice('reset_notice')

    def popup(self,event):
        self.dragging=True
        try:self.menu.tk_popup(event.x_root,event.y_root)
        finally:self.menu.grab_release();self.dragging=False

    def enter(self,event):
        self.leave(event)
        self.hover_job=self.root.after(1200,self.hover)

    def hover(self):
        self.hover_job=None
        if self.engine.update().state=='idle':self.interact('begging')

    def leave(self,event):
        if self.hover_job is not None:self.root.after_cancel(self.hover_job);self.hover_job=None
        # Never cancel a gesture merely because the pointer moved away.

    def drag_begin(self,event):
        self.dragging=True
        self.drag_start=(event.x_root,event.y_root,self.root.winfo_x(),self.root.winfo_y())
        self.drag_distance=0

    def drag_move(self,event):
        if self.drag_start is None:return
        x,y,wx,wy=self.drag_start
        dx,dy=event.x_root-x,event.y_root-y
        self.drag_distance=max(self.drag_distance,abs(dx)+abs(dy))
        width,height=self.viewport_size()
        nx=max(0,min(wx+dx,self.root.winfo_screenwidth()-width))
        ny=max(0,min(wy+dy,self.root.winfo_screenheight()-height))
        self.root.geometry(f'+{nx}+{ny}')

    def drag_end(self,event):
        self.dragging=False
        if self.drag_start is not None and self.drag_distance<7:self.interact('petting')
        self.drag_start=None

    def poll(self):
        for event in self.reader.poll():
            self.received_event=True
            self.engine.task(event['task'],event['state'])
            if event['state']=='idle':
                # SessionEnd may omit turn_id; clear all tasks in that session.
                for key in getattr(self,'sessions',{}).get(event['session'],set()):
                    self.engine.task(key,'idle')
            if not hasattr(self,'sessions'):self.sessions={}
            self.sessions.setdefault(event['session'],set()).add(event['task'])
        self.after_jobs.append(self.root.after(400,self.poll))

    def tick(self):
        now=time.monotonic()
        display=self.engine.update()
        if self.roaming.get() and display.state=='idle' and now>=self.next_roam:
            self.engine.roam(random.choice(('run','trot','sniff')))
            self.next_roam=now+random.uniform(12,18)
            display=self.engine.update()
        state=display.state
        if state!=self.previous:self.started=now;self.clip_epoch=now;self.previous=state
        clip_state={'curious':'review','sniff':'review'}.get(state,state)
        if self.expanded.get() and clip_state in self.expanded_clips:
            index=frame_index(self.expanded_clips[clip_state],now-self.clip_epoch)
            image=self.expanded_frames[clip_state][index]
        elif state in ('run','trot'):
            frames=self.motion['run-left' if self.direction<0 else 'run']
            image=frames[int((now-self.started)*(8 if state=='run' else 5))%8]
        elif self.pet=='doubao':
            pose=DOG[state]
            if self.direction<0 and pose in ('run','trot','sniff'):pose+='-left'
            image=self.images[pose]
        else:
            row=ROWS[state]
            if state in ('run','trot') and self.direction<0:row=2
            frames=self.frames[row]
            image=frames[int((now-self.started)*6)%len(frames)]
        if state=='idle' and self.gaze.get() and not self.dragging and (not self.expanded.get() or now-self.clip_epoch>=3):
            px,py=self.root.winfo_pointerxy()
            dx=px-(self.root.winfo_x()+170*self.scale.get())
            dy=py-(self.root.winfo_y()+180*self.scale.get())
            if 12<math.hypot(dx,dy)<500:
                target=int(math.floor(((math.degrees(math.atan2(dx,-dy))+360)%360)/22.5+.5))%16
                self.look_seen=now
                if now-self.look_changed>=.09:
                    difference=(target-self.look_current+8)%16-8
                    if difference:self.look_current=(self.look_current+(1 if difference>0 else -1))%16
                    self.look_changed=now
                image=self.motion['look'][self.look_current]
            elif now-self.look_seen<.8:
                image=self.motion['look'][self.look_current]
        self.canvas.itemconfigure(self.sprite,image=image)
        self.canvas.coords(self.sprite,170,180+math.sin((now-self.started)*4)*3)
        if state in ('run','trot') and not self.dragging:
            x=self.root.winfo_x()+round((4 if state=='run' else 2)*self.scale.get())*self.direction
            limit=max(0,self.root.winfo_screenwidth()-self.viewport_size()[0])
            if x<=0 or x>=limit:self.direction*=-1
            self.root.geometry(f'+{max(0,min(x,limit))}+{self.root.winfo_y()}')
        label=self.text('state_'+state)
        if state=='waiting':label+=self.text('waiting_suffix')
        elif state=='coding':label+=self.text('working_suffix')
        elif display.until>now:label+=self.text('countdown',seconds=math.ceil(display.until-now))
        self.canvas.itemconfigure(self.title,text=label)
        self.canvas.itemconfigure(self.detail,text=self.text(('follow_status' if self.received_event else 'await_events') if self.follow.get() else 'demo_status')+self.text('affection',value=self.affection))
        self.canvas.itemconfigure(self.bubble,text=self.text(self.notice_key) if now<self.notice_until else '')
        self.canvas.itemconfigure(self.bubble_bg,state='normal' if now<self.notice_until else 'hidden')
        self.alpha_window.present(image,180+math.sin((now-self.started)*4)*3,
            label,self.canvas.itemcget(self.detail,'text'),self.canvas.itemcget(self.bubble,'text'))
        self.after_jobs.append(self.root.after(50,self.tick))
        # Keep only live timer IDs for orderly shutdown.
        if len(self.after_jobs)>100:self.after_jobs=[x for x in self.after_jobs if x in self.root.tk.call('after','info')]

    def close(self):
        if self.closed:return
        self.closed=True
        self.leave(None)
        for job in self.after_jobs:
            try:self.root.after_cancel(job)
            except tk.TclError:pass
        self.save_settings()
        self.alpha_window.close()
        self.root.destroy()

    def save_settings(self):
        import os,uuid
        self.settings_path.parent.mkdir(parents=True,exist_ok=True)
        target=self.settings_path.with_suffix('.'+uuid.uuid4().hex+'.tmp')
        target.write_text(json.dumps({'x':self.root.winfo_x(),'y':self.root.winfo_y(),
            'affection':self.affection,'roaming':self.roaming.get(),'gaze':self.gaze.get(),
            'language':self.language.get(),'expanded':self.expanded.get(),'scale':self.scale.get()}),encoding='utf-8')
        os.replace(target,self.settings_path)

_mutex=None
def main():
    global _mutex
    parser=argparse.ArgumentParser()
    parser.add_argument('--pet',choices=('mikan','doubao'),default='doubao')
    parser.add_argument('--language',choices=('zh','en'))
    args=parser.parse_args()
    if sys.platform!='win32':parser.error('Standalone transparent desktop mode requires Windows.')
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateMutexW.restype=ctypes.c_void_p
    _mutex=kernel.CreateMutexW(None,False,'Local\\CodexPetsWorkBuddy_'+args.pet)
    if ctypes.get_last_error()==183:return
    app=Companion(args.pet,language=args.language)
    app.root.mainloop()

if __name__=='__main__':main()
