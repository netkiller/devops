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
    progressHeight = 14

    data = [
        {'title': '汉字', 'begin': '2023-03-01', 'end': '2023-03-05', 'progress': 3},
        {'title': 'Java', 'begin': '2023-03-01',
            'end': '2023-03-05', 'progress': 2},
        {'title': 'PHP', 'begin': '2023-03-03',
            'end': '2023-03-10', 'progress': 5},
        {'title': 'Go', 'begin': '2023-03-10', 'end': '2023-03-20'},
        {'title': 'Python', 'begin': '2023-03-06', 'end': '2023-03-08'},
        {'title': 'Swift', 'begin': '2023-03-06', 'end': '2023-03-20', 'subitem': [
            {'title': 'LLVM', 'begin': '2023-03-01', 'end': '2023-03-05'},
            {'title': 'Clang', 'begin': '2023-03-03', 'end': '2023-03-10'},
        ]},

    ]

    def __init__(self) -> None:
        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)
        self.draw.append(draw.Rectangle(1, 1, self.canvasWidth - 1,
                         self.canvasHeight-1, fill='#eeeeee', stroke='black'))

        # left = draw.Line(0, 0, 1, self.canvasHeight, stroke='black')
        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        # buttom = draw.Line(0, self.canvasHeight, self.canvasWidth,
        #                    self.canvasHeight,  stroke='black')
        # self.draw.append(left)
        # self.draw.append(top)
        # self.draw.append(right)
        # self.draw.append(buttom)

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
        group = draw.Group(id='background')
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
                group.append(draw.Line(x + 30, top - 40,
                                       x + 30, self.canvasHeight, stroke='black'))

            r = draw.Rectangle(x, top, self.unitWidth,
                               self.canvasHeight, fill=color)
            r.append_title(str(day))
            group.append(r)
            group.append(
                draw.Text(str(day), 24, x, top + 24, fill='#555555'))

            if day:
                offsetX += self.splitLine
        group.append(draw.Line(1, top + 26, self.canvasWidth,
                               top + 26, stroke='grey'))

        self.draw.append(group)

    def item(self, line, subitem=False):
        left = self.starting
        top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine
        # print(top)

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

            # mask = draw.Mask()

            # 工时
            r = draw.Rectangle(left, top + 4, right,
                               self.barHeight, fill='#ccccff')
            r.append_title(line['title'])
            group.append(r)

            # 进度
            if 'progress' in line:
                progress = draw.Rectangle(
                    left, top + 7, 30 * line['progress'], self.progressHeight, fill='#ccffff')
                progress.append_title(str(line['progress']))
                # mask.append(progress)
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
        print(draw.Text("Test", 20, 5, top + 15, text_anchor='start'))
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

    def save(self):
        # d.set_pixel_scale(2)  # Set number of pixels per geometry unit
        # d.set_render_size(400, 200)  # Alternative to set_pixel_scale

        self.draw.save_svg('example.svg')
        # self.draw.save_png('example.png')
        # self.draw.rasterize()

    def main(self):

        self.title("Gantt Test")
        self.background()
        # self.days()
        self.task()
        self.save()


gantt = Gantt()
gantt.main()
