import svgwrite

from .constants import SIZE_X, POSITION, SPACE
from .utils import handle_depth, handle_note


class Image:
    def __init__(self, depth, path):
        self.size_x = SIZE_X
        self.size_y = handle_depth(depth)
        self.picture = svgwrite.Drawing(filename=path, size=(self.size_x, self.size_y), debug=True)
        self.picture.add(self.picture.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='white'))

        self.paint_tab_lines(depth)

    # basic functionality

    def paint_line(self, from_x, from_y, to_x, to_y, color):
        self.picture.add(self.picture.line((from_x, from_y), (to_x, to_y), stroke=color))

    def paint_text(self, pos_x, pos_y, text, color):
        self.picture.add(self.picture.text(text, insert=(pos_x, pos_y), fill=color,
                                           style="font-size:13px; font-family:Arial"))

    def save_image(self):
        self.picture.save()

    # advanced functionality

    def paint_vertical_line(self, size, i):
        self.paint_line(50 + (i + 1) * 80, 50, 50 + (i + 1) * 80, size, "black")

    def paint_horizontal_line(self, i):
        self.paint_line(50, 50 + (i + 1) * 50, 1010, 50 + (i + 1) * 50, "black")

    def paint_tone(self, i, j, tone):
        self.paint_text(85 + i * 80, 30 + (j + 1) * 50, tone, "red")

    def write_bar_number(self, i):
        self.paint_text(80 + i * 80, 30, str(i + 1), "black")

    def write_base_tone(self, i, tone, color):
        self.paint_text(30, 80 + i * 50, tone, color)

    def write_text_under_picture(self, i, tones):
        self.paint_text(50, i, "tones: " + ", ".join(sorted(set(tones))), "black")

    def paint_start_boundary(self, from_x, to_x, y):
        self.paint_line(from_x + 22, y, to_x, y, 'rgb(170,170,170)')
        self.paint_line(from_x + 22, y - 5, from_x + 22, y + 5, 'rgb(170,170,170)')

    def paint_end_boundary(self, from_x, to_x, y):
        self.paint_line(from_x, y, to_x - 22, y, 'rgb(170,170,170)')
        self.paint_line(to_x - 22, y - 5, to_x - 22, y + 5, 'rgb(170,170,170)')

    def paint_middle_boundary(self, from_x, to_x, y):
        self.paint_line(from_x, y, to_x, y, 'rgb(170,170,170)')

    # main functionality

    def paint_tab_lines(self, num):
        for position in range(num):
            space = SPACE * (position + 1)
            position *= POSITION
            for step in range(0, POSITION, 10):
                self.paint_line(25, step + position + space, 925, step + position + space, 'rgb(170,170,170)')

            for step in range(25, 1150, 225):
                self.paint_line(step, position + space, step, position + space + SPACE, 'rgb(170,170,170)')

    def write_title(self, title):
        pos_x = 475 - len(title) * 3
        pos_y = 20
        self.paint_text(pos_x, pos_y, title, "black")

    def draw_bar_numbers(self, number_of_bars):
        number = 1
        for i in range(number_of_bars):
            for step in range(30, 930, 225):
                pos_x = step
                pos_y = POSITION * (i + 1) + SPACE * i - 15
                self.paint_text(pos_x, pos_y, number, 'rgb(170,170,170)')
                number += 1

    def paint_tabs(self, data):
        for row in range(len(data)):
            for bar in range(len(data[row])):  # max is 4
                for note in range(len(data[row][bar])):  # max is 10
                    for (number, string) in data[row][bar][note]:
                        if number is not None and string is not None:
                            pos_x, pos_y = handle_note(string, row, bar, note, len(data[row][bar]))
                            self.paint_text(pos_x, pos_y, number, "black")

    def draw_comments(self, boundaries, texts):
        """
        Boundaries hints:
        0: none
        1: start
        2: end
        3: middle
        """
        i = 0
        step = 50
        while i < len(texts):
            pos_x = step
            pos_y = POSITION * ((i // 4) + 1) + SPACE * (i // 4) - 33
            if texts[i]:
                self.paint_text(pos_x, pos_y, texts[i][:33], 'rgb(170,170,170)')
            step = (step + 225) % 900
            i += 1

        i = 0
        step = 25
        while i < len(boundaries):
            if boundaries[i] != 0:
                from_x = step
                to_x = step + 225
                y = POSITION * ((i // 4) + 1) + SPACE * (i // 4) - 30
                if boundaries[i] == 1:
                    self.paint_start_boundary(from_x, to_x, y)
                elif boundaries[i] == 2:
                    self.paint_end_boundary(from_x, to_x, y)
                elif boundaries[i] == 3:
                    self.paint_middle_boundary(from_x, to_x, y)
            step = (step + 225) % 900
            i += 1


def draw_picture(data, title, bar_numbers, path):
    image = Image(data.depth, path)
    if bar_numbers:
        image.draw_bar_numbers(data.depth)
    image.paint_tabs(data.bars)
    image.write_title(title)
    image.draw_comments(data.boundaries, data.texts)
    image.save_image()
    return True
