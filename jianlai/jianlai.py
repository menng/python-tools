# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import os
from bs4 import BeautifulSoup
import requests
import schedule

CHAPTER_NUM_TXT = os.path.join(os.path.split(os.path.realpath(__file__))[0], "chapter_num.txt")

def getChapterNo():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Host": "book.zongheng.com"}
    url = 'http://book.zongheng.com/book/672340.html'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.select(".book-new-chapter .tit a")[0].text
    chapter = title[1:(title.index(u'章'))]
    print(chapter)
    chapter_num = chinese2digits(chapter)
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
    print(total)
    return total

def getOldChapterNo():
    if os.path.exists(CHAPTER_NUM_TXT):
        with open(CHAPTER_NUM_TXT, "r") as f:
            f = open(CHAPTER_NUM_TXT, "r")
            return int(f.readline())
    else:
        return None

def setChapterNo(chapterNo):
    with open(CHAPTER_NUM_TXT, "w") as f:
        f.write(str(chapterNo))

def checkOrSaveChapterNo(chapterNo):
    old_no = getOldChapterNo()
    if old_no is None or chapterNo > old_no:
        response = requests.get("https://sc.ftqq.com/xxxxxx.send?text=主人剑来更新啦~")
        print(response.json())
        setChapterNo(chapterNo)
        print("更新，已通知")
    else:
        response = requests.get("https://sc.ftqq.com/xxxxxx.send?text=主人剑来未更新啦~")
        print("未更新，不通知")

def job():
    # print(chinese2digits("一百一十"))
    current_no = getChapterNo()
    checkOrSaveChapterNo(current_no)

schedule.every().hour.do(job)

if __name__ == "__main__":
    job()
    while True:
        schedule.run_pending()

    
  