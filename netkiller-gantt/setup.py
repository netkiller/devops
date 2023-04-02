from netkiller import __version__, __author__
import os
import sys
from setuptools import setup, find_packages
sys.path.insert(0, os.path.abspath('lib'))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="netkiller-gantt",
    version=__version__,
    author=__author__,
    author_email="netkiller@msn.com",
    description="Best Gantt chart in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.netkiller.cn",
    license='CC 3.0',
    classifiers=[
                # 'Development Status :: 1 - Production/Stable',
                'Environment :: Console',
                "Programming Language :: Python :: 3",
                # "License :: OSI Approved :: CC 2.0",
                "Operating System :: OS Independent",
    ],
    install_requires=['pillow', 'drawsvg', 'pyproject.toml', 'pycairo','mysql-connector-python'],
    #   'opencv-python',
    # package_dir={ '': '..' },
    # packages=find_packages('../netkiller'),
    packages=find_packages(),

    scripts=[
        'bin/gantt',
    ],
    data_files=[
        ('share/netkiller', ['doc/gantt.svg','doc/by-nc-sa.png','font/Songti.ttc']),

    ]
)
