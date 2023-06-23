from typing import Any, Optional

NUM_CHARACTER: int
CHAR_OFFSET: int
CHAR_SPACE: int
BYTE_SPACE: int
SHORT_SPACE: int
INT_SPACE: int
CHAR_CODE_OFFSET: int
CHAR_TEXT_OFFSET: int
CHAR_XPOS_OFFSET: int
CHAR_YPOS_OFFSET: int
CHAR_SIZE_X: int
CHAR_SIZE_Y: int
VERIFY_CODE_OFFSET: int
VERIFY_OFFSET: int
VERIFY_CODE: int
NUM_TEXTURE: int
TEXTURE_SIZE: int
TEXT_OFFSET: int
MULTIPLIER: int
FONT_NAME: str
FONT_SIZE: int
TOTAL_X_OFFSET: float
TOTAL_Y_OFFSET: float
X_CENTERED: bool
Y_CENTERED: bool
STROKE_WIDTH: Optional[int]
IN_DIR: str
OUT_DIR: str
TEST: bool
NO_OUTPUT: bool
LOG: bool


def assign_value(k: str, v: Any) -> None:
    global NUM_CHARACTER
    global CHAR_OFFSET
    global CHAR_SPACE
    global BYTE_SPACE
    global SHORT_SPACE
    global INT_SPACE
    global CHAR_CODE_OFFSET
    global CHAR_TEXT_OFFSET
    global CHAR_XPOS_OFFSET
    global CHAR_YPOS_OFFSET
    global CHAR_SIZE_X
    global CHAR_SIZE_Y
    global VERIFY_CODE_OFFSET
    global VERIFY_OFFSET
    global VERIFY_CODE
    global NUM_TEXTURE
    global TEXTURE_SIZE
    global TEXT_OFFSET
    global MULTIPLIER
    global FONT_NAME
    global FONT_SIZE
    global TOTAL_X_OFFSET
    global TOTAL_Y_OFFSET
    global X_CENTERED
    global Y_CENTERED
    global STROKE_WIDTH
    global IN_DIR
    global OUT_DIR
    global TEST
    global NO_OUTPUT
    global LOG
    k = k.upper()
    if k == 'NUM_CHARACTER':
        NUM_CHARACTER = v
    elif k == 'CHAR_OFFSET':
        CHAR_OFFSET = v
    elif k == 'CHAR_SPACE':
        CHAR_SPACE = v
    elif k == 'BYTE_SPACE':
        BYTE_SPACE = v
    elif k == 'SHORT_SPACE':
        SHORT_SPACE = v
    elif k == 'INT_SPACE':
        INT_SPACE = v
    elif k == 'CHAR_CODE_OFFSET':
        CHAR_CODE_OFFSET = v
    elif k == 'CHAR_TEXT_OFFSET':
        CHAR_TEXT_OFFSET = v
    elif k == 'CHAR_XPOS_OFFSET':
        CHAR_XPOS_OFFSET = v
    elif k == 'CHAR_YPOS_OFFSET':
        CHAR_YPOS_OFFSET = v
    elif k == 'CHAR_SIZE_X':
        CHAR_SIZE_X = v
    elif k == 'CHAR_SIZE_Y':
        CHAR_SIZE_Y = v
    elif k == 'VERIFY_CODE_OFFSET':
        VERIFY_CODE_OFFSET = v
    elif k == 'VERIFY_OFFSET':
        VERIFY_OFFSET = v
    elif k == 'VERIFY_CODE':
        VERIFY_CODE = v
    elif k == 'NUM_TEXTURE':
        NUM_TEXTURE = v
    elif k == 'TEXTURE_SIZE':
        TEXTURE_SIZE = v
    elif k == 'TEXT_OFFSET':
        TEXT_OFFSET = v
    elif k == 'MULTIPLIER':
        MULTIPLIER = v
    elif k == 'FONT_NAME':
        FONT_NAME = v
    elif k == 'FONT_SIZE':
        FONT_SIZE = v
    elif k == 'TOTAL_X_OFFSET':
        TOTAL_X_OFFSET = v
    elif k == 'TOTAL_Y_OFFSET':
        TOTAL_Y_OFFSET = v
    elif k == 'X_CENTERED':
        X_CENTERED = v
    elif k == 'Y_CENTERED':
        Y_CENTERED = v
    elif k == 'STROKE_WIDTH':
        STROKE_WIDTH = v
    elif k == 'IN_DIR':
        IN_DIR = v
    elif k == 'OUT_DIR':
        OUT_DIR = v
    elif k == 'TEST':
        TEST = v
    elif k == 'NO_OUTPUT':
        NO_OUTPUT = v
    elif k == 'LOG':
        LOG = v


def load(file_path: str = 'data.txt') -> None:
    def remove_space(ln: str) -> str:
        buf = ln.split()
        ln = ''
        for bf in buf:
            ln += bf
        return ln

    def my_cnt(ln: str, ch: str) -> int:
        if ln.count('\"') not in (0, 2) or ln.count('\'') not in (0, 2) or ln.count('\"') + ln.count(
                '\'') not in (0, 2):
            raise RuntimeError('data.txt is corrupted')
        if '\'' in ln:
            l__ = ln.index('\'')
            r__ = ln.rindex('\'')
            my_ln = ln[:l__] + ln[r__ + 1:]
        elif '\"' in ln:
            l__ = ln.index('\"')
            r__ = ln.rindex('\"')
            my_ln = ln[:l__] + ln[r__ + 1:]
        else:
            my_ln = ln
        return my_ln.count(ch)

    with open(file_path, 'r', encoding='UTF-8') as f:
        s = f.read().split('\n')
        for line in s:
            if '#' in line:
                sharp_index = line.index('#')
                line = line[:sharp_index]
            if not remove_space(line):
                continue
            if my_cnt(line, ':') + my_cnt(line, '=') not in (1, 2):
                raise RuntimeError('data.txt is corrupted')
            if my_cnt(line, ':') + my_cnt(line, '=') == 1:
                line = remove_space(line)
                if ':' in line:
                    split_index = line.index(':')
                else:
                    split_index = line.index('=')
                k = line[:split_index]
                v = int(line[split_index + 1:], 16)
            else:
                if my_cnt(line, ':') != 1 or my_cnt(line, '=') != 1 or line.index('=') < line.index(':'):
                    raise RuntimeError('data.txt is corrupted')
                l_ = line.index(':')
                r_ = line.index('=')
                k = remove_space(line[:l_])
                t = remove_space(line[l_ + 1:r_])
                v = line[r_ + 1:].strip()
                if '\'' in v or '\"' in v:
                    if str(v[0]) + str(v[-1]) not in ('\'\'', '\"\"') or v.count('\'') + v.count(
                            '\"') != 2 or t != 'str':
                        raise RuntimeError('data.txt is corrupted')
                    else:
                        v = v[1:-1]
                if t == 'str':
                    pass
                elif t == 'int':
                    v = int(v, 16)
                elif t == 'float':
                    v = float(v)
                elif t == 'bool':
                    v = True if v in ('True', '1') else False
                elif t == 'Optional[int]':
                    v = None if v == 'None' else int(v)
                else:
                    raise RuntimeError('data.txt is corrupted')
            assign_value(k, v)
