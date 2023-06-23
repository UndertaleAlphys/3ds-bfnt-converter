from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont

import bytemanager
import character
import data
import sys
import platform


class CharacterLoc:
    def __init__(self, x: int, y: int, sx: int, sy: int, multiplier: int = 1):
        self.x = x * multiplier
        self.y = y * multiplier
        self.sx = sx * multiplier
        self.sy = sy * multiplier
        self.x_ = (x + sx) * multiplier
        self.y_ = (y + sy) * multiplier

    def to_box(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.x_, self.y_

    @classmethod
    def from_box(cls, x_min: int, y_min: int, x_max: int, y_max: int, multiplier: int = 1) -> CharacterLoc:
        return cls(x_min, y_min, x_max - x_min, y_max - y_min, multiplier)

    @classmethod
    def from_tuple(cls, t: tuple[int, int, int, int], multiplier: int = 1) -> CharacterLoc:
        return cls(t[0], t[1], t[2], t[3], multiplier)

    @classmethod
    def from_box_tuple(cls, t: tuple[int, int, int, int], multiplier: int = 1):
        return cls.from_box(t[0], t[1], t[2], t[3], multiplier)

    def __mul__(self, other: int) -> CharacterLoc:
        return CharacterLoc(self.x, self.y, self.sx, self.sy, other)


class ParseFont:
    """
    Parse .bfnt File
    attributes:
    _b: byte manager
    _c: list of character
    _i: list of generated texture
    _d: to draw texture
    _nc: number of characters
    _nt: number of texture pngs
    _ts: size of per png
    _to: offset of the first texure
    _tx: list of read texture images
    _ft: dict of fonts, in different size
    _fc: font color
    """
    _b: bytemanager.ByteManager
    _c: character.Characters
    _i: list[Image]
    _d: list[ImageDraw]
    _nc: int
    _nt: int
    _ts: int
    _to: int
    _tx: list[Image]
    _ft: ImageFont
    _fc: tuple[int, int, int, int]

    def __init__(self):
        self._b = bytemanager.ByteManager()
        self._c = []
        self._i = []
        self._d = []
        self._nc = 0
        self._nt = 0
        self._ts = 0
        self._to = 0
        self._tx = []
        self._fc = (0, 0, 0, 255)
        self._ft = None

    def load_font(self, in_path: str):
        self._b.from_file(in_path)
        self._nc = self._b.to_integer(data.NUM_CHARACTER, data.SHORT_SPACE)
        self._ts = self._b.to_integer(data.TEXTURE_SIZE, data.INT_SPACE)
        self._nt = self._b.to_integer(data.NUM_TEXTURE, data.INT_SPACE)
        if data.LOG:
            f = open('LOG.txt', 'a')
            f.write('FILE ' + in_path + ' \n')
            f.close()
        for cnt in range(self._nc):
            offset = data.CHAR_OFFSET + cnt * data.CHAR_SPACE
            ch = character.Character(self._b, offset)
            if not ch.invalid:
                self._c.append(ch)

    def draw_font(self, in_path: str, out_path: str):
        self._ft = ImageFont.truetype(data.FONT_NAME, data.FONT_SIZE * data.MULTIPLIER)
        out_path = out_path.strip()
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        for cnt in range(self._nt):
            self._i.append(Image.new('RGBA', (1024 * data.MULTIPLIER, 1024 * data.MULTIPLIER), (0, 0, 0, 0)))
            self._d.append(ImageDraw.Draw(self._i[cnt]))

        for c in self._c:
            _, _, x_max, y_max = self._ft.getbbox(chr(c.code))
            img = Image.new('RGBA', (x_max, y_max),
                            (0, 0, 0, 0))
            drw = ImageDraw.Draw(img)
            if data.STROKE_WIDTH is None:
                drw.text((0, 0), chr(c.code), font=self._ft, fill=self._fc)
            else:
                drw.text((0, 0), chr(c.code), font=self._ft, fill=self._fc, stroke_width=data.STROKE_WIDTH)
            t = img.getbbox()
            if t is None:
                x_min, y_min, x_max, y_max = self._ft.getbbox(chr(c.code))
            else:
                x_min, y_min, x_max, y_max = t
            ascent, descent = self._ft.getmetrics()
            if data.X_CENTERED:
                final_x = c.x_offset + (c.x_size - x_max - x_min) // 2
            else:
                final_x = c.x_offset
            if data.Y_CENTERED:
                final_y = c.y_offset + (c.y_size - y_max - y_min) // 2
            else:
                final_y = c.y_offset + (c.y_size - ascent)
            _, _, _, a = img.split()
            self._i[c.which_texture].paste(
                img,
                (final_x,
                 final_y),
                mask=a
            )
            if data.TEST:
                self._d[c.which_texture].rectangle(
                    (c.x_offset, c.y_offset, c.x_offset + c.x_size, c.y_offset + c.y_size),
                    outline=(255, 0, 0, 128))
        for cnt in range(self._nt):
            suffix, _ = os.path.splitext(in_path)
            final_path = out_path + r'/tex' + suffix + str(cnt)
            while os.path.exists(final_path + r'.png'):
                print(f'\"{final_path}\" already exists')
                final_path += ' ' + str(2)
                print(f'try \"{final_path}\".png...')
            if not data.NO_OUTPUT:
                self._i[cnt].save(final_path + r'.png')
                print(f'{final_path}.png generated successfully.')
            else:
                print('NO_OUTPUT mode is enabled.', end=' ')
                print(final_path + r'.png not generated.')


def pause():
    import platform
    s = platform.system().lower()
    if s in ('darwin', 'linux'):
        pause_unix()
    elif s == 'windows':
        pause_windows()
    else:
        print('Enter any key to continue...')
        input()


def pause_windows():
    import os
    os.system('pause')


def pause_unix():
    import tty
    import termios
    print("Press any key to continue...")

    fd = sys.stdin.fileno()
    if not os.isatty(fd):
        fd = os.open("/dev/tty", os.O_RDWR)

    old = termios.tcgetattr(fd)

    tty.setraw(fd, termios.TCSADRAIN)
    os.read(fd, 1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    import data
    try:
        data.load()
    except RuntimeError:
        pause()
        exit(-1)
    print(platform.system())
    print('bfnt - >png 提取工具 alpha 0.1')
    print('')
    print('作者：火纹梅戚\tGithub:Undertale_Alphys')
    print('用法：')
    print('将.bfnt文件放入input文件夹')
    print('然后运行本工具')
    print('可以在data.txt中修改设置')
    for root, dirs, files in os.walk(data.IN_DIR):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext == r'.bfnt':
                mp = ParseFont()
                mp.load_font(root + '/' + file)
                mp.draw_font(file, data.OUT_DIR)
    print('完成')
    pause()


if __name__ == '__main__':
    main()
