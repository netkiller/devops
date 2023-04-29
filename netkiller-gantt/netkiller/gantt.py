#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-09
##############################################
try:
    import calendar
    import drawsvg as draw
    from datetime import datetime, date
    from PIL import ImageFont
    import requests
    import os
    import platform
except ImportError as err:
    print("Error: %s" % (err))


class Canvas:
    width = 1980
    height = 1080


class Data:
    data = {}

    def __init__(self) -> None:
        pass

    def add(self, id, name, start, finish, resource, predecessor, milestone, parent):
        # duration
        item = {"id": id, "name": name, "start": start, "finish": finish, "resource": resource, "predecessor": predecessor, "milestone": milestone}

        if parent != "" and int(parent) > 0:
            # print(parent)
            if not "subitem" in self.data[parent]:
                self.data[parent]["subitem"] = {}
            self.data[parent]["subitem"][id] = item

        else:
            self.data[id] = item

    def addFromMySQL(self, row):
        # if row['milestone'] == 'TRUE':
        #     row['milestone'] = True
        # else:
        #     row['milestone'] = False

        id = row["id"]
        parent = row["parent"]
        row["start"] = row["start"].strftime("%Y-%m-%d")
        row["finish"] = row["finish"].strftime("%Y-%m-%d")
        if not row["resource"]:
            row["resource"] = ""
        # print(type(parent))
        if parent and parent > 0:
            if not "subitem" in self.data[parent]:
                self.data[parent]["subitem"] = {}
            self.data[parent]["subitem"][id] = row

        else:
            self.data[id] = row

    def addDict(self, item):
        pass


