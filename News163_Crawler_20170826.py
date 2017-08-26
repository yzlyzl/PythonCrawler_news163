# -*- coding: utf-8 -*-

# Content: 抓取网易新闻排行榜的新闻标题和链接，保存为.txt文件
# 创建时间: 20170826
# 最后修改时间: 20170826

import requests
import re
import os
import time

def Get_Index_Page_Info(page_str):
    """ 
        从含新闻排行榜首页的HTML代码str中获得各个分栏的名称和链接信息，
        存储在一个2-元组的列表中返回。
    """
    IndexPageInfoList = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', page_str, re.S)
    return IndexPageInfoList

def Get_Page_Info(page_str):
    """
        从含一个新闻分类的HTML代码str中获得各条热点新闻的名称和链接信息，
        存储在一个2-元组的列表中返回。        
    """
    PageInfoList = re.findall(r'<td class=".*?"><span>.*?</span><a href="(.*?)">(.*?)</a></td>', page_str, re.S)
    return PageInfoList

def Change_Info2txt(info_list, filename, save_path):
    """ 
        根据save_path创建.txt文件，
        将某类别的当日新闻标题和网址链接写入文件
    """
    with open(save_path + filename, 'w') as f:
        for info in info_list:
            f.write('%s\t\t%s\n' % (info[1], info[0]))


def Run(url):
    """  """
    # 从url获取首页各个新闻分类的名称和链接
    response = requests.get(url)
    content = response.content.decode('gbk')
    IndexPageInfoList = Get_Index_Page_Info(content)
    
    # 创建文件夹
    dir_name = u'网易新闻排行榜'
    dir_name_today = u'网易新闻_' + time.strftime('%Y%m%d')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    if not os.path.exists(dir_name + '/' + dir_name_today):
        os.mkdir(dir_name + '/' + dir_name_today)

    # 根据新闻分类循环处理每个分类页面的信息
    for item, link in IndexPageInfoList:
        filename = item + '_' + time.strftime('%Y%m%d') + '.txt'
        save_path = dir_name + '/' + dir_name_today + '/'
        page_content = requests.get(link).content.decode('gbk')
        PageInfoList = Get_Page_Info(page_content)
        Change_Info2txt(PageInfoList, filename, save_path)

        print (u'%s 处理完成' % item)


if __name__ == '__main__':
    url = 'http://news.163.com/rank/'
    print ('Start---------------------')
    Run(url)
    print ('Done--------------------——')