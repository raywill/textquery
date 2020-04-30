#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
#
# name: tq
# info: tq is a powerful text process engine with out-of-the-box SQL support
# author: hustos@qq.com
# version: v1.0
# date: April 30, 2020
#

from __future__ import print_function
from moz_sql_parser import parse
import sqlite3
import sys

BOM = b'\xef\xbb\xbf'
DB_PATH = '/tmp/data.db'

if len(sys.argv) < 2:
    print ("usage:%s \"select c1 from inputfile\"" % (sys.argv[0]))
    sys.exit(0)

userSql=sys.argv[1]
ast = parse(userSql)

def collectTableNames(ast):
    names = {}
    _collectTableNames(ast, names)
    return names

def resolveFrom(frm, names):
    if isinstance(frm, dict):
        for key in frm.keys():
            if key == 'value':
                names[frm['value']] = 0
            else:
                _collectTableNames(frm[key], names)
    elif isinstance(frm, list):
        for item in frm:
            #print item
            if isinstance(item, dict):
                if item.has_key('value'):
                    resolveFrom(item, names)
                else:
                    _collectTableNames(item, names)
            else:
                resolveFrom(item, names)
    else:
        names[frm] = 0

def _collectTableNames(ast, names):
    if isinstance(ast, dict):
        for key in ast.keys():
            if key in ['from', 'left join', 'join']:
                resolveFrom(ast[key], names)
            else:
                _collectTableNames(ast[key], names)
    elif isinstance(ast, list):
        for subAst in ast:
            _collectTableNames(subAst, names)
    else:
        pass


def buildQuestionMarks(count):
    # ?,?,?...
    return ",".join(["?" for n in range(1, count + 1)])

def buildCreateTableSql(tableName, columnCount):
    # c1,c2,c3....
    return "CREATE TABLE %s (%s)" % (tableName, ",".join(["c%d" % (n) for n in range(1, columnCount + 1)]))


conn = sqlite3.connect(DB_PATH)
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
cursor = conn.cursor()

fileNames = collectTableNames(ast)
for fileName in fileNames.keys():
    # stat max column size
    lines = open(fileName,'r').readlines()
    columnCount = 0
    for line in lines:
        items = line.strip('\n').strip('\r').split(',')
        columnCount = max(columnCount, len(items))

    # create table
    sql = "drop table if exists %s" % (fileName)
    cursor.execute(sql)
    sql = buildCreateTableSql(fileName, columnCount)
    cursor.execute(sql)

    insertSql = "INSERT INTO %s VALUES (%s)" % (fileName, buildQuestionMarks(columnCount))

    # load data into sqlite table
    for line in lines:
        items = line.strip('\n').strip('\r').strip(BOM).split(',')
        if (len(items) == 0 or len(items[0]) == 0): # skip empty line
            continue
	items.extend(['' for n in range(len(items), columnCount)])
        cursor.execute(insertSql, items)
    conn.commit()

# output sql result
cursor.execute(userSql)
result = cursor.fetchall()
for r in result:
    for v in r:
        print ("%s" % (v),end='')
    print ("")

conn.close()

