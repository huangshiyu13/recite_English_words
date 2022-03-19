# -*- coding: utf-8 -*-
# 读入有道词典生词本和词频单词本，输出含有音标，解释的详细版单词本
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xlrd
import xlwt
import xlutils
from xlwt import *
from xlutils.copy import copy
from utils import set_style

def read_xml(in_path):
    """读取并解析xml文件
       in_path: xml路径
       return: tree"""
    tree = ET.parse(in_path)
    return tree

def creat_dict(root):
    """xml生成为dict：，
    将tree中个节点添加到list中，将list转换为字典dict_init
    叠加生成多层字典dict_new"""
    dict_new = {}
    for key, valu in enumerate(root):
        dict_init = {}
        list_init = []
        for item in valu:
            list_init.append([item.tag, item.text])
            for lists in list_init:
                dict_init[lists[0]] = lists[1]
        dict_new[key] = dict_init
    return dict_new

if __name__ == '__main__':
    in_excel = 'world_list_original.xlsx'
    in_xml = 'youdao.xml'

    out_excel = 'word_list.xlsx'

    # read xml
    tree = read_xml(in_xml)
    word_dict = creat_dict(tree.getroot())  # 将xml转换为dict
    print('word number:',len(word_dict)) 
    word_dict_new = {}
    for key in word_dict:
        word_dict_now = word_dict[key]
        word = word_dict_now['word']
        trans = word_dict_now['trans']
        phonetic = word_dict_now['phonetic']
        word_dict_new[word] = {'trans':trans,'phonetic':phonetic}

    # read excel
    rb = xlrd.open_workbook(in_excel)
    table = rb.sheets()[0]
    nrows = table.nrows

    #write excel
    wb = xlwt.Workbook() #创建工作簿
    # wb = copy(rb)
    sheet = wb.add_sheet('coca20000',cell_overwrite_ok=True) #创建sheet
    my_style = set_style('Times New Roman',220,True)
    sheet.write(0,0,'Rank',my_style)
    sheet.write(0,1,'Word',my_style)
    sheet.write(0,2,'Phonetic',my_style)
    sheet.write(0,3,'Definition',my_style)
    sheet.write(0,4,'Description',my_style)

    for row_index in range(1,nrows):
        row_data = table.row_values(row_index)
        sheet.write(row_index,0,row_index)
        sheet.write(row_index,1,row_data[1])
        sheet.write(row_index,3,row_data[2])
        if row_data[1] in word_dict_new:
            word_now = word_dict_new[row_data[1]]
            sheet.write(row_index,2,word_now['phonetic'])     
            sheet.write(row_index,4,word_now['trans'])
    
    row_index+=1
    for word in word_dict_new:
        if word not in table.col_values(1):
            sheet.write(row_index,0,row_index)
            sheet.write(row_index,1,word)
            word_now = word_dict_new[word]
            sheet.write(row_index,2,word_now['phonetic'])     
            sheet.write(row_index,4,word_now['trans'])
            row_index += 1
    print('Total word number:',row_index)
    wb.save(out_excel) #保存文件

    # wb = copy(rb)
    # ws = wb.get_sheet(0)
    # wb.save(out_excel)

    
    	