"""Per-pixel alpha composition for Windows; never blend sprites against a key color."""
import ctypes as C
from ctypes import wintypes as W
from io import BytesIO
from pathlib import Path
import os
from PIL import Image, ImageChops, ImageDraw, ImageFont

FONT_ASSETS=Path(__file__).resolve().parent/'assets/fonts'

def register_private_fonts():
    if os.name=='nt':
        gdi=C.WinDLL('gdi32',use_last_error=True)
        gdi.AddFontResourceExW.argtypes=[W.LPCWSTR,W.DWORD,C.c_void_p]
        for name in ('PetsCJK-Regular.ttf','PetsCJK-Bold.ttf'):
            file=FONT_ASSETS/name
            if file.is_file():gdi.AddFontResourceExW(str(file),0x10,None)
    folder=Path(os.environ.get('WINDIR',os.environ.get('SYSTEMROOT','/Windows')))/'Fonts'
    return 'Microsoft YaHei UI' if (folder/'msyh.ttc').is_file() else 'Pets CJK'


def clean_sprite(image):
    image = image.convert('RGBA').copy()
    # Discard nearly invisible background pixels before compositing.
    alpha = image.getchannel('A').point(lambda a: 0 if a < 32 else a)
    image.putalpha(alpha)
    return image


def premultiplied_bgra(image):
    r, g, b, a = image.split()
    return Image.merge('RGBA', (ImageChops.multiply(b, a),
        ImageChops.multiply(g, a), ImageChops.multiply(r, a), a)).tobytes()


class SIZE(C.Structure):
    _fields_ = [('cx', W.LONG), ('cy', W.LONG)]


class BLEND(C.Structure):
    _fields_ = [('op', C.c_ubyte), ('flags', C.c_ubyte),
                ('constant', C.c_ubyte), ('format', C.c_ubyte)]


class HEADER(C.Structure):
    _fields_ = [('size', W.DWORD), ('width', W.LONG), ('height', W.LONG),
        ('planes', W.WORD), ('bits', W.WORD), ('compression', W.DWORD),
        ('image_size', W.DWORD), ('xppm', W.LONG), ('yppm', W.LONG),
        ('used', W.DWORD), ('important', W.DWORD)]


