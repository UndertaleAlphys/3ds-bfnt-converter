from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont

import bytemanager
import character
import data


class MainProcess:
    _b: bytemanager.ByteManager
    _c: character.Characters
    _i: list[Image]
    _d: list
    _nc: int
    _nt: int
    _ft: ImageFont
    _fc: tuple[int, int, int, int]

    def __init__(self):
        # Load data
        data.load()
        self._b = bytemanager.ByteManager()
        self._c = []
        self._i = []
        self._d = []
        self._nc = 0
        self._nt = 0
        self._fc = (0, 0, 0, 255)

    def load_font(self, in_path: str):
        self._b.from_file(in_path)
        self._nc = self._b.to_integer(data.NUM_CHARACTER, 2)
        for cnt in range(self._nc):
            offset = data.CHAR_OFFSET + cnt * data.CHAR_SPACE
            ch = character.Character(self._b, offset)
            if not ch.invalid:
                self._c.append(ch)

    def draw_font(self, out_path: str):
        out_path = out_path.strip()
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        self._nt = self._b.to_integer(data.NUM_TEXTURE, data.INT_SPACE)
        self._ft = ImageFont.truetype(data.FONT_NAME, data.FONT_SIZE * data.MULTIPLIER)

        for cnt in range(self._nt):
            self._i.append(Image.new('RGBA', (1024 * data.MULTIPLIER, 1024 * data.MULTIPLIER), (0, 0, 0, 0)))
            self._d.append(ImageDraw.Draw(self._i[cnt]))
        for c in self._c:
            self._d[c.which_texture].text(
                (c.x_offset, c.y_offset),
                chr(c.code), font=self._ft,
                fill=self._fc
            )
        for cnt in range(self._nt):
            self._i[cnt].save(out_path + r'/tex' + str(cnt) + r'.png')


def main():
    import data
    mp = MainProcess()
    mp.load_font(data.IN_FILE)
    mp.draw_font(data.OUT_DIR)


if __name__ == '__main__':
    main()
