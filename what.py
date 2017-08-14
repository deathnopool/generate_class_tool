#!/usr/bin/python2.7  
# -*- coding:utf-8 -*-
import os
from string import Template 
import psycopg2
import json

configFile = open('config.json', 'r')
config = json.load(configFile, encoding='utf-8')

DATABASE = config['database']
USER = config['user']
PASSWORD = config['password']
HOST = config['host']
PORT = config['port']
SCHEMA = config['schema']
TABLE = config['table']
CLASS = config['class']
EXTENSION = config['extension']

conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
print 'connecting to database successful!'
cur = conn.cursor()
cur.execute('select COLUMN_NAME, DATA_TYPE from information_schema.columns where table_schema=\''+SCHEMA +'\' and table_name=\''+TABLE+ '\';')
rows = cur.fetchall()
conn.close()

className = CLASS
fieldNames = rows

destDir = './'+className
classFileName = destDir + '/' + className + EXTENSION
methodsCode = ''
classCode = ''
interfaceCode = ''
dataCode = ''

f = open('./method.shit', 'r')
fieldTempt = Template(f.read())
f = open('./data.shit', 'r')
dataTempt = Template(f.read())
interfaceTempt = Template('    ${field}: ${type},\n')
classTempt= ''

def translateType(t):
    if t == 'bigint' or t == 'integer':
        return 'number'
    elif t == 'character varying' or t == 'text':
        return 'string'
    return 'object'

def translateValue(t):
    if t=='number':
        return '0'
    elif t=='string':
        return '\'\''
    else:
        return '{}'

for field in fieldNames:
    fName = field[0]
    FName = fName[0].upper() + fName[1: len(fName)]
    tName = translateType(field[1])
    methodsCode += '\n' + fieldTempt.substitute(field=fName, type=tName, Field=FName)
    interfaceCode +=  interfaceTempt.substitute(field=fName, type=tName)
    dataCode += dataTempt.substitute(field=fName, defaultValue=translateValue(tName)) + '\n'
f = open('./class.shit', 'r')
classTempt = Template(f.read())
classCode = classTempt.substitute(className=className, methods=methodsCode, interface=interfaceCode, data=dataCode)
f.close()

if True!=os.path.exists(destDir):
    os.mkdir(destDir)

f = open(classFileName, 'w')
f.write(classCode)
f.close()
print 'done~~~~~~, dir->', os.path.abspath(destDir)