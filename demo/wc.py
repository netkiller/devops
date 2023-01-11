#!/usr/bin/env python
# -*- coding: utf-8 -*-
from graphviz import Digraph

A = [('Yellow', 'ink'), ('blue', 'ink'), ('pink', 'ink')]

e = Digraph()
e.attr(rankdir='LR')
for a in A:
    e.node(a[0])
    e.edge(a[0], a[1])

e.view()
