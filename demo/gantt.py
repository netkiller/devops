import calendar
import drawsvg as draw
from datetime import datetime


class Canvas:
    width = 1980
    height = 1080


class Item:
    height = 30


class Gantt:
    canvasWidth = 1980
    canvasHeight = 1080
    unitWidth = 30
    unitHeight = 30
    splitLine = 1
    starting = 100
    itemLine = 0
    itemHeight = 30
    itemWidth = 30
    barHeight = 20
    progressHeight = 15

    data = [
        {'title': '汉字', 'begin': '2023-03-01', 'end': '2023-03-05'},
        {'title': 'Java', 'begin': '2023-03-01', 'end': '2023-03-05'},
        {'title': 'PHP', 'begin': '2023-03-03', 'end': '2023-03-10'},
        {'title': 'Go', 'begin': '2023-03-10', 'end': '2023-03-20'},
        {'title': 'Python', 'begin': '2023-03-06', 'end': '2023-03-08'},
        {'title': 'Swift', 'begin': '2023-03-06', 'end': '2023-03-20', 'subitem': [
            {'title': 'LLVM', 'begin': '2023-03-01', 'end': '2023-03-05'},
            {'title': 'Clang', 'begin': '2023-03-03', 'end': '2023-03-10'},
        ]},

    ]

    def __init__(self) -> None:
        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)
        self.draw.append(draw.Rectangle(1, 1, self.canvasWidth,
                         self.canvasHeight, fill='#eeeeee'))

        left = draw.Line(0, 0, 1, self.canvasHeight, stroke='black')
        top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        right = draw.Line(self.canvasWidth, 0,
                          self.canvasWidth, self.canvasHeight, stroke='black')
        buttom = draw.Line(0, self.canvasHeight, self.canvasWidth,
                           self.canvasHeight,  stroke='black')
        self.draw.append(left)
        self.draw.append(top)
        self.draw.append(right)
        self.draw.append(buttom)

    def title(self, text):
        group = draw.Group(id='title', fill='none', stroke='none')
        group.append(draw.Line(1, 50, self.canvasWidth, 50, stroke='black'))
        group.append(draw.Text(text, 30, self.canvasWidth / 2,
                     25, center=True, text_anchor='middle'))
        self.draw.append(group)

    def background(self):
        left = self.starting
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
            x = left + self.unitWidth * (day-1) + offsetX

            if weekday == 6:
                self.draw.append(draw.Line(x + 30, top - 40,
                                 x + 30, self.canvasHeight, stroke='black'))

            r = draw.Rectangle(x, top, self.unitWidth,
                               self.canvasHeight, fill=color)
            r.append_title(str(day))
            self.draw.append(r)
            self.draw.append(
                draw.Text(str(day), 24, x, top + 24, fill='#555555'))

            if day:
                offsetX += self.splitLine
        line = draw.Line(1, top + 26, self.canvasWidth,
                         top + 26, stroke='grey')
        self.draw.append(line)

    def item(self, line, subitem=False):
        left = self.starting
        top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine
        print(top)

        begin = datetime.strptime(line['begin'], '%Y-%m-%d').day
        # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        end = (datetime.strptime(line['end'], '%Y-%m-%d').date() -
               datetime.strptime(line['begin'], '%Y-%m-%d').date()).days

        left += self.itemWidth * (begin - 1) + (1 * begin)
        # 日宽度 + 竖线宽度
        right = self.itemWidth * (end + 1) + (1 * end)

        group = draw.Group(id='item', fill='none', stroke='black')

        group.append(
            draw.Text(line['title'], 20, 5, top + 15, text_anchor='start'))
        if subitem:
            # print(begin,end)
            # print(left,top,right)
            offsetY = 6
            length = left + right
            group.append(draw.Lines(
                # 坐标
                left, top + offsetY,
                # 横线
                length, top + offsetY,
                # 竖线
                length, top + 24,
                # 斜线
                length - 10, top + 15,
                # 横线2
                left + 10, top+15,
                # # 斜线
                left, top + 24,
                # # 闭合竖线
                left, top + offsetY,
                fill='black', stroke='black'))
        else:

            day = 2
            # mask = draw.Mask()
            # 进度
            progress = draw.Rectangle(
                left, top + 5, 30 * day, self.progressHeight, fill='#ccffff')
            progress.append_title("50%")
            # mask.append(progress)

            # 工时
            r = draw.Rectangle(left, top +4, right,self.barHeight, fill='#ccccff')
            r.append_title(line['title'])
            group.append(r)
            group.append(progress)

        # 分割线
        group.append(draw.Lines(self.starting, top + self.itemHeight,
                                self.canvasWidth, top + self.itemHeight, stroke='grey'))

        self.draw.append(group)
        self.itemLine += 1

    def test(self):
        top = 10
        width = 100
        polygon = draw.Lines(15, top, width, top, width, 25, width - 8, 20, 15, top+5, width, top+5,
                             fill='red', stroke='black', close='true')
        star = draw.Lines(48, 16, 16, 96, 96, 48, 0, 48, 88, 96,
                          stroke='black', fill='red', close='true')
        print(draw.Text("Test", 20, 5, top + 15, text_anchor='start').get_svg_defs)
        # self.draw.append(lines)
        # top = 40
        # line = draw.Line(1, top, self.canvasWidth, top, stroke='black')
        # self.draw.append(line)
        # offsetX = 0
        # for w in range(1, 6):
        #     # w = 0
        #     x = self.unitWidth * 7 * (w-1) + offsetX
        #     r = draw.Rectangle(x, top, self.unitWidth * 7, top, fill='#44cccc')
        #     r.append_title(str(w))
        #     self.draw.append(r)
        #     if w:
        #         offsetX += 5

    def task(self):
        offsetY = 0
        for line in self.data:
            if 'subitem' in line:
                self.item(line, True)
                for item in line['subitem']:
                    self.item(item)
            else:
                self.item(line)
        #      = 30 * y
        #     for x in range(1, 30):
        #         # print(day)
        #         offsetX = 31 * x
        #         r = draw.Rectangle(offsetX, offsetY+150,
        #                            30, 30, fill='#bbbbbb')
        #         r.append_title("Our first rectangle")  # Add a tooltip
        #         self.draw.append(r)

    def main(self):

        self.title("Gantt Test")
        self.background()
        # self.days()
        self.task()
        self.test()
        self.draw.save_svg('example.svg')


gantt = Gantt()

gantt.main()


# # Draw an arbitrary path (a triangle in this case)
# p = draw.Path(stroke_width=2, stroke='lime', fill='black', fill_opacity=0.2)
# p.M(-10, -20)  # Start path at point (-10, -20)
# p.C(30, 10, 30, -50, 70, -20)  # Draw a curve to (70, -20)
# d.append(p)

# # Draw text
# d.append(draw.Text('Basic text', 8, -10, -35, fill='blue'))  # 8pt text at (-10, -35)
# d.append(draw.Text('Path text', 8, path=p, text_anchor='start', line_height=1))
# d.append(draw.Text(['Multi-line', 'text'], 8, path=p, text_anchor='end', center=True))

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
