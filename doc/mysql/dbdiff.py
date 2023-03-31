#!/usr/bin/python
# -*- coding: UTF-8 -*-

# from distutils.sysconfig import get_python_lib
# print(get_python_lib())

import mysql.connector
from mysql.connector import FieldType
from mysql import (connector)
from mysql.connector import errorcode


class MySQL:
    conn = None

    def __init__(self, config=None):
        if config:
            self.config = config
            self.connect(self.config)
            # self.config['user'] = config['user']
            # self.config['password'] = config['password']
            # self.config['host'] = config['host']
            # self.config['port'] = config['host']
            # self.config['database'] = config['database']
        pass

    def connect(self, config):
        try:
            self.conn = connector.connect(**config)

        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                # print("Something is wrong with your user name or password")
                print(err)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist: %s" % config['database'])
            else:
                print(err)
            exit()
        # else:
    def close(self):
        self.conn.close()

    def showDatabases(self):
        self.cursor = self.conn.cursor()
        query = "show databases;"
        self.cursor.execute(query)
        dbs = list([tuple[0] for tuple in self.cursor.fetchall()])
        self.cursor.close()
        for db in ['information_schema', 'mysql', 'performance_schema', 'sys']:
            dbs.remove(db)
        # print(dbs)
        return dbs

    def showTables(self):
        self.cursor = self.conn.cursor()
        query = "show tables;"
        self.cursor.execute(query)
        tables = [tuple[0] for tuple in self.cursor.fetchall()]
        # print(tables)
        # self.cursor.execute("SELECT table_name FROM information_schema.tables;")
        # myresult = self.cursor.fetchall()
        # for x in myresult:
        # print(x)
        self.cursor.close()
        return tables

    def describe(self, table):
        self.cursor = self.conn.cursor()
        self.cursor.execute("describe %s" % (table))

        # self.cursor.execute("SELECT * FROM %s LIMIT 1" % (table))
        # rows = self.cursor.fetchall()
        #
        # for desc in self.cursor.description:
        #     colname = desc[0]
        #     coltype = desc[1]
        #     print("Column {} has type {}".format(colname,
        #                                          FieldType.get_info(coltype)))
        desc = self.cursor.fetchall()
        self.cursor.close()
        return (desc)

    def showCreateTable(self, table):
        self.cursor = self.conn.cursor()
        # SET SQL_QUOTE_SHOW_CREATE=0;
        self.cursor.execute("show create table %s" % (table))
        rows = self.cursor.fetchone()
        self.cursor.close()
        # print(rows[1])
        return (rows[1])

    def showIndexs(self, table):
        self.cursor = self.conn.cursor()
        self.cursor.execute("SHOW INDEXES FROM  %s" % (table))
        lists = self.cursor.fetchall()
        indexs = [{
            'Non_unique': column[1],
            'Key_name': column[2],
            'Column_name': column[4],
            'Comment': column[9]
        } for column in lists]
        self.cursor.close()
        return (indexs)

    def execute(self, sql):
        self.cursor = self.conn.cursor()
        try:
            # print("Creating table {}: ".format(table_name), end='')
            self.cursor.execute(sql)
        except connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
            return (False)
        else:
            return (True)


class Load(MySQL):

    def __init__(self, config):
        super().__init__(config)
        pass

    def database(self):
        return self.showDatabases()

    def table(self):
        return self.showTables()

    def index(self, table):
        return self.showIndexs(table)


class Source(Load):

    def __init__(self, config):
        super().__init__(config)


class Target(Load):

    def __init__(self, config) -> None:
        super().__init__(config)