class Calendar(Canvas):
    draw = None
    canvasWidth = 0
    canvasHeight = 0
    splitLine = 1
    canvasTop = 0
    canvasLeft = 0
    startPosition = 0
    itemLine = 0
    rowHeight = 30
    columeWidth = 30
    barHeight = 20
    progressHeight = 14
    nameTextSize = 1
    resourceTextSize = 90
    beginDate = datetime.now().date()
    endDate = datetime.now().date()
    weekdayPosition = 0
    dayPosition = {}
    linkPosition = {}
    # 隐藏表格
    isTable = False

    def __init__(self) -> None:
        super().__init__()

    def __table(self, top):
        group = draw.Group(id="table")
        group.append_title("表格")
        # group.append(draw.Line(1, 80, self.canvasWidth,                               80,  stroke='black'))
        group.append(draw.Text("任务", 20, 5, top + 20 + self.rowHeight * 2, fill="#555555"))
        group.append(draw.Line(self.nameTextSize, top + self.rowHeight * 2, self.nameTextSize, self.canvasHeight, stroke="grey"))
        group.append(draw.Text("开始日期", 20, self.nameTextSize + 5, top + 20 + self.rowHeight * 2, fill="#555555"))
        group.append(draw.Line(self.nameTextSize + 95, top + self.rowHeight * 2, self.nameTextSize + 95, self.canvasHeight, stroke="grey"))
        group.append(draw.Text("截止日期", 20, self.nameTextSize + 100, top + 20 + self.rowHeight * 2, fill="#555555"))
        group.append(draw.Line(self.nameTextSize + 190, top + self.rowHeight * 2, self.nameTextSize + 190, self.canvasHeight, stroke="grey"))
        group.append(draw.Text("工时", 20, self.nameTextSize + 195, top + 20 + self.rowHeight * 2, fill="#555555"))
        group.append(draw.Line(self.nameTextSize + 240, top + self.rowHeight * 2, self.nameTextSize + 240, self.canvasHeight, stroke="grey"))
        group.append(draw.Text("资源", 20, self.nameTextSize + 245, top + 20 + self.rowHeight * 2, fill="#555555"))

        return group

    def weekNumberOfMonth(self, currentDate):
        # firstDay = currentDate.replace(            day=1, hour=0, minute=0, second=0, microsecond=0)
        firstDay = currentDate.replace(day=1)
        number = int(currentDate.strftime("%W")) - int(firstDay.strftime("%W")) + 1
        # print(currentDate, number)
        return number

    def __weekdays(self, top, begin, end):
        offsetX = 1
        column = 0

        begin = datetime.strptime(begin, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")

        beginDay = begin.day
        endDay = end.day
        # print(beginDay, endDay)

        weekNumberOfYear = datetime.strptime(str(begin.year) + "-" + str(begin.month) + "-01", "%Y-%m-%d").strftime("%W")
        # weekNumberOfYear = begin.strftime('%W')
        # weekNumberOfYear = datetime.date(datetime.now().year,month,1).strftime('%W')
        weekGroups = {}
        weekGroups[weekNumberOfYear] = draw.Group(id="week" + str(weekNumberOfYear))

        for day in range(beginDay, endDay + 1):
            # numberOfWeek = self.weekNumberOfMonth(datetime.strptime(str(begin.year)+'-'+str(begin.month)+'-'+str(day), '%Y-%m-%d').date())
            weekday = calendar.weekday(begin.year, begin.month, day)

            currentweekNumberOfYear = datetime.strptime(str(begin.year) + "-" + str(begin.month) + "-" + str(day), "%Y-%m-%d").strftime("%W")
            # print(weekNumberOfYear, currentweekNumberOfYear)
            if currentweekNumberOfYear != weekNumberOfYear:
                weekNumberOfYear = currentweekNumberOfYear
                weekGroups[weekNumberOfYear] = draw.Group(id="week" + str(weekNumberOfYear))
            if self.firstsd == True:
                if (int(weekNumberOfYear) % 2) == 0:
                    self.workweeks = 6
                else:
                    self.workweeks = 5
            if weekday >= self.workweeks:
                color = "#dddddd"
            else:
                color = "#cccccc"

            x = self.weekdayPosition + self.columeWidth * (column) + offsetX
            self.dayPosition[date(year=int(begin.year), month=int(begin.month), day=int(day)).strftime("%Y-%m-%d")] = x

            if day == beginDay:
                weekGroups[weekNumberOfYear].append(draw.Text(begin.strftime("%Y年%m月"), 20, x + 4, top + self.rowHeight - 10, fill="#555555"))
            # 右侧封闭
            if day == endDay:
                weekGroups[weekNumberOfYear].append(draw.Line(x + self.columeWidth, top, x + self.columeWidth, self.canvasHeight, stroke="black"))

            # dayName = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
            dayName = ["一", "二", "三", "四", "五", "六", "日"]

            weekGroups[weekNumberOfYear].append(draw.Text(dayName[weekday], 20, x + 4, top + self.columeWidth * 2 - 10, fill="#555555"))
            if day < 10:
                numberOffsetX = 10
            else:
                numberOffsetX = 0

            # 日栏位
            # print(self.weekdayPosition)
            r = draw.Rectangle(x, top + self.rowHeight * 2, self.columeWidth, self.canvasHeight - (top + self.rowHeight * 2), fill=color)
            r.append_title(str(day))
            weekGroups[weekNumberOfYear].append(r)
            # 周分割线
            if weekday == 6:
                weekGroups[weekNumberOfYear].append(draw.Line(x + self.columeWidth, top + self.rowHeight, x + self.columeWidth, self.canvasHeight, stroke="black"))
            # 日期
            weekGroups[weekNumberOfYear].append(draw.Text(str(day), 20, x + numberOffsetX, top + self.columeWidth * 3 - 10, fill="#555555"))

            # if column:
            offsetX += self.splitLine
            column += 1

        self.weekdayPosition = x + self.columeWidth

        return weekGroups

    def __month(self, top, months):
        monthGroups = {}
        for begin, end in months:
            month = datetime.strptime(begin, "%Y-%m-%d").month
            monthGroups[month] = draw.Group(id="month" + str(month))
            for key, value in self.__weekdays(top, begin, end).items():
                monthGroups[month].append(value)

        return monthGroups

    def __monthRange(self, begin, end):
        years = {}
        # result = []
        while True:
            if begin.month == 12:
                next = begin.replace(year=begin.year + 1, month=1, day=1)
            else:
                next = begin.replace(month=begin.month + 1, day=1)
            if next > end:
                break

            day = calendar.monthrange(begin.year, begin.month)[1]

            # result.append((begin.strftime("%Y-%m-%d"),
            #                begin.replace(day=day).strftime("%Y-%m-%d")))
            if not begin.year in years:
                years[begin.year] = []
            years[begin.year].append((begin.strftime("%Y-%m-%d"), begin.replace(day=day).strftime("%Y-%m-%d")))
            begin = next
        # result.append((begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

        if not end.year in years:
            years[end.year] = []
        years[end.year].append((begin.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
        # print(years)
        return years

    def calendarYear(self, top):
        self.weekdayPosition = self.startPosition
        yearGroups = {}
        # print(self.beginDate, self.endDate)
        years = self.__monthRange(self.beginDate, self.endDate)

        # print(len(years))
        for year, month in years.items():
            # print(year, month)
            # begin = datetime.strptime(begin, "%Y-%m-%d").date()
            # end = datetime.strptime(end, "%Y-%m-%d").date()
            yearGroups[year] = draw.Group(id="year" + str(year))
            for key, value in self.__month(top, month).items():
                yearGroups[year].append(value)
        return yearGroups

    def setWorkweeks(self, workweeks=5, firstsd=False):
        # 'five-day','six-day'
        self.workweeks = workweeks
        self.firstsd = firstsd

    def calendar(self):
        left = self.startPosition
        top = self.canvasTop

        background = draw.Group(id="calendar")
        if not self.isTable:
            background.append(self.__table(top))

        for key, value in self.calendarYear(top).items():
            background.append(value)
        # for key, value in self.__month(top).items():
        #     background.append(value)
        # 月线
        background.append(draw.Line(1, top + self.rowHeight, self.canvasWidth, top + self.rowHeight, stroke="grey"))

        # top = draw.Line(0, 0, self.canvasWidth, 0, stroke='black')
        # right = draw.Line(self.canvasWidth, 0,
        #                   self.canvasWidth, self.canvasHeight, stroke='black')
        # 周线
        background.append(draw.Line(1, top + self.rowHeight * 2, self.canvasWidth, top + self.rowHeight * 2, stroke="grey"))
        # 日线
        background.append(draw.Line(1, top + self.rowHeight * 3, self.canvasWidth, top + self.rowHeight * 3, stroke="grey"))
        # 上边封闭
        background.append(draw.Line(1, top, self.canvasWidth, top, stroke="grey"))
        # 左边封闭
        background.append(draw.Line(left, top + self.rowHeight, left, self.canvasHeight, stroke="grey"))
        self.draw.append(background)


class Gantt(Calendar):
    data = {}
    textIndent = 0
    textIndentSize = 19

    def __init__(self) -> None:
        super().__init__()
        self.canvasWidth = self.width
        self.canvasHeight = self.height
        self.workweeks = 5
        self.firstsd = None
        self.fontSize = 18

        pass

    def name(self, name):
        self.name = name

    def title(self, text):
        if self.isTable:
            return
        if text:
            self.canvasTop += 50

        group = draw.Group(id="title", onclick="this.style.stroke = 'green'; ")
        group.append(draw.Text(text, 30, self.canvasWidth / 2, 25, center=True, text_anchor="middle"))
        group.append(draw.Text(self.name, 20, 5, self.rowHeight * 3 + 12))
        self.draw.append(group)

    def legend(self):
        if self.isTable:
            return
        top = 10
        self.draw.append(draw.Text("https://www.netkiller.cn - design by netkiller", 15, self.canvasWidth - 280, top + 30, text_anchor="start", fill="grey"))
        self.draw.append(draw.Rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill="none", stroke="black"))
        # fill='#eeeeee'
        license = "/var/tmp/by-nc-sa.png"
        if not os.path.exists(license):
            # url = 'https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png'
            url = "https://www.netkiller.cn/graphics/by-nc-sa.png"
            # license = wget.download(url, out=license)
            request = requests.get(url)
            if request.status_code == 200:
                file = open(license, "wb")
                file.write(request.content)
                file.flush()
                file.close()

        self.draw.append(draw.Image(8, 8, 100, 34.99, license, embed=True))

    def hideTable(self):
        self.isTable = True

    def items(self, line, subitem=False):
        top = self.canvasTop + self.rowHeight * 3 + self.itemLine * self.rowHeight + self.splitLine * self.itemLine

        begin = datetime.strptime(line["start"], "%Y-%m-%d").day
        # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        end = (datetime.strptime(line["finish"], "%Y-%m-%d").date() - datetime.strptime(line["start"], "%Y-%m-%d").date()).days

        # left += self.columeWidth * (begin - 1) + (1 * begin)
        # # 日宽度 + 竖线宽度
        right = self.columeWidth * (end + 1) + (1 * end)

        left = self.dayPosition[line["start"]]
        # right = self.dayPosition[line['end']]

        self.linkPosition[line["id"]] = {"x": left, "y": top, "width": right}

        lineGroup = draw.Group(id="task")
        if not self.isTable:
            table = draw.Group(id="text")

            table.append(draw.Text(line["name"], self.fontSize, 5 + (self.textIndent * self.textIndentSize), top + 20, text_anchor="start"))
            # text.append(draw.TSpan(line['begin'], text_anchor='start'))
            # text.append(draw.TSpan(line['end'], text_anchor='start'))

            table.append(draw.Text(line["start"], self.fontSize, self.nameTextSize + 5, top + 20, text_anchor="start"))
            table.append(draw.Text(line["finish"], self.fontSize, self.nameTextSize + 100, top + 20, text_anchor="start"))
            # if 'progress' in line:
            #     table.append(draw.Text(
            #         str(line['progress']), 20, self.nameTextSize + 200, top + 20, text_anchor='start'))

            table.append(draw.Text(str(end + 1), self.fontSize, self.nameTextSize + 205, top + 20, text_anchor="start"))
            if "resource" in line:
                table.append(draw.Text(str(line["resource"]), self.fontSize, self.nameTextSize + 245, top + 20, text_anchor="start"))
            lineGroup.append(table)

        group = draw.Group(id="item")
        # fill='none', stroke='black'

        if subitem:
            # print(begin,end)
            # print(left,top,right)
            offsetY = 7
            length = left + right
            group.append(
                draw.Lines(
                    # 坐标
                    left,
                    top + offsetY,
                    # 横线
                    length,
                    top + offsetY,
                    # 竖线
                    length,
                    top + 24,
                    # 斜线
                    length - 10,
                    top + 15,
                    # 横线2
                    left + 10,
                    top + 15,
                    # # 斜线
                    left,
                    top + 24,
                    # # 闭合竖线
                    left,
                    top + offsetY,
                    fill="black",
                    stroke="black",
                )
            )
        else:
            if "milestone" in line and line["milestone"]:
                mleft = left + 15
                mtop = top + 4
                p = draw.Path(fill="black")
                p.M(mleft, mtop).L(mleft + 11, top + 15).L(mleft, top + 26).L(mleft - 11, top + 15).L(mleft, mtop).Z()
                group.append(p)
                group.append(draw.Text(datetime.strptime(line["start"], "%Y-%m-%d").strftime("%Y年%m月%d日"), 18, left + 30, top + 20, text_anchor="start", fill="black"))
            else:
                # 工时
                r = draw.Rectangle(left, top + 4, right, self.barHeight, fill="#67AAFF", stroke="black")
                r.append_title(line["name"])
                group.append(r)

                # 进度
                if "progress" in line and line["progress"] > 0:
                    progress = 0
                    if line["progress"] > end + 1:
                        progress = end + 1
                    else:
                        progress = line["progress"]

                    progressBar = draw.Rectangle(left + 2, top + 7, 30 * progress - 2, self.progressHeight, fill="#8AD97A")
                    # progressBar.append_title(str(progress))
                    group.append(progressBar)
                    group.append(draw.Text("%d%%" % ((progress / (end + 1)) * 100), 10, left + 5, top + 18, text_anchor="start", fill="black"))

        # 分割线
        group.append(draw.Lines(1, top + self.rowHeight, self.canvasWidth, top + self.rowHeight, stroke="grey"))

        lineGroup.append(group)
        self.itemLine += 1
        return lineGroup

    def tasks(self, data):
        for id, line in data.items():
            try:
                if "subitem" in line:
                    item = self.items(line, True)
                    self.taskGroup.append(item)
                    self.textIndent += 1
                    self.tasks(line["subitem"])
                    self.textIndent -= 1
                else:
                    item = self.items(line)
                    self.taskGroup.append(item)
            except KeyError as err:
                print("KeyError %s: %s" % (err, line))
                exit()

    def link(self, fromTask, toTask):
        # print(fromTask, toTask)
        linkGroup = draw.Group(id="link")
        x = fromTask["x"] + fromTask["width"] + 1
        y = fromTask["y"] + 15
        arrow = draw.Marker(-0.1, -0.51, 0.9, 0.5, scale=4, orient="auto")
        arrow.append(draw.Lines(-0.1, 0.5, -0.1, -0.5, 0.9, 0, fill="red", close=True))
        path = draw.Path(stroke="red", stroke_width=2, fill="none", marker_end=arrow)
        path.M(x, y).H(toTask["x"] + 15).V(toTask["y"] - 5)
        linkGroup.append(path)
        return linkGroup

    def predecessor(self, data):
        for id, task in data.items():
            try:
                if "subitem" in task:
                    self.predecessor(task["subitem"])
                elif "predecessor" in task and task["predecessor"] and int(task["predecessor"]) > 0:
                    # print(self.linkPosition)
                    link = self.link(self.linkPosition[task["predecessor"]], self.linkPosition[task["id"]])
                    self.handover.append(link)
            except KeyError as err:
                print("KeyError: predecessor=%s, %s" % (err, task))

    def getTextSize(self, text, size=21):
        # # fontFace = cv2.FONT_HERSHEY_SIMPLEX
        # fontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        # # fontFace = cv2.FONT_HERSHEY_PLAIN
        # fontScale = 0.55
        # thickness = 2

        # size = cv2.getTextSize(text, fontFace, fontScale, thickness)
        # width, height = size[0]

        # font = 'AdobeFangsongStd-Regular.otf'
        # font = r'Apple Symbols.ttf'

        if platform.system() == "Linux":
            font = r"/usr/local/share/netkiller/Songti.ttc"
        elif platform.system() == "Darwin":
            font = r"/System/Library/Fonts/Supplemental/Songti.ttc"
        else:
            font = r"Songti.ttc"

        font = ImageFont.truetype(font=font, size=size, encoding="utf-8")
        # font = ImageFont.truetype("symbol.ttf", 16, encoding="symb")
        width, height = font.getsize(text)
        return width

    def load(self, data):
        self.data = data

    def __initialize(self, data):
        for id, item in data.items():
            if "subitem" in item:
                self.textIndent += 1
                self.__initialize(item["subitem"])
                self.lineNumber += len(item["subitem"].keys())
                self.textIndent -= 1

            # 计算文字宽度
            length = self.getTextSize(item["name"])

            # 文本表格所占用的宽度
            if self.textIndent > 0:
                if self.nameTextSize < length + self.textIndentSize:
                    self.nameTextSize = length + self.textIndentSize
            else:
                if self.nameTextSize < length:
                    self.nameTextSize = length

            if "resource" in item and item["resource"]:
                length = self.getTextSize(item["resource"])
                if self.resourceTextSize < length:
                    self.resourceTextSize = length

            # begin = datetime.strptime(item['start'], '%Y-%m-%d').date()
            self.minDate.append(item["start"])
            # end = datetime.strptime(item['finish'], '%Y-%m-%d').date()
            self.maxDate.append(item["finish"])

    def ganttChart(self, title):
        self.maxDate = []
        self.minDate = []
        self.lineNumber = len(self.data)

        self.__initialize(self.data)

        begin = min(sorted(self.minDate, key=lambda d: datetime.strptime(d, "%Y-%m-%d").timestamp()))
        end = max(sorted(self.maxDate, key=lambda d: datetime.strptime(d, "%Y-%m-%d").timestamp()))
        self.beginDate = datetime.strptime(begin, "%Y-%m-%d").date()
        self.endDate = datetime.strptime(end, "%Y-%m-%d").date()

        # print(self.maxDate, end)
        # print(self.beginDate, self.endDate)

        # 行首加5像素美化
        self.nameTextSize += 10

        if not self.isTable:
            self.startPosition = self.nameTextSize + self.resourceTextSize + 230

        days = self.endDate - self.beginDate
        self.canvasWidth = self.startPosition + self.columeWidth * days.days + days.days + self.columeWidth + 2
        self.canvasHeight = self.canvasTop + self.rowHeight * 5 + self.rowHeight * self.lineNumber + self.lineNumber + 20

        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)

        self.title(title)
        self.calendar()

        self.taskGroup = draw.Group(id="tasks")
        self.tasks(self.data)
        self.draw.append(self.taskGroup)

        self.handover = draw.Group(id="handover")
        self.predecessor(self.data)
        self.draw.append(self.handover)

        self.legend()

    def save(self, filename=None):
        if filename:
            # d.set_pixel_scale(2)  # Set number of pixels per geometry unit
            # d.set_render_size(400, 200)  # Alternative to set_pixel_scale
            self.draw.save_svg(filename)
        # self.draw.save_png('example.png')
        # self.draw.rasterize()

    def export(self, filename=None):
        if filename:
            self.draw.save_png("example.png")


class Workload(Gantt):
    def __init__(self) -> None:
        super().__init__()
        self.workloadData = {}
        self.minDate = []
        self.maxDate = []
        self.resourceTextSize = 0

    def __gantt2workload(self, data):
        # self.workloadData = dict()
        for key, item in data.items():
            if "subitem" in item:
                self.__gantt2workload(item["subitem"])

            if not "resource" in item:
                continue
            elif not item["resource"]:
                item["resource"] = "null"

            start = datetime.strptime(item["start"], "%Y-%m-%d").date()
            finish = datetime.strptime(item["finish"], "%Y-%m-%d").date()

            self.minDate.append(start)
            self.maxDate.append(finish)

            length = self.getTextSize(item["resource"])
            # print(self.resourceTextSize,length)
            if self.resourceTextSize < length:
                self.resourceTextSize = length

            if item["resource"] in self.workloadData.keys():
                # if data.has_key(item['resource']):

                # if not 'start' in self.workloadData[item['resource']]:
                # self.workloadData[item['resource']]['start']=''
                # if datetime.strptime(self.data[item['resource']]['start'], '%Y-%m-%d').date() > start:
                #     self.workloadData[item['resource']]['start'] = item['start']
                # if datetime.strptime(self.data[item['resource']]['finish'], '%Y-%m-%d').date() < finish:
                #     self.workloadData[item['resource']]['finish'] = item['finish']

                # print(self.workloadData)

                if self.workloadData[item["resource"]]["start"] > start:
                    self.workloadData[item["resource"]]["start"] = start
                if self.workloadData[item["resource"]]["finish"] < finish:
                    self.workloadData[item["resource"]]["finish"] = finish
            else:
                self.workloadData[item["resource"]] = {"resource": item["resource"], "start": start, "finish": finish}
        return self.workloadData

    def workload(self, title):
        self.data = self.__gantt2workload(self.data)

        self.startPosition = self.resourceTextSize + 300
        left = self.startPosition

        self.beginDate = min(self.minDate)
        self.endDate = max(self.maxDate)

        lineNumber = len(self.data)

        days = self.endDate - self.beginDate
        self.canvasWidth = self.startPosition + self.columeWidth * days.days + days.days + self.columeWidth + 2
        self.canvasHeight = self.canvasTop + self.rowHeight * 5 + self.rowHeight * lineNumber + lineNumber + 15
        # print(self.canvasTop, self.canvasHeight)

        self.draw = draw.Drawing(self.canvasWidth, self.canvasHeight)

        self.title(title)

        top = self.rowHeight * 4 - 10
        chart = draw.Group(id="workload")

        table = draw.Group(id="table")
        table.append_title("表格")
        # 封顶
        table.append(draw.Line(1, self.canvasTop, self.canvasWidth, self.canvasTop, stroke="black"))
        table.append(draw.Text("资源", 20, 5, top + 20, fill="#555555"))
        table.append(draw.Line(self.resourceTextSize, top, self.resourceTextSize, self.canvasHeight, stroke="grey"))
        table.append(draw.Text("开始日期", 20, self.resourceTextSize + +5, top + 20, fill="#555555"))
        table.append(draw.Line(self.resourceTextSize + 100, top, self.resourceTextSize + 100, self.canvasHeight, stroke="grey"))
        table.append(draw.Text("截止日期", 20, self.resourceTextSize + 100 + 5, top + 20, fill="#555555"))
        table.append(draw.Line(self.resourceTextSize + 200, top, self.resourceTextSize + 200, self.canvasHeight, stroke="grey"))
        table.append(draw.Text("工时", 20, self.resourceTextSize + 200 + 5, top + 20, fill="#555555"))
        # table.append(draw.Line(self.resourceTextSize + 400, top,                               self.resourceTextSize + 400, self.canvasHeight, stroke='grey'))

        chart.append(table)

        # for key, value in self.__month(top).items():
        #     chart.append(value)
        for key, value in super().calendarYear(self.canvasTop).items():
            chart.append(value)

        # print(self.dayPosition)

        # for key, value in self.__weekday(top).items():
        #     background.append(value)
        # 月线
        chart.append(draw.Line(self.startPosition, self.canvasTop + self.rowHeight, self.canvasWidth, self.canvasTop + self.rowHeight, stroke="grey"))
        # 周线
        chart.append(draw.Line(1, self.canvasTop + self.rowHeight * 2, self.canvasWidth, self.canvasTop + self.rowHeight * 2, stroke="grey"))

        chart.append(draw.Line(1, self.canvasTop + self.rowHeight * 3, self.canvasWidth, self.canvasTop + self.rowHeight * 3, stroke="black"))
        # 竖线
        chart.append(draw.Line(left, self.canvasTop, left, self.canvasHeight, stroke="grey"))

        # begin = datetime.strptime(line['begin'], '%Y-%m-%d').day
        # # end = datetime.strptime(line['end'], '%Y-%m-%d').day
        #

        # left += self.columeWidth * (begin - 1) + (1 * begin)
        # # 日宽度 + 竖线宽度
        self.canvasTop = self.rowHeight * 5 - 10
        for resource, row in self.data.items():
            # # 工时
            top = self.canvasTop + self.itemLine * self.rowHeight + self.splitLine * self.itemLine
            # print(resource, row, top)
            # end = (datetime.strptime(row['finish'], '%Y-%m-%d').date() -
            #        datetime.strptime(row['start'], '%Y-%m-%d').date()).days
            end = (row["finish"] - row["start"]).days
            # end = (row['finish'] - row['start']).days
            right = self.columeWidth * (end + 1) + (1 * end)

            chart.append(draw.Text(resource, self.fontSize, 5, top + 20, text_anchor="start"))
            chart.append(draw.Text(row["start"].strftime("%Y-%m-%d"), self.fontSize, self.resourceTextSize + 5, top + 20, text_anchor="start"))
            chart.append(draw.Text(row["finish"].strftime("%Y-%m-%d"), self.fontSize, self.resourceTextSize + 100 + 5, top + 20, text_anchor="start"))

            chart.append(draw.Text(str(end + 1), self.fontSize, self.resourceTextSize + 200 + 5, top + 20, text_anchor="start"))

            left = self.dayPosition[row["start"].strftime("%Y-%m-%d")]
            r = draw.Rectangle(left, top + 4, right, self.barHeight, fill="blue")
            r.append_title(resource)
            chart.append(r)

            chart.append(draw.Line(1, top + self.rowHeight, self.canvasWidth, top + self.rowHeight, stroke="grey"))

            self.itemLine += 1

        self.draw.append(chart)
        # self.draw.append(draw.Rectangle(1, 1, self.canvasWidth,
        #                                 self.canvasHeight, fill='none', stroke='black'))
        self.legend()

    def workloadChart(self, title):
        self.workload(title)
