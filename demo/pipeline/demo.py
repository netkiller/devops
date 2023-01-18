#!/usr/bin/env python3

from multiprocessing.connection import Pipe
import sys
sys.path.insert(0, '/Users/neo/workspace/GitHub/devops')

from netkiller.kubernetes import *
from netkiller.git import *
from netkiller.pipeline import *

def test():
    pipeline = Pipeline('kkk')
    pipeline.env('JAVA_HOME','/Library/Java/JavaVirtualMachines/jdk1.8.0_341.jdk/Contents/Home')
    pipeline.begin('name').checkout('url','branch').build('build').dockerfile(registry="registry",dir="module").startup(['ls']).end(["docker images | grep none | awk '{ print $3; }' | xargs docker rmi"]).debug()


def main():
    test()

if __name__ == "__main__":
    main()