class AlphaWindow:
    def __init__(self, root, scale=2.0):
        self.root = root
        self.cache = {}
        self.fonts = {}
        self.last_frame = None
        self.last_args = None
        self.user = C.WinDLL('user32', use_last_error=True)
        self.gdi = C.WinDLL('gdi32', use_last_error=True)
        self.user.GetAncestor.argtypes = [W.HWND, W.UINT]
        self.user.GetAncestor.restype = W.HWND
        self.user.GetWindowLongW.argtypes = [W.HWND, C.c_int]
        self.user.SetWindowLongW.argtypes = [W.HWND, C.c_int, W.LONG]
        self.user.GetDC.argtypes = [W.HWND]
        self.user.GetDC.restype = W.HDC
        self.user.ReleaseDC.argtypes = [W.HWND, W.HDC]
        self.gdi.CreateCompatibleDC.argtypes = [W.HDC]
        self.gdi.CreateCompatibleDC.restype = W.HDC
        self.gdi.CreateDIBSection.argtypes = [W.HDC, C.c_void_p, W.UINT,
            C.POINTER(C.c_void_p), W.HANDLE, W.DWORD]
        self.gdi.CreateDIBSection.restype = W.HBITMAP
        self.gdi.SelectObject.argtypes = [W.HDC, W.HANDLE]
        self.gdi.SelectObject.restype = W.HANDLE
        self.gdi.DeleteObject.argtypes = [W.HANDLE]
        self.gdi.DeleteDC.argtypes = [W.HDC]
        self.user.UpdateLayeredWindow.argtypes = [W.HWND, W.HDC,
            C.POINTER(W.POINT), C.POINTER(SIZE), W.HDC,
            C.POINTER(W.POINT), W.DWORD, C.POINTER(BLEND), W.DWORD]
        self.root.update_idletasks()
        self.hwnd = self.user.GetAncestor(root.winfo_id(), 2)
        style = self.user.GetWindowLongW(self.hwnd, -20)
        self.user.SetWindowLongW(self.hwnd, -20, style | 0x80000)
        self.screen = self.user.GetDC(None)
        self.dc = self.gdi.CreateCompatibleDC(self.screen)
        self.bitmap = None
        self.set_scale(scale)

    def set_scale(self, scale):
        if scale not in (1, 1.5, 2):
            raise ValueError('Unsupported display scale')
        width, height = round(340 * scale), round(350 * scale)
        header = HEADER(C.sizeof(HEADER), width, -height, 1, 32)
        bits = C.c_void_p()
        bitmap = self.gdi.CreateDIBSection(self.screen, C.byref(header), 0,
            C.byref(bits), None, 0)
        if not bitmap:
            raise C.WinError(C.get_last_error())
        previous = self.gdi.SelectObject(self.dc, bitmap)
        if self.bitmap:
            self.gdi.DeleteObject(self.bitmap)
        else:
            self.old = previous
        self.bitmap = bitmap
        self.bits = bits
        self.scale, self.width, self.height = scale, width, height
        self.cache.clear()

    def font(self, size, bold=False):
        key = (size, bold)
        if key not in self.fonts:
            folder = Path(os.environ.get('WINDIR', os.environ.get('SYSTEMROOT', '/Windows'))) / 'Fonts'
            file=folder/('msyhbd.ttc' if bold else 'msyh.ttc')
            if not file.is_file():file=FONT_ASSETS/('PetsCJK-Bold.ttf' if bold else 'PetsCJK-Regular.ttf')
            self.fonts[key] = ImageFont.truetype(str(file), size)
        return self.fonts[key]

    def compose(self, photo, y, title, detail, bubble):
        key = str(photo)
        if key not in self.cache:
            png = self.root.tk.call(key, 'data', '-format', 'png')
            sprite = clean_sprite(Image.open(BytesIO(png)))
            if self.scale != 1:
                sprite = sprite.resize((round(sprite.width * self.scale), round(sprite.height * self.scale)), Image.Resampling.LANCZOS)
            self.cache[key] = sprite
        scale = self.scale
        frame = Image.new('RGBA', (self.width, self.height))
        sprite = self.cache[key]
        frame.alpha_composite(sprite, (round(170 * scale) - sprite.width // 2, round(y * scale) - sprite.height // 2))
        draw = ImageDraw.Draw(frame)
        # Both text areas have fully transparent backgrounds.
        for text, cy, size, bold in ((title, 305, 16, True), (detail, 330, 12, False), (bubble, 32, 14, True)):
            if text:
                size = round(size * scale)
                while size > round(9 * scale) and draw.textlength(text, font=self.font(size, bold)) > 320 * scale:
                    size -= 1
                draw.text((170 * scale, cy * scale), text, font=self.font(size, bold), anchor='mm', fill='#543c30')
        self.last_frame = frame
        return frame

    def present(self, photo, y, title, detail, bubble):
        self.last_args = (photo, y, title, detail, bubble)
        frame = self.compose(photo, y, title, detail, bubble)
        if not self.root.winfo_viewable():
            return
        raw = premultiplied_bgra(frame)
        C.memmove(self.bits, raw, len(raw))
        position = W.POINT(self.root.winfo_x(), self.root.winfo_y())
        origin = W.POINT(0, 0)
        size = SIZE(self.width, self.height)
        blend = BLEND(0, 0, 255, 1)
        if not self.user.UpdateLayeredWindow(self.hwnd, self.screen, C.byref(position),
                C.byref(size), self.dc, C.byref(origin), 0, C.byref(blend), 2):
            raise C.WinError(C.get_last_error())

    def close(self):
        self.gdi.SelectObject(self.dc, self.old)
        self.gdi.DeleteObject(self.bitmap)
        self.gdi.DeleteDC(self.dc)
        self.user.ReleaseDC(None, self.screen)