class MySQLDiff:

    def __init__(self) -> None:
        self.source = Source({
            'user': 'root',
            'password': 'chen',
            'host': '127.0.0.1',
            'database': 'test',
        })
        self.target = Target({
            'user': 'root',
            'password': 'chen',
            'host': '127.0.0.1',
            'database': 'test1',
        })

    def string(self, tmp):
        return tmp.decode('utf-8')

    def diffDatabaseAll(self):
        print(
            set(self.source.database()).difference(set(
                self.target.database())))

    def diffTableAll(self):
        print(set(self.source.table()).difference(set(self.target.table())))

    def diffTable(self, table):
        if table in self.source.table() and table in self.target.table():
            print(
                set(self.source.describe(table)).difference(
                    set(self.target.describe(table))))

    def diffIndex(self, table):
        sources = self.source.index(table)
        targets = self.target.index(table)
        # print(sources - targets)

    def margeTable(self, table=None, execute=False, delete_source=False):
        ddls = []
        if table in self.source.table() and table in self.target.table():

            sources = self.source.describe(table)
            targets = self.target.describe(table)

            sourceFields = [tuple[0] for tuple in sources]
            targetFields = [tuple[0] for tuple in targets]

            after = ''

            for field, type, null, key, default, extra in sources:

                if field not in targetFields:
                    # print(field)
                    # print(targets)
                    if sourceFields.index(field) > 0 and sourceFields[
                            sourceFields.index(field) - 1]:
                        after = "AFTER %s" % sourceFields[
                            sourceFields.index(field) - 1]
                    else:
                        after = "FIRST"
                    # print(after)

                    if null == 'NO':
                        null = 'NOT NULL'
                    else:
                        null = ''
                    if default == None:
                        default = ''
                    else:
                        default = 'DEFAULT %s' % default

                    if key == 'PRI':
                        ddl = "ALTER TABLE `{schema}`.`{table}` ADD COLUMN `{field}` {type} {null} {extra} {after}, ADD PRIMARY KEY (`{field}`);".format(
                            schema=self.target.config['database'],
                            table=table,
                            field=field,
                            type=self.string(type),
                            null=null,
                            extra=extra,
                            after=after)
                    else:
                        uni = ''
                        if key == 'UNI':
                            uni = ", ADD UNIQUE INDEX `{field}_UNIQUE` (`{field}` ASC) VISIBLE".format(
                                field=field)
                        ddl = "ALTER TABLE `{schema}`.`{table}` ADD COLUMN `{field}` {type} {null} {default} {extra} {after} {uni};".format(
                            schema=self.target.config['database'],
                            table=table,
                            field=field,
                            type=self.string(type),
                            null=null,
                            default=default,
                            extra=extra,
                            after=after,
                            uni=uni)
                    ddls.append(ddl)

            targets = self.target.describe(table)
            changes = [tuple[0] for tuple in set(sources).difference(targets)]
            # print(sources)
            # print(changes)
            for change in changes:
                field, type, null, key, default, extra = sources[
                    sourceFields.index(change)]
                # print(sourceFields.index(change))
                # print(field)
                if null == 'NO':
                    null = 'NOT NULL'
                else:
                    null = ''
                if default == None:
                    default = ''
                else:
                    default = 'DEFAULT %s' % default
                ddl = "ALTER TABLE `{schema}`.`{table}` CHANGE COLUMN {field} {field} {type} {null} {default} {extra};".format(
                    schema=self.target.config['database'],
                    table=table,
                    field=field,
                    type=self.string(type),
                    null=null,
                    default=default,
                    extra=extra)
                ddls.append(ddl)

            if delete_source:
                deletes = [
                    tuple[0] for tuple in set(targets).difference(sources)
                ]
                for delete in deletes:
                    ddl = "ALTER TABLE `{schema}`.`{table}` DROP COLUMN `{column}`;".format(
                        schema=self.target.config['database'],
                        table=table,
                        column=delete)
                    ddls.append(ddl)
                # print(deletes)

        elif table in self.source.table():
            ddl = self.source.showCreateTable(table)
            ddls.append(ddl)
            # self.target.execute(ddl)
        if execute:
            for ddl in ddls:
                print(ddl)
                self.target.execute(ddl)
        else:
            print("\n".join(ddls))
    def mergeIndex(self, table, execute=False):
        ddls = []
        if table in self.source.table() and table in self.target.table():
            sources = self.source.index(table)
            targets = self.target.index(table)
            for source in sources:
                if source['Key_name'] == 'PRIMARY':
                    continue
                column = source['Column_name']

                print(source)
                for target in targets:
                    # print(target[column])
                    if target.get(column) == None :
                        unique = ''
                        if source['Non_unique'] == 0 :
                            unique = 'UNIQUE'

                        ddl = "CREATE {unique} INDEX `idx_{table}_{column}`  ON `{schema}`.`{table}` ({column}) COMMENT '{comment}' ALGORITHM DEFAULT LOCK DEFAULT;".format(
                            unique =unique,
                            schema=self.target.config['database'],
                            table=table,
                            column=column,
                            comment=source['Comment'])
                        ddls.append(ddl)
            # diffs = set(sources).difference(targets)
            # print(sources)
            # print(targets)
            # 

        if execute:
            for ddl in ddls:
                print(ddl)
                self.target.execute(ddl)
        else:
            print("\n".join(ddls))

config = {
    'user': 'root',
    'password': 'chen',
    'host': '127.0.0.1',
    'database': 'test',
    #   'raise_on_warnings': True
}
mysql = MySQL(config)
# mysql.showDatabases()
# mysql.showTables()
# mysql.describe('employees')
# mysql.showCreateTable('employees')
# print(mysql.showIndexs('employees'))

mySQLDiff = MySQLDiff()
# (mySQLDiff.diffDatabaseAll())
# (mySQLDiff.diffTableAll())
# mySQLDiff.diffTable('employees')
# mySQLDiff.margeTable('employees', True)
# mySQLDiff.diffIndex('employees')
mySQLDiff.mergeIndex('employees')
