# Python Gantt 工具

## 命令帮助

```bash
neo@MacBook-Pro-M2 ~> gantt -h

Usage: gantt [options] message

Options:
  -h, --help            show this help message and exit
  -l /path/to/gantt.json, --load=/path/to/gantt.json
                        load data from file.
  -s /path/to/gantt.svg, --save=/path/to/gantt.svg
                        save file
  --stdin               cat gantt.json | gantt -s file.svg
  -d, --debug           debug mode

```

## 从标准输出载入json数据生成甘特图

```bash
neo@MacBook-Pro-M2 ~> cat gantt.json | gantt --stdin
/Users/neo/workspace/GitHub/devops
Usage: gantt [options] message

Options:
  -h, --help            show this help message and exit
  -l /path/to/gantt.json, --load=/path/to/gantt.json
                        load data from file.
  -s /path/to/gantt.svg, --save=/path/to/gantt.svg
                        save file
  --stdin               cat gantt.json | gantt -s file.svg
  -d, --debug           debug mode
```