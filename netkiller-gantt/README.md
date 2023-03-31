# netkiller-gantt
Best project gantt charts in Python

![甘特图](https://github.com/netkiller/devops/raw/master/netkiller-gantt/doc/gantt.svg "Gantt chart")

# Python Gantt 工具

## 安装

MacOS 环境

```bash
brew install cairo
brew install pkg-config
pip3 install pycairo -i https://pypi.tuna.tsinghua.edu.cn/simple


```

Linux 环境

```shell
dnf install -y cairo-devel python3-cairo python3-pillow

```

配置镜像

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

root@netkiller ~# cat /root/.config/pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

安装

```shell
pip install netkiller-gantt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 命令帮助

```bash
root@netkiller ~# gantt 
Usage: gantt [options] 

Options:
  -h, --help            show this help message and exit
  -t 项目甘特图, --title=项目甘特图
                        甘特图标题
  -c /path/to/gantt.csv, --csv=/path/to/gantt.csv
                        /path/to/gantt.csv
  -l /path/to/gantt.json, --load=/path/to/gantt.json
                        load data from file.
  -s /path/to/gantt.svg, --save=/path/to/gantt.svg
                        save file
  --stdin               cat gantt.json | gantt -s file.svg
  -g, --gantt           Gantt chart
  -w, --workload        Workload chart
  -d, --debug           debug mode

Homepage: https://www.netkiller.cn	Author: Neo <netkiller@msn.com>
Help: https://github.com/netkiller/devops/blob/master/doc/gantt/index.md
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
select id, name,estStarted as start, deadline as finish,  assignedTo as resource, parent from zt_task where assignedTo in ('neo','netkiller','tom','jerry') order by id desc limit 100;
```

## 从数据库生成甘特图

### MySQL 5.7

```sql

CREATE TABLE `project` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '任务名称',
  `start` date NOT NULL COMMENT '开始日期',
  `finish` date NOT NULL COMMENT '完成日期',
  `resource` varchar(255) DEFAULT NULL COMMENT '资源',
  `predecessor` bigint(20) DEFAULT NULL COMMENT '前置任务',
  `milestone` bit(1) DEFAULT NULL COMMENT '里程碑',
  `parent` bigint(20) DEFAULT NULL COMMENT '父任务',
  `status` enum('Enabled','Disabled') DEFAULT 'Enabled' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `project_has_subproject` (`parent`),
  CONSTRAINT `project_has_subproject` FOREIGN KEY (`parent`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4

```

### MySQL 8.0

```sql
CREATE TABLE `project` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `start` date NOT NULL DEFAULT (curdate()) COMMENT '开始日期',
  `finish` date NOT NULL DEFAULT (curdate()) COMMENT '完成日期',
  `resource` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '资源',
  `predecessor` bigint unsigned DEFAULT NULL COMMENT '前置任务',
  `milestone` bit(1) DEFAULT NULL COMMENT '里程碑',
  `parent` bigint unsigned DEFAULT NULL COMMENT '父任务',
  `status` enum('Enabled','Disabled') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'Enabled' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `project_has_subproject` (`parent`),
  KEY `task_has_predecessor_idx` (`predecessor`),
  CONSTRAINT `project_has_subproject` FOREIGN KEY (`parent`) REFERENCES `project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

UPDATE `test`.`project` SET `milestone` = b'001'  WHERE (`id` = '11');
```

```bash

gantt --host mysql.netkiller.cn -u root -p passw0rd --database test -g

```