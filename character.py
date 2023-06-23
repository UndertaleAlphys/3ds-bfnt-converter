import data
import bytemanager


class Character:
    code: int
    which_texture: int
    x_offset: int
    y_offset: int
    invalid: bool

    def __init__(self, b: bytemanager.ByteManager, offset: int):
        self.invalid = False

        self.x_size = b.to_integer(offset + data.CHAR_SIZE_X, data.BYTE_SPACE) * data.MULTIPLIER
        self.y_size = b.to_integer(offset + data.CHAR_SIZE_Y, data.BYTE_SPACE) * data.MULTIPLIER
        self.which_texture = b.to_integer(offset + data.CHAR_TEXT_OFFSET, data.SHORT_SPACE)
        self.x_offset = b.to_integer(offset + data.CHAR_XPOS_OFFSET, data.SHORT_SPACE) * data.MULTIPLIER
        self.y_offset = b.to_integer(offset + data.CHAR_YPOS_OFFSET, data.SHORT_SPACE) * data.MULTIPLIER
        self.code = b.to_integer(offset + data.CHAR_CODE_OFFSET, data.SHORT_SPACE)
        if data.VERIFY_CODE == b.to_integer(offset + data.VERIFY_OFFSET, data.SHORT_SPACE):
            self.invalid = True
        if data.LOG:
            f = open('log.txt', 'a')
            if self.invalid:
                s = ''
                s += f'{hex(self.code):<6} {self.which_texture} '
                for i in range(0x0, 0x10):
                    s += f'{b.to_integer(offset + i, data.BYTE_SPACE)} '
                s = s[:-1]
                s += '\n'
                f.write(s)
            f.close()


Characters = list[Character]
