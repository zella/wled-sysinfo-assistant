from dataclasses import dataclass


@dataclass
class Row:
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass
class LedRow:
    i1: int
    i2: int
    fill: bool


class WledChartV2:

    def __init__(self, api, segment_id, width_x, width_y, is_zigzag):
        self.api = api
        self.segment_id = segment_id
        self.width_x = width_x
        self.width_y = width_y
        self.old_rows = []
        self.is_zigzag = is_zigzag

    def __make_rows_from__(self, percent):
        rows = []
        for i in range(0, self.width_y):
            x2 = round(self.width_x * percent)
            y2 = i
            x1 = 0
            y1 = i
            rows.append(Row(x1, y1, x2, y2))
        print(rows)
        return rows

    @staticmethod
    def black_or_none(x_old, x_new):
        if x_old > x_new:
            x_start = x_new + 1
            x_end = x_old
            return x_start, x_end
        else:
            return None

    def to1d(self, x, y):
        if self.is_zigzag:
            return y * self.width_x + (self.width_x - x - 1)
        else:
            return y * self.width_x + x

    def compute_rows(self, percent):
        rows = self.__make_rows_from__(percent)
        led_rows = []
        for i, row in enumerate(rows):
            old_row = self.old_rows[i] if i < len(self.old_rows) else None
            fill = True
            x1 = row.x1
            x2 = row.x2
            if old_row:
                x1x2 = self.black_or_none(old_row.x2, row.x2)
                if x1x2:
                    fill = False
                    (x1, x2) = x1x2
            self.old_rows = rows
            led_rows.append(LedRow(
                self.to1d(x1, row.y1),
                self.to1d(x2, row.x2), fill)
            )
        return led_rows

    def update_leds(self, percent, color):
        color_empty = [0, 0, 0]
        logical_rows = self.compute_rows(percent)
        wled_rows = []
        for r in logical_rows:
            wled_rows.append(r.i1)
            wled_rows.append(r.i2)
            wled_rows.append(color if r.fill else color_empty)
        self.api.set_state({
            'seg': [{"id": self.segment_id, "i": wled_rows}]
        })

    def clear(self):
        self.update_leds(1, [0, 0, 0])
