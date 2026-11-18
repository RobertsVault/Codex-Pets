"""Desktop application and optional task integration settings."""
import argparse
import logging
import os
from pathlib import Path
import sys

VERSION='1.1.0'

def main():
    parser=argparse.ArgumentParser(description='Codex Pets desktop companion')
    parser.add_argument('--pet',choices=('doubao','mikan'),default='doubao')
    parser.add_argument('--language',choices=('zh','en'))
    parser.add_argument('--configure-hooks',choices=('enable','disable'))
    parser.add_argument('--home',type=Path)
    parser.add_argument('--quiet',action='store_true')
    args=parser.parse_args()
    from events import data_dir
    data_dir().mkdir(parents=True,exist_ok=True)
    logging.basicConfig(filename=str(data_dir()/'application.error.log'),level=logging.ERROR,encoding='utf-8')
    try:
        if args.configure_hooks:
            from setup_hooks import configure
            home=args.home or Path(os.environ.get('WORKBUDDY_HOME',str(Path.home()/'.workbuddy')))
            configure(home,remove=args.configure_hooks=='disable')
            if not args.quiet:
                import tkinter as tk
                from tkinter import messagebox
                root=tk.Tk();root.withdraw()
                zh=args.language!='en'
                if args.configure_hooks=='enable':
                    message=('已配置任务跟随。请重启或恢复 WorkBuddy，并审阅、信任新增 hooks 后使用。' if zh else 'Task integration configured. Restart/resume WorkBuddy and review/trust the added hooks before use.')
                else:
                    message=('已移除此安装目录的任务跟随配置。' if zh else 'Task integration for this installation has been removed.')
                messagebox.showinfo('Codex Pets',message,parent=root);root.destroy()
            return 0
        from companion import main as companion_main
        sys.argv=[sys.argv[0],'--pet',args.pet]+(['--language',args.language] if args.language else [])
        companion_main()
        return 0
    except Exception:
        logging.exception('Application operation failed')
        if not args.quiet:
            import ctypes
            ctypes.windll.user32.MessageBoxW(None,
                '无法启动或完成配置，请查看本机 CodexPetsWorkBuddy 数据目录中的错误日志。\nUnable to start or configure the application. See the local CodexPetsWorkBuddy error log.',
                'Codex Pets',0x10)
        return 1

if __name__=='__main__':raise SystemExit(main())
