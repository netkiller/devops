import calendar
import drawsvg as draw

from datetime import datetime

begin = '2023-02-01'
end = '2023-02-28'

print(datetime.strptime(end, '%Y-%m-%d'))

interval = datetime.strptime(end, '%Y-%m-%d').date() - \
    datetime.strptime(begin, '%Y-%m-%d').date()
print(interval.days)  # 181 days, 0:00:00


# 系统默认：星期一作为一周的第一天（即：0），星期日作为一周的最后一天（即：6）

# class Graph:


class Gantt:
    canvasWidth = 1980
    canvasHeight = 1080
    unitWidth = 30
    unitHeight = 30
    splitLine = 1

    def __init__(self) -> None:
        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)
        self.draw.append(draw.Rectangle(1, 1, self.canvasWidth,
                         self.canvasHeight, fill='#eeeeee'))

        # left = draw.Line(1, 1, 1, self.canvas_height, stroke='black')
        # top = draw.Line(1, 1, self.canvas_width, 1, stroke='black')
        # right = draw.Line(self.canvas_width, 1, 1,
        #                   self.canvas_height, stroke='black')
        # buttom = draw.Line(self.canvas_height, 1, 1,
        #                    self.canvas_width,  stroke='black')
        # self.draw.append(left)
        # self.draw.append(top)
        # self.draw.append(right)
        # self.draw.append(buttom)
    def month(self):
        line = draw.Line(1, 50, self.canvasWidth, 50, stroke='black')
        self.draw.append(line)

        self.draw.append(draw.Text('Middle', 30, self.canvasWidth /
                         2, 25, center=True, text_anchor='middle'))

    def week(self):
        top = 40
        line = draw.Line(1, top, self.canvasWidth, top, stroke='black')
        self.draw.append(line)
        offsetX = 0
        for w in range(1,6):
        # w = 0
            x = self.unitWidth * 7 * (w-1) + offsetX
            r = draw.Rectangle(x, top, self.unitWidth *7 , top, fill='#44cccc')
            r.append_title(str(w))  
            self.draw.append(r)
            if w :
                offsetX += 5

    def days(self):
        top = 80
        offsetX = 0
        for day in range(1, 31):
            # print(day)
            weekday = calendar.weekday(2023, 3, day)
            # print(weekday)
            if weekday >= 5:
                color = '#dddddd'
            else:
                color = '#cccccc'
            x = self.unitWidth * (day-1) + offsetX
            r = draw.Rectangle(x, top, self.unitWidth, self.canvasHeight, fill=color)
            r.append_title(str(day))
            self.draw.append(r)
            self.draw.append(draw.Text(str(day), 24, x, top + 24, fill='#555555'))

            if day :
                offsetX += self.splitLine
        line = draw.Line(1, top + 26, self.canvasWidth,top + 26, stroke='grey')
        self.draw.append(line)

    def task(self):
        for y in range(1, 10):
            offsetY = 30 * y
            for x in range(1, 30):
                # print(day)
                offsetX = 31 * x
                r = draw.Rectangle(offsetX, offsetY+150,
                                   30, 30, fill='#bbbbbb')
                r.append_title("Our first rectangle")  # Add a tooltip
                self.draw.append(r)

        # r = draw.Rectangle(5, 5, 40, 50, fill='#cccccc')
        # r.append_title("Our first rectangle")  # Add a tooltip
        # self.draw.append(r)

    def main(self):

        self.month()
        self.week()
        self.days()
        # self.task()
        self.draw.save_svg('example.svg')


gantt = Gantt()

gantt.main()

# Draw an irregular polygon
# d.append(draw.Lines(-80, 45,
#                      70, 49,
#                      95, -49,
#                     -90, -40,
#                     close=False,
#             fill='#eeee00',
#             stroke='black'))

# Draw a rectangle


# # Draw a circle
# d.append(draw.Circle(-40, 10, 30,
#         fill='red', stroke_width=2, stroke='black'))

# # Draw an arbitrary path (a triangle in this case)
# p = draw.Path(stroke_width=2, stroke='lime', fill='black', fill_opacity=0.2)
# p.M(-10, -20)  # Start path at point (-10, -20)
# p.C(30, 10, 30, -50, 70, -20)  # Draw a curve to (70, -20)
# d.append(p)

# # Draw text
# d.append(draw.Text('Basic text', 8, -10, -35, fill='blue'))  # 8pt text at (-10, -35)
# d.append(draw.Text('Path text', 8, path=p, text_anchor='start', line_height=1))
# d.append(draw.Text(['Multi-line', 'text'], 8, path=p, text_anchor='end', center=True))

# # Draw multiple circular arcs
# d.append(draw.ArcLine(60, 20, 20, 60, 270,
#         stroke='red', stroke_width=5, fill='red', fill_opacity=0.2))
# d.append(draw.Arc(60, 20, 20, 90, -60, cw=True,
#         stroke='green', stroke_width=3, fill='none'))
# d.append(draw.Arc(60, 20, 20, -60, 90, cw=False,
#         stroke='blue', stroke_width=1, fill='black', fill_opacity=0.3))

# # Draw arrows
# arrow = draw.Marker(-0.1, -0.51, 0.9, 0.5, scale=4, orient='auto')
# arrow.append(draw.Lines(-0.1, 0.5, -0.1, -0.5, 0.9, 0, fill='red', close=True))
# p = draw.Path(stroke='red', stroke_width=2, fill='none',
#         marker_end=arrow)  # Add an arrow to the end of a path
# p.M(20, 40).L(20, 27).L(0, 20)  # Chain multiple path commands
# d.append(p)


# d.set_pixel_scale(2)  # Set number of pixels per geometry unit
# d.set_render_size(400, 200)  # Alternative to set_pixel_scale

# d.save_png('example.png')

# Display in Jupyter notebook
# d.rasterize()  # Display as PNG
# d  # Display as SVG
