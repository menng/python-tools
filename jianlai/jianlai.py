# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import os
import sys
from bs4 import BeautifulSoup
import requests
from dbutil import DbOperate, Dbconn
import logging
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'config.ini'), encoding="utf-8")
token = config.get("ServerChan", "token")
path = config.get("ServerChan", "url")
path_url = '%s%s.send?text=主人剑来更新啦~' % (path, token)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

def getChapterNo():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Host": "book.zongheng.com"}
    url = 'http://book.zongheng.com/book/672340.html'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.select(".book-new-chapter .tit a")[0].text
    chapter = title[1:(title.index(u'章'))]
    chapter_num = chinese2digits(chapter)
    logging.info("最新章节：%s", chapter_num)
    return chapter_num

def chinese2digits(chiness_chars):
    num_map = {u"零": 0, u"一": 1, u"二": 2 , u"三": 3, u"四": 4, u"五": 5, u"六": 6, u"七": 7, u"八": 8, u"九": 9, u"十": 10, u"百": 100, u"千": 1000, u"万": 10000}
    total = 0
    r = 1
    for i in range(len(chiness_chars) - 1, -1, -1):
        num = num_map.get(chiness_chars[i])
        if num >=10 and i == 0:
            if num > r:
                r = num
                total = total + num
            else:
                r = r * num
        elif num >= 10:
            if num > r:
                r = num
            else:
                r = r * num
        else:
            total = total + r * num
    return total

def getOldChapterNo():
    dbConn = Dbconn(config)
    dbOperate = DbOperate(dbConn.get_conn())
    return dbOperate.get_chapter()

def setChapterNo(chapterNo):
    dbConn = Dbconn(config)
    dbOperate = DbOperate(dbConn.get_conn())
    dbOperate.update_chapter(chapterNo)

def checkOrSaveChapterNo(chapterNo):
    old_no = getOldChapterNo()
    if old_no is None or chapterNo > old_no:
        response = requests.get(path_url)
        print(response.json())
        setChapterNo(chapterNo)
        logging.info("更新了，已通知")
    else:
        logging.info("未更新，不通知")

def job():
    current_no = getChapterNo()
    checkOrSaveChapterNo(current_no)
