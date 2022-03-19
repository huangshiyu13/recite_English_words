# -*- coding: utf-8 -*-
# 生成每天需要背的单词，同时画出背诵曲线

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import xlrd
import xlsxwriter
import xlutils
from xlwt import *
from xlutils.copy import copy
import time
from utils import set_style,check_file
from utils import IGNORE, get_date_diff
# import matplotlib
# matplotlib.use('TkAgg')

def draw_log(lines):
    import matplotlib.pyplot as plt

    date = []
    values = []
    solid_values = []
    for line in lines:
        line = line.strip().split(':')
        date.append(line[0])
        values.append(int(line[1]))
        solid_values.append(int(line[2]))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.title('words')
    line1 = ax.plot(date, values, 'go-')
    line2 = ax.plot(date, solid_values, 'yo-')
    ax.set_ylabel('date')
    ax.set_ylabel('words number')

    ax2 = ax.twinx()
    line3 = ax2.plot(date, [1. if v == 0 else float(s)/v for v, s in zip(values,solid_values)], 'ro-')
    ax2.set_ylabel('rate')

    plt.gcf().autofmt_xdate()

    lns = line1+line2+line3
    ax.legend(lns, ['all_number:{}'.format(values[-1]),
        'remembered:{}'.format(solid_values[-1]),
        'remember rate:{}%'.format( int(10000*float(solid_values[-1])/values[-1])/100.)], loc=3)

    # plt.show()
    # exit()
    plt.savefig('u_log.png')

def get_rowindex(log_file,word_per_day):
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if not check_file(log_file):
        print('Can\'t find the log file, create {} now!'.format(log_file))
        row_index = 0
    else:
        f_in = open(log_file,'r')
        lines = f_in.readlines()
        draw_log(lines)
        row_index = int(lines[-1].strip().split(':')[1])
        day_before = lines[-1].strip().split(':')[0]
        f_in.close()
        if today == day_before:
            print('You have generate the file today!')
            exit()
            # return row_index-word_per_day
    return row_index

def write_log(log_file,row_now,solid_number):
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    f_out = open(log_file,'a')
    f_out.write('{}:{}:{}\n'.format(today,row_now,solid_number))
    f_out.close()

if __name__ == '__main__':  
    word_num_per_day = 50
    log_file = 'u_log.txt'
    

    row_index = get_rowindex(log_file,word_num_per_day)
    
    print('row_index:',row_index)
    in_excel = 'word_list.xlsx'
    out_excel = u'每日单词表.xlsx'
    ignore_word_file = 'ignore_words.txt'

    ignore = IGNORE(ignore_word_file)
    
    if check_file(out_excel):
        ignore.update_from_once_excel(out_excel)
    
    ignore.save()

    rb = xlrd.open_workbook(in_excel)
    in_sheet = rb.sheets()[0]

    nrows = in_sheet.nrows

    wb = xlsxwriter.Workbook(out_excel) #创建工作簿
    # wb = copy(rb)
    sheet = wb.add_worksheet('new_words') #创建sheet
    
    sheet.write(0,0,'Mark')
    sheet.write(0,1,'Rank')
    sheet.write(0,2,'Word')
    sheet.write(0,3,'Phonetic')
    sheet.write(0,4,'Definition')
    sheet.write(0,5,'Description')

    for i in range(word_num_per_day):
        row_data = in_sheet.row_values(row_index+i+1)
        for j in range(5):
            sheet.write(i+1,j+1,row_data[j])

    # sheet.col(0).width = 256*5
    # sheet.col(2).width = 256*25
    # sheet.col(3).width = 256*80
    sheet.set_column('A:A', 5)
    sheet.set_column('B:B', 5)
    sheet.set_column('C:C', 15)
    sheet.set_column('D:D', 30)
    sheet.set_column('E:E', 80)
    sheet.set_column('F:F', 80)
    sheet.freeze_panes(1, 0)

    wb.close()

    write_log(log_file,row_index+word_num_per_day,ignore.get_number())