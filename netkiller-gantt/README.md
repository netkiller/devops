# netkiller-gantt
Best project gantt charts in Python

![甘特图](doc/gantt.svg "Gantt chart")

# Python Gantt 工具

## 安装

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install netkiller-gantt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

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

## 从 CSV 文件生成

```sql
select id, parent, name,estStarted,deadline,assignedTo  from zt_task 
INTO OUTFILE '/tmp/project.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ‘,’
ESCAPED BY '"'
LINES TERMINATED BY '\r\n';
```

```shell
rm -rf /tmp/project.csv
cat <<EOF | mysql -h127.0.0.1 -uroot -p123456 zentao
SELECT 'id','name','start','finish', 'resource', 'parent'
UNION
select id, name,estStarted,deadline,assignedTo, parent  from zt_task
INTO OUTFILE '/tmp/project.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ','
ESCAPED BY '"'
LINES TERMINATED BY '\r\n';
EOF
```

```
select id, name,estStarted as start, deadline as finish,  assignedTo as resource, parent from zt_task where `group` = 4 order by id desc limit 100;
select id, name,estStarted as start, deadline as finish,  assignedTo as resource, parent from zt_task where assignedTo in ('chenjingfeng','ligongfa','yuanjianfeng','liqiang') order by id desc limit 100;
```