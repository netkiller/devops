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
        # self.parser.add_option("-c", "--config", dest="config", help="config file",                               default='/usr/local/etc/wechat.ini', metavar="/usr/local/etc/wechat.ini")
        self.parser.add_option('-l', '--load', dest='load',
                               help='load data from file.', default=None, metavar='/path/to/gantt.json')
        self.parser.add_option('-s', '--save', dest='save',
                               help='save file', default=None, metavar='/path/to/gantt.svg')
        self.parser.add_option(
            '', "--stdin", action="store_true", dest="stdin", help="cat gantt.json | gantt -s file.svg")
        self.parser.add_option(
            '-d', "--debug", action="store_true", dest="debug", help="debug mode")

        self.gantt = Gantt()

    def usage(self):
        self.parser.print_help()
        print("\nHomepage: https://www.netkiller.cn\tAuthor: Neo <netkiller@msn.com>")
        print("Help: https://github.com/netkiller/devops/blob/master/doc/gantt.md")
        exit()

    def main(self):
        (options, args) = self.parser.parse_args()
        if options.stdin:
            data = sys.stdin.read()
            print(data)
        elif options.save:
            self.gantt.save(options.save)
        elif options.debug:
            print(options, args)
            data = [
                {'title': 'S级需求开发排期', 'begin': '2023-03-06', 'end': '2023-03-22', 'subitem': [
                    {'title': 'P1.5.1 开发', 'begin': '2023-03-06',
                     'end': '2023-03-15', 'progress': 4, 'resource' :'陈景峰'},
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
            
        else:
            self.usage()

        self.gantt.title("Gantt Test")
        self.gantt.load(data)
        self.gantt.rander()
        self.gantt.save('gantt.svg')


ganttChart = GanttChart()
ganttChart.main()
