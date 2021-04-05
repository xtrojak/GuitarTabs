from app.libs.constants import POSITION, SPACE


def handle_note(string, row, bar, note, maximum):
    pos_x = 225 * bar + (note + 1) * (225 / (maximum + 1)) + 25
    pos_y = row * POSITION + SPACE * (row + 1) + string * 10 - 5
    return pos_x, pos_y


def handle_depth(number):
    return 50 * (number - 1) + 60 * (number + 1)


class SizeException(Exception):
    pass
