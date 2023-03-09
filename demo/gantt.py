#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
##############################################
import os
import sys
module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0, module)

try:
    from netkiller.gantt import Gantt
    import cv2
    import requests

    import logging
    import logging.handlers
    from optparse import OptionParser, OptionGroup
except ImportError as err:
    print("Error: %s" % (err))


class GanttChart:
    def __init__(self) -> None:

        self.parser = OptionParser("usage: %prog [options] message")
        self.parser.add_option("-c", "--config", dest="config", help="config file",
                               default='/usr/local/etc/wechat.ini', metavar="/usr/local/etc/wechat.ini")
        self.parser.add_option('-e', '--corporate', dest='corporate',
                               help='corporate', default='default', metavar='default')
        self.parser.add_option('-t', '--totag', dest='totag',
                               help='tag', default='1', metavar='"1|2|3"')
        self.parser.add_option(
            '-s', "--stdin", action="store_true", dest="stdin", help="stdin")
        self.parser.add_option(
            "", "--debug", action="store_true", dest="debug", help="debug mode")

        (options, args) = self.parser.parse_args()

        self.gantt = Gantt()

    def main(self):
        data = [
            {'title': 'S级需求开发排期', 'begin': '2023-03-06', 'end': '2023-03-22', 'subitem': [
                {'title': 'P1.5.1 开发', 'begin': '2023-03-06',
                    'end': '2023-03-15', 'progress': 4},
                {'title': 'P1.5.1 开发', 'begin': '2023-03-15',
                    'end': '2023-03-22', 'progress': 0},
            ]},

            {'title': 'S级需求测试排期', 'begin': '2023-03-06', 'end': '2023-03-22', 'subitem': [
                {'title': 'P1.5.1 开发', 'begin': '2023-03-06',
                    'end': '2023-03-15', 'progress': 4},
                {'title': 'P1.5.1 开发', 'begin': '2023-03-15',
                    'end': '2023-03-22', 'progress': 0},
            ]},

            {'title': '汉字', 'begin': '2023-03-01',
                'end': '2023-03-05', 'progress': 3},
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
        self.gantt.title("Gantt Test")
        self.gantt.load(data)
        self.gantt.rander()
        self.gantt.save()


ganttChart = GanttChart()
ganttChart.main()
