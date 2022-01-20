class WledChart:
    def __init__(self, api, segment_id, x, y):
        self.api = api
        self.prev_rows = {}
        self.segment_id = segment_id
        self.x = x
        self.y = y

    def clear(self):
        self.update_leds(1, [0, 0, 0])


    def update_leds(self, percent, color):
        color_empty = [0, 0, 0]
        rows = []
        for i in range(0, self.y):
            start = i * self.x
            stop = (start + round(self.x * percent) - 1)

            start, stop = tuple(sorted([start, stop]))

            if i in self.prev_rows:
                prev_start, prev_stop = tuple(self.prev_rows[i])
            else:
                prev_start, prev_stop = (0, 0)
            if stop < prev_stop:
                black_stop = prev_stop  # or last
                black_start = stop + 1
                rows.append([black_start, black_stop, color_empty])
            else:
                rows.append([start, stop, color])
            self.prev_rows[i] = (start, stop)

        wled_rows = []
        for i in range(0, self.y):
            start, stop, color = tuple(rows[i])
            diff = abs(stop - start)
            if (i % 2) == 0:
                start = start
                stop = stop + 1  # wled api
            else:  # led matrix zig-zag
                trans = start - self.x * i
                start = self.x * (i + 1) - trans
                stop = start - diff - 1  # wled api
            start, stop = tuple(sorted([start, stop]))
            wled_rows.append(start)
            wled_rows.append(stop)
            wled_rows.append(color)

        self.api.set_state({
            'seg': [{"id": self.segment_id, "i": wled_rows}]
        })
