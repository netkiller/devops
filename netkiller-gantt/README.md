# netkiller-gantt
Best project gantt charts in Python

![甘特图](https://github.com/netkiller/devops/raw/master/netkiller-gantt/doc/gantt.svg "Gantt chart")

# Python Gantt 工具

## 安装依赖

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

## 配置镜像

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

root@netkiller ~# cat /root/.config/pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装 netkiller-gantt 

```shell
pip install netkiller-gantt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 命令帮助

```bash
root@netkiller ~# gantt 

Usage: gantt [options] 

Options:
  -h, --help            show this help message and exit
  --stdin               cat gantt.json | gantt -s file.svg
  -c /path/to/gantt.csv, --csv=/path/to/gantt.csv
                        /path/to/gantt.csv
  -l /path/to/gantt.json, --load=/path/to/gantt.json
                        load data from file.
  -d, --debug           debug mode

  loading data from mysql:
    -H localhost, --host=localhost
    -u root, --username=root
    -p PASSWORD, --password=PASSWORD
    -D test, --database=test

  Charts:
    -t 项目甘特图, --title=项目甘特图
                        甘特图标题
    -W 5, --workweeks=5
                        workweeks default 5
    -g, --gantt         Gantt chart
    -w, --workload      Workload chart
    -s /path/to/gantt.svg, --save=/path/to/gantt.svg
                        save file

Homepage: https://www.netkiller.cn	Author: Neo <netkiller@msn.com>
```

# 生成甘特图

## 从标准输出载入json数据生成甘特图

准备 json 文件

```json
{
    "1": {
        "id": 1,
        "name": "开发需求排期",
        "start": "2023-02-22",
        "finish": "2023-03-03",
        "subitem": {
            "11": {
                "id": 11,
                "name": "用户登录开发",
                "start": "2023-02-22",
                "finish": "2023-02-24",
                "progress": 4,
                "resource": "陈景峰"
            },
            "12": {
                "id": 12,
                "name": "权限角色开发",
                "start": "2023-02-27",
                "finish": "2023-03-03",
                "resource": "Neo",
                "progress": 5,
                "predecessor": 11
            },
            "2": {
                "id": "2",
                "name": "测试任务排期",
                "start": "2023-03-01",
                "finish": "2023-03-15",
                "subitem": {
                    "21": {
                        "id": 21,
                        "name": "用户登陆测试",
                        "start": "2023-03-01",
                        "finish": "2023-03-08",
                        "resource": "陈景峰",
                        "progress": 4
                    },
                    "22": {
                        "id": 22,
                        "name": "权限角色测试",
                        "start": "2023-03-09",
                        "finish": "2023-03-15",
                        "resource": "netkiller",
                        "progress": 0,
                        "predecessor": 21
                    }
                }
            }
        }
    },
    "3": {
        "id": 3,
        "name": "任务组测试",
        "start": "2023-02-25",
        "finish": "2023-03-10",
        "resource": "陈景峰",
        "progress": 3,
        "subitem": {
            "4": {
                "id": 4,
                "name": "Java",
                "start": "2023-02-24",
                "finish": "2023-02-27",
                "resource": "司空摘星",
                "progress": 2
            },
            "5": {
                "id": 5,
                "name": "PHP",
                "start": "2023-03-03",
                "finish": "2023-03-15",
                "resource": "阿不都沙拉木",
                "progress": 5,
                "predecessor": 4,
                "subitem": {
                    "83": {
                        "id": 83,
                        "name": "V7.0",
                        "start": "2023-03-03",
                        "finish": "2023-03-05",
                        "predecessor": 82,
                        "subitem": {
                            "83": {
                                "id": 83,
                                "name": "V8.0",
                                "start": "2023-03-06",
                                "finish": "2023-03-10",
                                "predecessor": 82,
                                "subitem": {
                                    "83": {
                                        "id": 83,
                                        "name": "V8.5",
                                        "start": "2023-03-13",
                                        "finish": "2023-03-16",
                                        "predecessor": 82
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "6": {
                "id": "6",
                "name": "Go",
                "start": "2023-03-10",
                "finish": "2023-03-20",
                "milestone": true
            },
            "7": {
                "id": 7,
                "name": "Python",
                "start": "2023-03-06",
                "finish": "2023-03-08",
                "predecessor": 5
            },
            "8": {
                "id": 8,
                "name": "Swift",
                "start": "2023-02-27",
                "finish": "2023-03-16",
                "subitem": {
                    "81": {
                        "id": 81,
                        "name": "LLVM",
                        "start": "2023-02-28",
                        "finish": "2023-03-06",
                        "predecessor": 4
                    },
                    "82": {
                        "id": 82,
                        "name": "Clang",
                        "start": "2023-03-07",
                        "finish": "2023-03-10",
                        "predecessor": 81
                    },
                    "83": {
                        "id": 83,
                        "name": "Rust",
                        "start": "2023-03-13",
                        "finish": "2023-03-16",
                        "predecessor": 82
                    }
                }
            }
        }
    }
}
```

开始生成 Gantt 甘特图

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

从禅道导出 csv 文件

```sql
select id, parent, name,estStarted,deadline,assignedTo  from zt_task 
INTO OUTFILE '/tmp/project.csv'
FIELDS ENCLOSED BY '"'
TERMINATED BY ‘,’
ESCAPED BY '"'
LINES TERMINATED BY '\r\n';
```

命令行执行方法

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

如果导出指定的资源，可以通过查询 assignedTo 实现

```
select id, name,estStarted as start, deadline as finish,  assignedTo as resource, parent from zt_task where `group` = 4 order by id desc limit 100;
select id, name,estStarted as start, deadline as finish,  assignedTo as resource, parent from zt_task where assignedTo in ('neo','netkiller','tom','jerry') order by id desc limit 100;
```

## 从 MySQL 数据库生成甘特图

注意：MySQL 5.7 和 MySQL 8.0 有略微差别

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
  `milestone` bit(1) DEFAULT b'0' COMMENT '里程碑',
  `parent` bigint unsigned DEFAULT NULL COMMENT '父任务',
  PRIMARY KEY (`id`),
  KEY `project_has_subproject` (`parent`),
  KEY `task_has_predecessor_idx` (`predecessor`),
  CONSTRAINT `project_has_subproject` FOREIGN KEY (`parent`) REFERENCES `project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```

#### 插入测试数据

```sql
INSERT INTO `project` (`id`,`name`,`start`,`finish`,`resource`,`predecessor`,`milestone`,`parent`) VALUES (1,'任务组','2023-03-26','2023-04-10','小明',NULL,'0',NULL);
INSERT INTO `project` (`id`,`name`,`start`,`finish`,`resource`,`predecessor`,`milestone`,`parent`) VALUES (2,'任务A','2023-03-26','2023-03-29','小明',NULL,'0',1);
INSERT INTO `project` (`id`,`name`,`start`,`finish`,`resource`,`predecessor`,`milestone`,`parent`) VALUES (3,'任务B','2023-03-31','2023-04-01','小张',2,'0',1);
INSERT INTO `project` (`id`,`name`,`start`,`finish`,`resource`,`predecessor`,`milestone`,`parent`) VALUES (4,'任务C','2023-04-02','2023-04-08','小张',3,'0',1);
INSERT INTO `project` (`id`,`name`,`start`,`finish`,`resource`,`predecessor`,`milestone`,`parent`) VALUES (5,'里程碑','2023-04-06','2023-04-06',NULL,NULL,'1',NULL);
```

### bit(1) 类型数据更新注意事项

```sql
UPDATE `test`.`project` SET `milestone` = b'001'  WHERE (`id` = '11');
```

### 生成甘特图

```bash

gantt --host mysql.netkiller.cn -u root -p passw0rd --database test -g

```