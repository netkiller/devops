#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-09
##############################################
try:
    from optparse import OptionParser, OptionGroup
    import calendar
    import cv2
    import drawsvg as draw
    from datetime import datetime
except ImportError as err:
    print("Error: %s" % (err))


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
    textSize = 30
    textIndent = 0

    data = []

    def __init__(self) -> None:

        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)
        self.draw.append(draw.Rectangle(1, 1, self.canvasWidth - 1,
                         self.canvasHeight-1, fill='#eeeeee', stroke='black'))

    def title(self, text):
        group = draw.Group(id='title')  # fill='none', stroke='none'
        group.append(draw.Line(1, 50, self.canvasWidth, 50, stroke='black'))
        group.append(draw.Text(text, 30, self.canvasWidth / 2,
                     25, center=True, text_anchor='middle'))
        self.draw.append(group)

    def background(self):

        left = self.starting
        top = 80
        offsetX = 0
        background = draw.Group(id='background')

        group = draw.Group(id='table')
        group.append_title('表格')
        group.append(draw.Line(1, 80, self.canvasWidth,
                            80,  stroke='black'))
        group.append(draw.Text('任务', 20, 5, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize, top - 30,
                               self.textSize, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('开始日期', 20, self.textSize,
                     top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 100, top - 30,self.textSize + 100, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('截止日期', 20, self.textSize +
                     100, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 200, top - 30,self.textSize + 200, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('工时', 20, self.textSize +
                     200, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 250, top - 30,self.textSize + 250, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('资源', 20, self.textSize +
                     250, top + 20, fill='#555555'))
        background.append(group)

        
        # calendarGroup = draw.Group(id='calendar')
        
        weekNumber = datetime.strptime('2023-03-01', '%Y-%m-%d').strftime('%W')
        weekGroup = {}
        weekGroup[weekNumber] = draw.Group(id='week'+str(weekNumber))

        for day in range(1, 31):
            # print(day)
            weekday = calendar.weekday(2023, 3, day)
            
            currentWeekNumber = datetime.strptime('2023-03-'+ str(day), '%Y-%m-%d').strftime('%W')
            # print(weekNumber, currentWeekNumber)
            if currentWeekNumber != weekNumber:
                weekNumber = currentWeekNumber
                weekGroup[weekNumber]  = draw.Group(id='week'+str(weekNumber))

            if weekday >= 5:
                color = '#dddddd'
            else:
                color = '#cccccc'
            x = left + self.unitWidth * (day-1) + offsetX

            if weekday == 6:
                weekGroup[weekNumber].append(draw.Line(x + 30, top - 30,
                                       x + 30, self.canvasHeight, stroke='black'))

            r = draw.Rectangle(x, top, self.unitWidth,
                               self.canvasHeight, fill=color)
            r.append_title(str(day))
            weekGroup[weekNumber].append(r)
            weekGroup[weekNumber].append(
                draw.Text(str(day), 24, x, top + 24, fill='#555555'))

            if day:
                offsetX += self.splitLine
        # print(weekGroup)
        for key, value in weekGroup.items():
            background.append(value)

        group.append(draw.Line(1, top + 26, self.canvasWidth,
                               top + 26, stroke='grey'))
        background.append(group)

        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        # buttom = 
        background.append(
            draw.Line(left, top-30, left, self.canvasHeight, stroke='grey'))
        # self.draw.append(top)
        # self.draw.append(right)
        self.draw.append(background)

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

        table = draw.Group(id='text')
        text = draw.Text(line['title'], 20, 5 + (self.textIndent * self.itemWidth), top + 20, text_anchor='start')
        # text.append(draw.TSpan(line['begin'], text_anchor='start'))
        # text.append(draw.TSpan(line['end'], text_anchor='start'))
        table.append(text)
        fontSize = self.getTextSize(line['title'])
        begin = draw.Text(line['begin'], 20, self.textSize,
                          top + 20, text_anchor='start')
        table.append(begin)
        end = draw.Text(line['end'], 20, self.textSize +
                        100, top + 20, text_anchor='start')
        table.append(end)
        if 'progress' in line:
            table.append(draw.Text(
                str(line['progress']), 20, self.textSize + 200, top + 20, text_anchor='start'))
        if 'resource' in line:
            table.append(draw.Text(
                str(line['resource']), 20, self.textSize + 250, top + 20, text_anchor='start'))
        self.draw.append(table)

        group = draw.Group(id='item', fill='none', stroke='black')
        # text = draw.Text(line['title'], 20, 5, top + 15, text_anchor='start')
        # group.append(text)

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
        group.append(draw.Lines(1, top + self.itemHeight,
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
                self.textIndent += 1
                for item in line['subitem']:
                    self.item(item)
                self.textIndent -= 1
            else:
                self.item(line)

    def getTextSize(self, text):

        # fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        # fontFace = cv2.FONT_HERSHEY_PLAIN
        fontScale = 0.55
        thickness = 2

        size = cv2.getTextSize(text, fontFace, fontScale, thickness)
        width, height = size[0]
        return width

    def load(self, data):
        self.data = data
    def rander(self):
        # 计算文字宽度
        for item in self.data:
            length = self.getTextSize(item['title'])
            if self.starting < length:
                self.starting = length
                self.textSize = length
                # print(item['title'], len(item['title']))
        # print(lenght)
        # 文本表格所占用的宽度
        self.starting += 320

        self.background()
        self.task()

    def save(self, filename = None):
        if filename :
        # d.set_pixel_scale(2)  # Set number of pixels per geometry unit
        # d.set_render_size(400, 200)  # Alternative to set_pixel_scale
            self.draw.save_svg(filename)
        # self.draw.save_png('example.png')
        # self.draw.rasterize()
