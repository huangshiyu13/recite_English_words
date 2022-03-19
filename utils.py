# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xlrd
import xlwt
import xlutils
from xlwt import *
from xlutils.copy import copy
import time
import os


def get_date_diff(start_str, end_str):
    import datetime
    start = datetime.datetime.strptime(start_str, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_str, '%Y-%m-%d')
    diff = end - start
    return diff.days

class IGNORE():
    def __init__(self,ignore_word_file):
        self.ignore_word_file = ignore_word_file
        self.self_load()

    def self_load(self):
        self.indexes = []
        self.words = []

        if check_file(self.ignore_word_file):
            f = open(self.ignore_word_file,'r')        
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                ls = line.split('_')
                self.indexes.append(int(ls[0]))
                self.words.append(ls[1])
            f.close()

    def update_from_excel(self,excel_file):
        rb = xlrd.open_workbook(excel_file)
        sheet = rb.sheets()[1]
        nrows = sheet.nrows
        for i in range(1,nrows):
            line = sheet.row_values(i)
            if line[0] != '' and line[0] != ' ' and int(line[0]) == 1 and line[1] not in self.indexes:
                self.indexes.append(int(line[1]))
                self.words.append(line[2])

    def update_from_once_excel(self,excel_file):
        rb = xlrd.open_workbook(excel_file)
        sheet = rb.sheets()[0]
        nrows = sheet.nrows
        for i in range(1,nrows):
            line = sheet.row_values(i)
            if line[0] != '' and line[0] != ' ' and int(line[0]) == 1 and line[1] not in self.indexes:
                self.indexes.append(int(line[1]))
                self.words.append(line[2])

    def save(self,save_file=None):
        if save_file == None:
            save_file = self.ignore_word_file
        
        # for index,word in sorted(zip(self.indexes,self.words),key= lambda x: x[0]):
        #     print(index)

        # exit()
        f = open(save_file,'w')

        for index,word in sorted(zip(self.indexes,self.words),key= lambda x: x[0]):
            f.write('{}_{}\n'.format(index,word))
        f.close()

    def get_number(self):
        return len(self.words)


def set_style(name,height,bold=False,bd_left=1):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.colour_index = 0
    font.height = height
    style.font = font
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    style.alignment = alignment

    
    pattern = Pattern()                 # 创建一个模式                                        
    pattern.pattern = Pattern.SOLID_PATTERN     # 设置其模式为实型              
    # 设置单元格背景颜色 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta
    pattern.pattern_fore_colour = 1        
    style.pattern = pattern

    b_c = 1
    borders = Borders()                                         
    borders.left = bd_left                                           
    borders.right = b_c                                           
    borders.top = b_c                                            
    borders.bottom = b_c                                          
    style.borders = borders
    return style

def check_file(filename):
    return os.path.isfile(filename)