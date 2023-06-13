import data
import bytemanager


class Character:
    code: int
    which_texture: int
    x_offset: int
    y_offset: int
    x_size: int
    y_size: int
    invalid: bool

    def __init__(self, b: bytemanager.ByteManager, offset: int):
        if b.to_integer(offset + data.VERIFY_CODE, data.BYTE_SPACE) == 0x1:
            self.invalid = True
            return
        self.invalid = False
        self.code = b.to_integer(offset + data.CHAR_CODE_OFFSET, data.SHORT_SPACE)
        self.which_texture = b.to_integer(offset + data.CHAR_TEXT_OFFSET, data.SHORT_SPACE)
        self.x_offset = int(
            (b.to_integer(offset + data.CHAR_XPOS_OFFSET, data.SHORT_SPACE) + data.TOTAL_X_OFFSET) * data.MULTIPLIER)
        self.y_offset = int(
            (b.to_integer(offset + data.CHAR_YPOS_OFFSET, data.SHORT_SPACE) - data.TOTAL_Y_OFFSET) * data.MULTIPLIER)
        self.x_size = b.to_integer(offset + data.CHAR_SIZE_X, data.BYTE_SPACE) * data.MULTIPLIER
        self.y_size = b.to_integer(offset + data.CHAR_SIZE_Y, data.BYTE_SPACE) * data.MULTIPLIER


Characters = list[Character]
