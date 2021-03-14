import requests
import json
from bs4 import BeautifulSoup
import urllib,re
from time import sleep
import xlsxwriter
import os
import math
import operator
from functools import reduce
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class baiduspider():
    
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        self.get_info()

   
    def get_good_url(self):
        url = "http://top.baidu.com/buzz?b=1&fr=topindex"
        return url


    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  
        new_title = re.sub(rstr, "", title)
        return new_title


    def get_info(self):
        name = '百度实时热点' + '.xlsx'
        if os.path.exists(name):
            os.remove(name)
        workbook = xlsxwriter.Workbook('百度实时热点' + '.xlsx') #创建新表
        worksheet = workbook.add_worksheet()
        #写入标题，粗体
        worksheet.write('A1', '排名')        #写入标题，粗体
        worksheet.write('B1', '标题')
        worksheet.write('C1', '链接')


        worksheet.set_column('A:A', 20)            #改变列宽度
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 50)

        row = 1
        col = 0

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options,executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.implicitly_wait(10)
        link = self.get_good_url()
        driver.get(link)
        driver.maximize_window()

        for x in range(1, 10, 1):
            height = float(x) / 10
            js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * %f" % height
            driver.execute_script(js)
            sleep(0.5)
        html = driver.page_source
        # 创建Beautiful对象
        soup = BeautifulSoup(html,'lxml')            

        ranks = soup.find_all('td',attrs={'class': "first"})
        titles = soup.find_all(class_="keyword")


        for rank, title in zip(ranks, titles):
            data = {
                'rank' :   rank.text.strip(),
                'title' :   title.find_all('a')[0].text.strip(),
                'link'  :   title.find_all('a')[0].get("href")
                }

            key1 = self.validateTitle(data['title'])
            key1 = ''.join(key1.split())

            worksheet.write(row, col, data['rank'])    #写入数据
            worksheet.write(row, col+1, data['title'])
            worksheet.write(row, col+2, data['link'])
            print("爬取成功")
            row += 1
        sleep(1)
        driver.quit()
        workbook.close()
if __name__ == '__main__':
    a=baiduspider()

