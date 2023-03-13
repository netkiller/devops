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
    from datetime import datetime, date
    import time
except ImportError as err:
    print("Error: %s" % (err))


class Canvas:
    width = 1980
    height = 1080


class Data:
    data = {}

    def __init__(self) -> None:
        pass

    def add(self, id, name, start, finish, resource, parent):
        # duration
        item = {'id': id, 'name': name, 'begin': start,
                'end': finish, 'resource': resource}
        if int(parent) > 0:
            if not 'subitem' in self.data[parent]:
                self.data[parent]['subitem'] = {}
            self.data[parent]['subitem'][id] = item

        else:
            self.data[id] = item
        # print(self.data)

    def addDict(self, item):
        pass


class Gantt:
    canvasWidth = 1980
    canvasHeight = 1080
    unitWidth = 30
    unitHeight = 30
    splitLine = 1
    starting = 0
    itemLine = 0
    itemHeight = 30
    itemWidth = 30
    barHeight = 20
    progressHeight = 14
    textSize = 30
    textIndent = 0
    beginDate = datetime.now().date()
    endDate = datetime.now().date()
    weekdayPosition = 0
    dayPosition = {}
    linkPosition = {}

    data = {}

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

    def __table(self, top):
        group = draw.Group(id='table')
        group.append_title('表格')
        group.append(draw.Line(1, 80, self.canvasWidth,
                               80,  stroke='black'))
        group.append(draw.Text('任务', 20, 5, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize, top - 30,
                               self.textSize, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('开始日期', 20, self.textSize,
                               top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 100, top - 30,
                               self.textSize + 100, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('截止日期', 20, self.textSize +
                               100, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 200, top - 30,
                               self.textSize + 200, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('工时', 20, self.textSize +
                               200, top + 20, fill='#555555'))
        group.append(draw.Line(self.textSize + 250, top - 30,
                               self.textSize + 250, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('资源', 20, self.textSize +
                               250, top + 20, fill='#555555'))

        return group

    # def __weekday(self, top):
    #     left = self.starting
    #     offsetX = 0

    #     weekNumber = datetime.strptime('2023-03-01', '%Y-%m-%d').strftime('%W')
    #     weekGroups = {}
    #     weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

    #     for day in range(1, 31):
    #         # print(day)
    #         weekday = calendar.weekday(2023, 3, day)

    #         currentWeekNumber = datetime.strptime(
    #             '2023-03-' + str(day), '%Y-%m-%d').strftime('%W')
    #         # print(weekNumber, currentWeekNumber)
    #         if currentWeekNumber != weekNumber:
    #             weekNumber = currentWeekNumber
    #             weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

    #         if weekday >= 5:
    #             color = '#dddddd'
    #         else:
    #             color = '#cccccc'
    #         x = left + self.unitWidth * (day-1) + offsetX

    #         if weekday == 6:
    #             weekGroups[weekNumber].append(draw.Line(x + 30, top - 30,
    #                                           x + 30, self.canvasHeight, stroke='black'))

    #         r = draw.Rectangle(x, top, self.unitWidth,
    #                            self.canvasHeight, fill=color)
    #         r.append_title(str(day))
    #         weekGroups[weekNumber].append(r)
    #         weekGroups[weekNumber].append(
    #             draw.Text(str(day), 24, x, top + 24, fill='#555555'))

    #         if day:
    #             offsetX += self.splitLine
    #     # print(weekGroups)
    #     return weekGroups

    def __weekdays(self, top, month):
        offsetX = 1
        column = 0

        if month == self.beginDate.month:
            beginDay = self.beginDate.day
            endDay = calendar.monthrange(
                self.beginDate.year, self.beginDate.month)[1]
        elif month == self.endDate.month:
            beginDay = 1
            endDay = self.endDate.day
        else:
            beginDay = 1
            endDay = calendar.monthrange(datetime.now().year, month)[1]
        # print(beginDay, endDay)

        weekNumber = datetime.strptime(str(
            datetime.now().year)+'-'+str(month)+'-01', '%Y-%m-%d').strftime('%W')
        # weekNumber = datetime.date(datetime.now().year,month,1).strftime('%W')
        weekGroups = {}
        weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

        for day in range(beginDay, endDay+1):
            # print(day)
            weekday = calendar.weekday(datetime.now().year, month, day)

            currentWeekNumber = datetime.strptime(str(datetime.now().year) +
                                                  '-'+str(month)+'-' + str(day), '%Y-%m-%d').strftime('%W')
            # print(weekNumber, currentWeekNumber)
            if currentWeekNumber != weekNumber:
                weekNumber = currentWeekNumber
                weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

            if weekday >= 5:
                color = '#dddddd'
            else:
                color = '#cccccc'

            x = self.weekdayPosition + self.unitWidth * (column) + offsetX
            self.dayPosition[date(year=int(datetime.now().year), month=int(
                month), day=int(day)).strftime('%Y-%m-%d')] = x
            if weekday == 6:
                weekGroups[weekNumber].append(draw.Line(x + self.unitWidth, top - self.unitHeight,
                                                        x + self.unitWidth, self.canvasHeight, stroke='black'))

            r = draw.Rectangle(x, top, self.unitWidth,
                               self.canvasHeight, fill=color)
            r.append_title(str(day))
            weekGroups[weekNumber].append(r)

            # dayName = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
            dayName = ["一", "二", "三", "四", "五", "六", "日"]

            weekGroups[weekNumber].append(
                draw.Text(dayName[weekday], 20, x + 4, top - 10, fill='#555555'))
            if day < 10:
                numberOffsetX = 10
            else:
                numberOffsetX = 0
            weekGroups[weekNumber].append(
                draw.Text(str(day), 20, x + numberOffsetX, top + 20, fill='#555555'))

            # if column:
            offsetX += self.splitLine
            column += 1

        self.weekdayPosition = x + self.unitWidth

        return weekGroups

    def __month(self, top):
        self.weekdayPosition = self.starting
        monthGroups = {}
        for month in range(self.beginDate.month, self.endDate.month+1):
            monthGroups[month] = draw.Group(id='month'+str(month))
            for key, value in self.__weekdays(top, month).items():
                monthGroups[month].append(value)
        return monthGroups

    def background(self):

        left = self.starting
        top = 80

        background = draw.Group(id='background')

        background.append(self.__table(top))

        for key, value in self.__month(top).items():
            background.append(value)

        # print(self.dayPosition)

        # for key, value in self.__weekday(top).items():
        #     background.append(value)

        background.append(draw.Line(1, top + 26, self.canvasWidth,
                                    top + 26, stroke='grey'))

        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        background.append(
            draw.Line(left, top-30, left, self.canvasHeight, stroke='grey'))
        self.draw.append(background)

    # def item(self, line, subitem=False):
    #     left = self.starting
    #     top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine
    #     # print(top)

    #     begin = datetime.strptime(line['begin'], '%Y-%m-%d').day
    #     # end = datetime.strptime(line['end'], '%Y-%m-%d').day
    #     end = (datetime.strptime(line['end'], '%Y-%m-%d').date() -
    #            datetime.strptime(line['begin'], '%Y-%m-%d').date()).days

    #     left += self.itemWidth * (begin - 1) + (1 * begin)
    #     # 日宽度 + 竖线宽度
    #     right = self.itemWidth * (end + 1) + (1 * end)

    #     table = draw.Group(id='text')
    #     text = draw.Text(line['title'], 20, 5 + (self.textIndent *
    #                      self.itemWidth), top + 20, text_anchor='start')
    #     # text.append(draw.TSpan(line['begin'], text_anchor='start'))
    #     # text.append(draw.TSpan(line['end'], text_anchor='start'))
    #     table.append(text)
    #     fontSize = self.getTextSize(line['title'])
    #     begin = draw.Text(line['begin'], 20, self.textSize,
    #                       top + 20, text_anchor='start')
    #     table.append(begin)
    #     end = draw.Text(line['end'], 20, self.textSize +
    #                     100, top + 20, text_anchor='start')
    #     table.append(end)
    #     if 'progress' in line:
    #         table.append(draw.Text(
    #             str(line['progress']), 20, self.textSize + 200, top + 20, text_anchor='start'))
    #     if 'resource' in line:
    #         table.append(draw.Text(
    #             str(line['resource']), 20, self.textSize + 250, top + 20, text_anchor='start'))

    #     group = draw.Group(id='item', fill='none', stroke='black')
    #     # text = draw.Text(line['title'], 20, 5, top + 15, text_anchor='start')
    #     # group.append(text)
    #     group.append(table)
    #     if subitem:
    #         # print(begin,end)
    #         # print(left,top,right)
    #         offsetY = 6
    #         length = left + right
    #         group.append(draw.Lines(
    #             # 坐标
    #             left, top + offsetY,
    #             # 横线
    #             length, top + offsetY,
    #             # 竖线
    #             length, top + 24,
    #             # 斜线
    #             length - 10, top + 15,
    #             # 横线2
    #             left + 10, top+15,
    #             # # 斜线
    #             left, top + 24,
    #             # # 闭合竖线
    #             left, top + offsetY,
    #             fill='black', stroke='black'))
    #     else:

    #         # 工时
    #         r = draw.Rectangle(left, top + 4, right,
    #                            self.barHeight, fill='#ccccff')
    #         r.append_title(line['title'])
    #         group.append(r)

    #         # 进度
    #         if 'progress' in line:
    #             progress = draw.Rectangle(
    #                 left, top + 7, 30 * line['progress'], self.progressHeight, fill='#ccffff')
    #             progress.append_title(str(line['progress']))
    #             # mask.append(progress)
    #             group.append(progress)

    #     # 分割线
    #     group.append(draw.Lines(1, top + self.itemHeight,
    #                             self.canvasWidth, top + self.itemHeight, stroke='grey'))

    #     self.draw.append(group)
    #     self.itemLine += 1
    def items(self, line, subitem=False):
        left = self.starting
        top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine

        begin = datetime.strptime(line['begin'], '%Y-%m-%d').day
        # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        end = (datetime.strptime(line['end'], '%Y-%m-%d').date() -
               datetime.strptime(line['begin'], '%Y-%m-%d').date()).days

        # left += self.itemWidth * (begin - 1) + (1 * begin)
        # # 日宽度 + 竖线宽度
        right = self.itemWidth * (end + 1) + (1 * end)

        left = self.dayPosition[line['begin']]
        # right = self.dayPosition[line['end']]

        self.linkPosition[line['id']] = {'x': left, 'y':  top, 'width': right}

        lineGroup = draw.Group(id='line')
        table = draw.Group(id='text')
        text = draw.Text(line['name'], 20, 5 + (self.textIndent *
                                                self.itemWidth), top + 20, text_anchor='start')
        # text.append(draw.TSpan(line['begin'], text_anchor='start'))
        # text.append(draw.TSpan(line['end'], text_anchor='start'))
        table.append(text)
        fontSize = self.getTextSize(line['name'])
        table.append(draw.Text(line['begin'], 20, self.textSize,
                               top + 20, text_anchor='start'))
        table.append(draw.Text(line['end'], 20, self.textSize +
                               100, top + 20, text_anchor='start'))
        # if 'progress' in line:
        #     table.append(draw.Text(
        #         str(line['progress']), 20, self.textSize + 200, top + 20, text_anchor='start'))

        table.append(draw.Text(str(end), 20, self.textSize +
                     210, top + 20, text_anchor='start'))
        if 'resource' in line:
            table.append(draw.Text(
                str(line['resource']), 20, self.textSize + 250, top + 20, text_anchor='start'))
        lineGroup.append(table)
        group = draw.Group(id='item', fill='none', stroke='black')
        # text = draw.Text(line['name'], 20, 5, top + 15, text_anchor='start')
        # group.append(text)

        if subitem:
            # print(begin,end)
            # print(left,top,right)
            offsetY = 7
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

            # 工时
            r = draw.Rectangle(left, top + 4, right,
                               self.barHeight, fill='#ccccff')
            r.append_title(line['name'])
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

        lineGroup.append(group)
        self.draw.append(lineGroup)
        self.itemLine += 1

    def legend(self):
        top = 10
        self.draw.append(draw.Text("https://www.netkiller.cn - design by netkiller",
                                   15, self.canvasWidth - 300, top + 30, text_anchor='start', fill='grey'))
        # print(self.linkPosition)

    def task(self):
        offsetY = 0
        for id, line in self.data.items():
            if 'subitem' in line:
                self.items(line, True)
                self.textIndent += 1
                for id, item in line['subitem'].items():
                    self.items(item)
                self.textIndent -= 1
            else:
                self.items(line)

    def link(self, fromTask, toTask):
        # print(fromTask, toTask)
        linkGroup = draw.Group(id='link')
        x = fromTask['x']+fromTask['width'] + 1
        y = fromTask['y'] + 15
        arrow = draw.Marker(-0.1, -0.51, 0.9, 0.5, scale=4, orient='auto')
        arrow.append(draw.Lines(-0.1, 0.5, -0.1, -0.5,
                     0.9, 0, fill='red', close=True))
        path = draw.Path(stroke='red', stroke_width=2,
                         fill='none', marker_end=arrow)
        path.M(x, y).H(toTask['x']+15).V(toTask['y']-5)
        linkGroup.append(path)
        self.draw.append(linkGroup)

    def next(self):
        for id, line in self.data.items():
            if 'next' in line:
                self.link(self.linkPosition[line['id']],
                          self.linkPosition[line['next']])
            if 'subitem' in line:
                for id, item in line['subitem'].items():
                    if 'next' in item:
                        self.link(
                            self.linkPosition[item['id']], self.linkPosition[item['next']])

    def workload(self):
        self.starting = 400
        left = self.starting
        top = 80

        for key, value in self.data.items():
            self.fontSize = self.getTextSize(key)

        if self.beginDate > value['start']:
            self.beginDate = value['start']

        if self.endDate < value['finish']:
            self.endDate = value['finish']

        print(self.fontSize)

        chart = draw.Group(id='workload')

        table = draw.Group(id='table')
        table.append_title('表格')
        table.append(draw.Line(1, 80, self.canvasWidth,
                               80,  stroke='black'))
        table.append(draw.Text('资源', 20, 5, top + 20, fill='#555555'))
        table.append(draw.Line(self.textSize + 100, top - 30,
                     self.textSize + 100, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('开始日期', 20, self.textSize +
                     100, top + 20, fill='#555555'))
        table.append(draw.Line(self.textSize + 200, top - 30,
                     self.textSize + 200, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('截止日期', 20, self.textSize +
                     200, top + 20, fill='#555555'))
        table.append(draw.Line(self.textSize + 300, top - 30,
                     self.textSize + 300, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('工时', 20, self.textSize +
                               300, top + 20, fill='#555555'))
        table.append(draw.Line(self.textSize + 400, top - 30,
                               self.textSize + 400, self.canvasHeight, stroke='grey'))

        chart.append(table)

        for key, value in self.__month(top).items():
            chart.append(value)

        # print(self.dayPosition)

        # for key, value in self.__weekday(top).items():
        #     background.append(value)

        chart.append(draw.Line(1, top + 26, self.canvasWidth,
                               top + 26, stroke='grey'))

        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        chart.append(
            draw.Line(left, top-30, left, self.canvasHeight, stroke='grey'))

        # begin = datetime.strptime(line['begin'], '%Y-%m-%d').day
        # # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        #

        # left += self.itemWidth * (begin - 1) + (1 * begin)
        # # 日宽度 + 竖线宽度

        # left = self.dayPosition[line['begin']]

        for resource, row in self.data.items():
            #     print(resource, row)

            # # 工时
            top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine
            # end = (datetime.strptime(line['end'], '%Y-%m-%d').date() -               datetime.strptime(line['begin'], '%Y-%m-%d').date()).days
            end = (row['finish'] - row['start']).days
            right = self.itemWidth * (end + 1) + (1 * end)

            chart.append(draw.Text(resource, 20, 5 + (self.textIndent *
                         self.itemWidth), top + 20, text_anchor='start'))
            chart.append(draw.Text(row['start'].strftime('%Y-%m-%d'), 20, self.textSize + 100,
                                   top + 20, text_anchor='start'))
            chart.append(draw.Text(row['finish'].strftime('%Y-%m-%d'), 20, self.textSize +
                                   200, top + 20, text_anchor='start'))

            chart.append(draw.Text(str(end), 20, self.textSize +
                                   300, top + 20, text_anchor='start'))

            r = draw.Rectangle(left, top + 4, right,
                               self.barHeight, fill='#aaaaaa')
            r.append_title(resource)
            chart.append(r)

            self.itemLine += 1

        self.draw.append(chart)

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

    def initialize(self, item):
        # print(item)
        # 计算文字宽度
        length = self.getTextSize(item['name'])
        # print(item['name'], length)
        # 文本表格所占用的宽度
        if self.textSize < length - 50:
            self.textSize = length - 50
            # print(item['name'], len(item['name']))

        begin = datetime.strptime(item['begin'], '%Y-%m-%d').date()
        if self.beginDate > begin:
            self.beginDate = begin

        end = datetime.strptime(item['end'], '%Y-%m-%d').date()
        if self.endDate < end:
            self.endDate = end
        # print(self.endDate)

    def ganttChart(self):

        for id, line in self.data.items():
            self.initialize(line)
            if 'subitem' in line:
                for id, item in line['subitem'].items():
                    self.initialize(item)

        self.starting = self.textSize + 310
     # print(self.starting, self.textSize)

        self.background()
        self.task()
        self.next()
        self.legend()

    def workloadChart(self):
        self.workload()

    def save(self, filename=None):
        if filename:
            # d.set_pixel_scale(2)  # Set number of pixels per geometry unit
            # d.set_render_size(400, 200)  # Alternative to set_pixel_scale
            self.draw.save_svg(filename)
        # self.draw.save_png('example.png')
        # self.draw.rasterize()
