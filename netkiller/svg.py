#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-23
##############################################



class Line:
    def __init__(self, x1, y1, x2, y2, **attribute) -> None:
        print(x1, y1, x2, y2)
        print(attribute)
        postion = (x1, y1, x2, y2)
        print(type(postion))
        

class ScalableVectorGraphics:
    svg = []
    def __init__(self) -> None:
        # self.svg = []
        pass

    def appendChild(self, child):
        self.svg.append(child)

    def display(self):
        print(self.svg)

            
    def save(self):
        pass
    def debug(self):
        self.display()


# line = Line(1,1,10,10)
# print(line)
svg = ScalableVectorGraphics()
svg.Line(1,1,10,10)
# svg.debug()
