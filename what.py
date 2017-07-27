#!/usr/bin/python2.7  
# -*- coding:utf-8 -*-
import os
from string import Template 

className = 'Category'
fieldNames = [{'id': "number"}, {'parentId': "number"}, {'name': "string"}, {"description": "string"},{"commonId": "number"},{'creatorId': "number"}, {'createTime': "number"}, {"updatorId": 'number'}, {'updateTime': 'number'}, {'syncTime': 'number'}, {'disabled': 'number'}]
destDir = './'+className
classFileName = destDir + '/' + className + ".server.ts"
methodsCode = ''
classCode = ''
interfaceCode = ''

f = open('./method.shit', 'r')
fieldTempt = Template(f.read())
interfaceTempt = Template('    ${field}: ${type},\n')
classTempt= ''

for field in fieldNames:
    fName = field.keys()[0]
    FName = fName[0].upper() + fName[1: len(fName)]
    tName = field.values()[0]
    methodsCode += '\n' + fieldTempt.substitute(field=fName, type=tName, Field=FName)
    interfaceCode += interfaceTempt.substitute(field=fName, type=tName)
f = open('./class.shit', 'r')
classTempt = Template(f.read())
classCode = classTempt.substitute(className=className, methods=methodsCode, interface=interfaceCode)
f.close()

if True!=os.path.exists(destDir):
    os.mkdir(destDir)

f = open(classFileName, 'w')
f.write(classCode)
f.close()
print 'done~~~~~~, dir->', os.path.abspath(destDir)