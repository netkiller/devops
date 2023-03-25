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
    from distutils import util
except ImportError as err:
    print("Error: %s" % (err))


class Canvas:
    width = 1980
    height = 1080


class Data:
    data = {}

    def __init__(self) -> None:
        pass

    def add(self, id, name, start, finish, resource, next, milestone, parent):
        # duration
        item = {'id': id, 'name': name, 'start': start,
                'finish': finish, 'resource': resource, 'next': next, 'milestone': milestone}

        if parent != '' and int(parent) > 0:
            # print(parent)
            if not 'subitem' in self.data[parent]:
                self.data[parent]['subitem'] = {}
            self.data[parent]['subitem'][id] = item

        else:
            self.data[id] = item

    def addDict(self, item):
        pass


class Gantt:
    draw = None
    canvasWidth = 1980
    canvasHeight = 1080
    unitWidth = 30
    unitHeight = 30
    splitLine = 1
    canvasTop = 0
    canvasLeft = 0
    startPosition = 0
    itemLine = 0
    itemHeight = 30
    itemWidth = 30
    barHeight = 20
    progressHeight = 14
    nameTextSize = 1
    resourceTextSize = 90
    textIndent = 0
    textIndentSize = 0
    beginDate = datetime.now().date()
    endDate = datetime.now().date()
    weekdayPosition = 0
    dayPosition = {}
    linkPosition = {}
    # 隐藏表格
    isTable = False

    data = {}

    def __init__(self) -> None:
        pass

    def title(self, text):
        if not self.isTable:
            group = draw.Group(id='title', onclick="this.style.stroke = 'green'; ")  # fill='none', stroke='none'
            group.append(draw.Text(text, 30, self.canvasWidth / 2,
                                   25, center=True, text_anchor='middle'))
            self.draw.append(group)

    def __table(self, top):
        group = draw.Group(id='table')
        group.append_title('表格')
        # group.append(draw.Line(1, 80, self.canvasWidth,                               80,  stroke='black'))
        group.append(draw.Text('任务', 20, 5, top + 20 +
                     self.unitHeight * 2, fill='#555555'))
        group.append(draw.Line(self.nameTextSize, top + self.unitHeight * 2,
                               self.nameTextSize, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('开始日期', 20, self.nameTextSize,
                               top + 20 + self.unitHeight * 2, fill='#555555'))
        group.append(draw.Line(self.nameTextSize + 100, top + self.unitHeight * 2,
                               self.nameTextSize + 100, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('截止日期', 20, self.nameTextSize +
                               100, top + 20 + self.unitHeight * 2, fill='#555555'))
        group.append(draw.Line(self.nameTextSize + 200, top+self.unitHeight * 2,
                               self.nameTextSize + 200, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('工时', 20, self.nameTextSize +
                               200, top + 20 + self.unitHeight * 2, fill='#555555'))
        group.append(draw.Line(self.nameTextSize + 250, top+self.unitHeight * 2,
                               self.nameTextSize + 250, self.canvasHeight, stroke='grey'))
        group.append(draw.Text('资源', 20, self.nameTextSize +
                               250, top + 20 + self.unitHeight * 2, fill='#555555'))

        return group

    # def __weekdays(self, top, month):
    #     offsetX = 1
    #     column = 0

    #     if month == self.beginDate.month:
    #         beginDay = self.beginDate.day
    #         endDay = calendar.monthrange(
    #             self.beginDate.year, self.beginDate.month)[1]
    #     elif month == self.endDate.month:
    #         beginDay = 1
    #         endDay = self.endDate.day
    #     else:
    #         beginDay = 1
    #         endDay = calendar.monthrange(datetime.now().year, month)[1]
    #     # print(beginDay, endDay)

    #     weekNumber = datetime.strptime(str(
    #         datetime.now().year)+'-'+str(month)+'-01', '%Y-%m-%d').strftime('%W')
    #     # weekNumber = datetime.date(datetime.now().year,month,1).strftime('%W')
    #     weekGroups = {}
    #     weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

    #     for day in range(beginDay, endDay+1):
    #         # print(day)
    #         weekday = calendar.weekday(datetime.now().year, month, day)

    #         currentWeekNumber = datetime.strptime(str(datetime.now().year) +
    #                                               '-'+str(month)+'-' + str(day), '%Y-%m-%d').strftime('%W')
    #         # print(weekNumber, currentWeekNumber)
    #         if currentWeekNumber != weekNumber:
    #             weekNumber = currentWeekNumber
    #             weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

    #         if weekday >= 5:
    #             color = '#dddddd'
    #         else:
    #             color = '#cccccc'

    #         x = self.weekdayPosition + self.unitWidth * (column) + offsetX
    #         self.dayPosition[date(year=int(datetime.now().year), month=int(
    #             month), day=int(day)).strftime('%Y-%m-%d')] = x
    #         if weekday == 6:
    #             weekGroups[weekNumber].append(draw.Line(x + self.unitWidth, top - self.unitHeight,
    #                                                     x + self.unitWidth, self.canvasHeight, stroke='black'))
    #         # 日栏位
    #         # print(self.weekdayPosition)
    #         r = draw.Rectangle(x, top+1, self.unitWidth,
    #                            self.canvasHeight - 80-2, fill=color)
    #         r.append_title(str(day))
    #         weekGroups[weekNumber].append(r)

    #         # dayName = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    #         dayName = ["一", "二", "三", "四", "五", "六", "日"]

    #         weekGroups[weekNumber].append(
    #             draw.Text(dayName[weekday], 20, x + 4, top - 10, fill='#555555'))
    #         if day < 10:
    #             numberOffsetX = 10
    #         else:
    #             numberOffsetX = 0
    #         weekGroups[weekNumber].append(
    #             draw.Text(str(day), 20, x + numberOffsetX, top + 20, fill='#555555'))

    #         # if column:
    #         offsetX += self.splitLine
    #         column += 1

    #     self.weekdayPosition = x + self.unitWidth

    #     return weekGroups
    def __weekdays(self, top, begin, end):
        offsetX = 1
        column = 0

        # if month == self.beginDate.month:
        #     beginDay = self.beginDate.day
        #     endDay = calendar.monthrange(
        #         self.beginDate.year, self.beginDate.month)[1]
        # elif month == self.endDate.month:
        #     beginDay = 1
        #     endDay = self.endDate.day
        # else:
        #     beginDay = 1
        #     endDay = calendar.monthrange(datetime.now().year, month)[1]

        begin = datetime.strptime(begin, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')

        beginDay = begin.day
        endDay = end.day
        # print(beginDay, endDay)

        weekNumber = datetime.strptime(
            str(begin.year)+'-'+str(begin.month)+'-01', '%Y-%m-%d').strftime('%W')
        # weekNumber = begin.strftime('%W')
        # weekNumber = datetime.date(datetime.now().year,month,1).strftime('%W')
        weekGroups = {}
        weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

        for day in range(beginDay, endDay+1):
            # print(day)
            weekday = calendar.weekday(begin.year, begin.month, day)

            currentWeekNumber = datetime.strptime(
                str(begin.year) + '-'+str(begin.month)+'-' + str(day), '%Y-%m-%d').strftime('%W')
            # print(weekNumber, currentWeekNumber)
            if currentWeekNumber != weekNumber:
                weekNumber = currentWeekNumber
                weekGroups[weekNumber] = draw.Group(id='week'+str(weekNumber))

            if weekday >= 5:
                color = '#dddddd'
            else:
                color = '#cccccc'

            x = self.weekdayPosition + self.unitWidth * (column) + offsetX
            self.dayPosition[date(year=int(begin.year), month=int(
                begin.month), day=int(day)).strftime('%Y-%m-%d')] = x
            if weekday == 6:
                weekGroups[weekNumber].append(draw.Line(x + self.unitWidth, top + self.unitHeight,
                                                        x + self.unitWidth, self.canvasHeight, stroke='black'))
            if day == beginDay:
                weekGroups[weekNumber].append(draw.Text(begin.strftime(
                    '%Y年%m月'), 20, x + 4, top + self.unitHeight - 10, fill='#555555'))
            if day == endDay:
                weekGroups[weekNumber].append(draw.Line(x + self.unitWidth, top,
                                                        x + self.unitWidth, self.canvasHeight, stroke='black'))

            # dayName = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
            dayName = ["一", "二", "三", "四", "五", "六", "日"]

            weekGroups[weekNumber].append(
                draw.Text(dayName[weekday], 20, x + 4, top + self.unitWidth*2-10, fill='#555555'))
            if day < 10:
                numberOffsetX = 10
            else:
                numberOffsetX = 0

            # 日栏位
            # print(self.weekdayPosition)
            r = draw.Rectangle(x, top+self.unitHeight*2, self.unitWidth,
                               self.canvasHeight - (top+self.unitHeight*2), fill=color)
            r.append_title(str(day))
            weekGroups[weekNumber].append(r)

            # 日期
            weekGroups[weekNumber].append(
                draw.Text(str(day), 20, x + numberOffsetX, top + self.unitWidth * 3 - 10, fill='#555555'))

            # if column:
            offsetX += self.splitLine
            column += 1

        self.weekdayPosition = x + self.unitWidth

        return weekGroups

    # def __month(self, top):
    #     self.weekdayPosition = self.startPosition
    #     monthGroups = {}
    #     for month in range(self.beginDate.month, self.endDate.month+1):
    #         monthGroups[month] = draw.Group(id='month'+str(month))
    #         for key, value in self.__weekdays(top, month).items():
    #             monthGroups[month].append(value)
    #     return monthGroups

    def __month(self, top, months):
        # self.weekdayPosition = self.startPosition
        monthGroups = {}
        for begin, end in months:
            month = datetime.strptime(begin, '%Y-%m-%d').month
            monthGroups[month] = draw.Group(id='month'+str(month))
            for key, value in self.__weekdays(top, begin, end).items():
                monthGroups[month].append(value)

        return monthGroups

    def __monthRange(self, begin, end):
        years = {}
        # result = []
        while True:
            if begin.month == 12:
                next = begin.replace(year=begin.year+1, month=1, day=1)
            else:
                next = begin.replace(month=begin.month+1, day=1)
            if next > end:
                break

            day = calendar.monthrange(begin.year, begin.month)[1]

            # result.append((begin.strftime("%Y-%m-%d"),
            #                begin.replace(day=day).strftime("%Y-%m-%d")))
            if not begin.year in years:
                years[begin.year] = []
            years[begin.year].append((begin.strftime("%Y-%m-%d"),
                                      begin.replace(day=day).strftime("%Y-%m-%d")))
            begin = next
        # result.append((begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

        if not end.year in years:
            years[end.year] = []
        years[end.year].append(
            (begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        # print(years)
        return years

    def __year(self, top):
        self.weekdayPosition = self.startPosition
        yearGroups = {}
        # print(self.beginDate, self.endDate)
        years = self.__monthRange(self.beginDate, self.endDate)

        # print(len(years))
        for year, month in years.items():
            # print(year, month)
            # begin = datetime.strptime(begin, "%Y-%m-%d").date()
            # end = datetime.strptime(end, "%Y-%m-%d").date()
            yearGroups[year] = draw.Group(id='year'+str(year))
            for key, value in self.__month(top, month).items():
                yearGroups[year].append(value)
        return yearGroups

    def calendar(self):

        left = self.startPosition
        top = self.canvasTop

        background = draw.Group(id='calendar')
        if not self.isTable:
            background.append(self.__table(top))

        for key, value in self.__year(top).items():
            background.append(value)
        # for key, value in self.__month(top).items():
        #     background.append(value)
        # 月线
        background.append(draw.Line(1, top + self.unitHeight, self.canvasWidth,
                                    top + self.unitHeight, stroke='grey'))

        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        # 周线
        background.append(draw.Line(1, top + self.unitHeight * 2,
                          self.canvasWidth, top + self.unitHeight * 2, stroke='grey'))
        # 日线
        background.append(draw.Line(1, top + self.unitHeight * 3,
                          self.canvasWidth, top + self.unitHeight * 3, stroke='grey'))
        # 上边封闭
        background.append(
            draw.Line(1, top, self.canvasWidth, top, stroke='grey'))
        # 左边封闭
        background.append(draw.Line(left, top + self.unitHeight,
                          left, self.canvasHeight, stroke='grey'))
        self.draw.append(background)

    def items(self, line, subitem=False):

        left = self.startPosition
        top = self.canvasTop + self.unitHeight * 3 + self.itemLine * \
            self.itemHeight + self.splitLine * self.itemLine

        begin = datetime.strptime(line['start'], '%Y-%m-%d').day
        # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        end = (datetime.strptime(line['finish'], '%Y-%m-%d').date() -
               datetime.strptime(line['start'], '%Y-%m-%d').date()).days

        # left += self.itemWidth * (begin - 1) + (1 * begin)
        # # 日宽度 + 竖线宽度
        right = self.itemWidth * (end + 1) + (1 * end)

        left = self.dayPosition[line['start']]
        # right = self.dayPosition[line['end']]

        self.linkPosition[line['id']] = {'x': left, 'y':  top, 'width': right}

        lineGroup = draw.Group(id='line')
        if not self.isTable:
            table = draw.Group(id='text')
            table.append(draw.Text(
                line['name'], 20, 5 + (self.textIndent * self.itemWidth), top + 20, text_anchor='start'))
            # text.append(draw.TSpan(line['begin'], text_anchor='start'))
            # text.append(draw.TSpan(line['end'], text_anchor='start'))
            # if not subitem:
            #     table.append(draw.Text(
            #         line['name'], 20, 5 + self.textIndent, top + 20, text_anchor='start'))
            # else:
            #     table.append(
            #         draw.Text(line['name'], 20, 5, top + 20, text_anchor='start'))

            table.append(draw.Text(line['start'], 20, self.nameTextSize,
                                   top + 20, text_anchor='start'))
            table.append(draw.Text(line['finish'], 20, self.nameTextSize +
                                   100, top + 20, text_anchor='start'))
            # if 'progress' in line:
            #     table.append(draw.Text(
            #         str(line['progress']), 20, self.nameTextSize + 200, top + 20, text_anchor='start'))

            table.append(draw.Text(str(end+1), 20, self.nameTextSize +
                                   210, top + 20, text_anchor='start'))
            if 'resource' in line:
                table.append(draw.Text(
                    str(line['resource']), 20, self.nameTextSize + 250, top + 20, text_anchor='start'))
            lineGroup.append(table)

        group = draw.Group(id='item')
        # fill='none', stroke='black'

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
            if 'milestone' in line and line['milestone']:
                mleft = left + 15
                mtop = top + 4
                p = draw.Path(fill='black')
                p.M(mleft, mtop).L(mleft+11, top+15).L(mleft, top +
                                                       26).L(mleft - 11, top + 15).L(mleft, mtop).Z()
                group.append(p)
                group.append(draw.Text(datetime.strptime(line['start'], '%Y-%m-%d').strftime('%Y年%m月%d日'),
                                       18, left + 30, top + 20, text_anchor='start', fill='black'))
            else:
                # 工时
                r = draw.Rectangle(left, top + 4, right,
                                   self.barHeight, fill='#67AAFF', stroke='black')
                r.append_title(line['name'])
                group.append(r)

                # 进度
                if 'progress' in line and line['progress'] > 0:

                    progress = 0
                    if line['progress'] > end + 1:
                        progress = end + 1
                    else:
                        progress = line['progress']

                    progressBar = draw.Rectangle(
                        left+2, top + 7, 30 * progress - 2, self.progressHeight, fill='#8AD97A')
                    # progressBar.append_title(str(progress))
                    group.append(progressBar)
                    group.append(draw.Text("%d%%" % ((progress/(end+1))*100),
                                           10, left + 5, top + 18, text_anchor='start', fill='black'))

        # 分割线
        group.append(draw.Lines(1, top + self.itemHeight,
                                self.canvasWidth, top + self.itemHeight, stroke='grey'))

        lineGroup.append(group)
        self.itemLine += 1
        return lineGroup

    def legend(self):
        top = 10
        self.draw.append(draw.Text("https://www.netkiller.cn - design by netkiller",
                                   15, self.canvasWidth - 300, top + 30, text_anchor='start', fill='grey'))
        # print(self.linkPosition)

    def hideTable(self):
        self.isTable = True

    def task(self):
        taskGroup = draw.Group(id='task')
        for id, line in self.data.items():
            if 'subitem' in line:
                item = self.items(line, True)
                taskGroup.append(item)
                self.textIndent += 1
                for id, item in line['subitem'].items():
                    item = self.items(item)
                    taskGroup.append(item)
                self.textIndent -= 1
            else:
                item = self.items(line)
                taskGroup.append(item)
        self.draw.append(taskGroup)

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
        return linkGroup

    def next(self):
        handover = draw.Group(id='handover')
        for id, line in self.data.items():
            if 'next' in line and line['next'] and int(line['next']) > 0:
                link = self.link(self.linkPosition[line['id']],
                                 self.linkPosition[line['next']])
                handover.append(link)
            if 'subitem' in line:
                for id, item in line['subitem'].items():
                    if 'next' in item and line['next'] and int(item['next']) > 0:
                        link = self.link(
                            self.linkPosition[item['id']], self.linkPosition[item['next']])
                        handover.append(link)
        self.draw.append(handover)

    def workload(self, title):
        self.startPosition = 400
        left = self.startPosition
        top = 80

        self.title(title)

        for key, value in self.data.items():
            self.fontSize = self.getTextSize(key)

            start = datetime.strptime(value['start'], '%Y-%m-%d').date()
            finish = datetime.strptime(value['finish'], '%Y-%m-%d').date()

            if self.beginDate > start:
                self.beginDate = start

            if self.endDate < finish:
                self.endDate = finish

        # print(self.fontSize)

        chart = draw.Group(id='workload')

        table = draw.Group(id='table')
        table.append_title('表格')
        table.append(draw.Line(1, 80, self.canvasWidth,
                               80,  stroke='black'))
        table.append(draw.Text('资源', 20, 5, top + 20, fill='#555555'))
        table.append(draw.Line(self.nameTextSize + 100, top,
                     self.nameTextSize + 100, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('开始日期', 20, self.nameTextSize +
                     100, top + 20, fill='#555555'))
        table.append(draw.Line(self.nameTextSize + 200, top,
                     self.nameTextSize + 200, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('截止日期', 20, self.nameTextSize +
                     200, top + 20, fill='#555555'))
        table.append(draw.Line(self.nameTextSize + 300, top,
                     self.nameTextSize + 300, self.canvasHeight, stroke='grey'))
        table.append(draw.Text('工时', 20, self.nameTextSize +
                               300, top + 20, fill='#555555'))
        table.append(draw.Line(self.nameTextSize + 400, top,
                               self.nameTextSize + 400, self.canvasHeight, stroke='grey'))

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

        for resource, row in self.data.items():
            #     print(resource, row)

            # # 工时
            top = 110 + self.itemLine * self.itemHeight + self.splitLine * self.itemLine
            end = (datetime.strptime(row['finish'], '%Y-%m-%d').date() -
                   datetime.strptime(row['start'], '%Y-%m-%d').date()).days
            # end = (row['finish'] - row['start']).days
            right = self.itemWidth * (end + 1) + (1 * end)

            chart.append(draw.Text(resource, 20, 5 + (self.textIndent *
                         self.itemWidth), top + 20, text_anchor='start'))
            chart.append(draw.Text(row['start'], 20, self.nameTextSize + 100,
                                   top + 20, text_anchor='start'))
            chart.append(draw.Text(row['finish'], 20, self.nameTextSize +
                                   200, top + 20, text_anchor='start'))

            chart.append(draw.Text(str(end), 20, self.nameTextSize +
                                   300, top + 20, text_anchor='start'))

            left = self.dayPosition[row['start']]
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
        if self.nameTextSize + self.textIndentSize < length:
            self.nameTextSize = length
            # print(+ self.textIndent)

        if 'resource' in item:
            length = self.getTextSize(item['resource'])
            if self.resourceTextSize < length:
                self.resourceTextSize = length

        # begin = datetime.strptime(item['start'], '%Y-%m-%d').date()
        self.minDate.append(item['start'])
        # end = datetime.strptime(item['finish'], '%Y-%m-%d').date()
        self.maxDate.append(item['finish'])

    def ganttChart(self, title):
        self.maxDate = []
        self.minDate = []
        lineNumber = len(self.data)
        # textIndent = 0
        for id, line in self.data.items():
            self.initialize(line)
            if 'subitem' in line:
                for id, item in line['subitem'].items():
                    self.initialize(item)
                self.textIndentSize = 30
                lineNumber += len(line['subitem'].items())

        begin = min(sorted(self.minDate, key=lambda d: datetime.strptime(
            d, "%Y-%m-%d").timestamp()))
        end = max(sorted(self.maxDate, key=lambda d: datetime.strptime(
            d, "%Y-%m-%d").timestamp()))
        self.beginDate = datetime.strptime(begin, '%Y-%m-%d').date()
        self.endDate = datetime.strptime(end, '%Y-%m-%d').date()
        # print(self.minDate, begin)
        # print(self.maxDate, end)
        # print(self.beginDate, self.endDate)

        # self.nameTextSize += self.textIndent

        if not self.isTable:
            self.startPosition = self.nameTextSize + self.resourceTextSize + 250

        if title:
            self.canvasTop += 50

        days = self.endDate - self.beginDate
        self.canvasWidth = self.startPosition + self.unitWidth * \
            days.days + days.days + self.unitWidth
        self.canvasHeight = self.canvasTop + self.unitHeight * \
            3 + self.unitHeight * lineNumber + lineNumber
        # print(self.canvasTop, self.canvasHeight)

        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)
        self.draw.append(draw.Rectangle(0, 0, self.canvasWidth - 1,
                                        self.canvasHeight-1, fill='#eeeeee', stroke='black'))

        self.title(title)
        self.calendar()
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
