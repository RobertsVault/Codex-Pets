"""Silent lifecycle event receiver with redirected stdin support on Windows."""
import ctypes
import io
import os
import sys

def main():
    try:
        if sys.stdin is None:
            import msvcrt
            kernel=ctypes.WinDLL('kernel32',use_last_error=True)
            kernel.GetStdHandle.argtypes=[ctypes.c_ulong]
            kernel.GetStdHandle.restype=ctypes.c_void_p
            handle=kernel.GetStdHandle(-10 & 0xffffffff)
            if not handle or handle==ctypes.c_void_p(-1).value:return 0
            fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
            sys.stdin=io.TextIOWrapper(os.fdopen(fd,'rb',closefd=False),encoding='utf-8-sig')
        from task_hook import main as receive
        return receive()
    except Exception:
        return 0

if __name__=='__main__':raise SystemExit(main())
