#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import re
import xlsxwriter
import os
import numpy as np
from PIL import Image
import ast
from wordcloud import WordCloud

def drawWordCloud(words, title, imgpath, savepath='./results'):
   img_array = np.array(Image.open(imgpath))
   wc = WordCloud(font_path='simkai.ttf', background_color='white', mask=img_array, max_words=2000, width=1920, height=1080, margin=5)
   wc.generate_from_frequencies(words)
   wc.to_file(os.path.join(savepath, title+'.png'))



dict = {'科技迷':'20', '艺术家':'27', '大诗人':'14','玩机高手':'50','动漫狂热者':'10','历史学家':'8','生物学家':'18','画家':'34','建筑大师':'2',}



for sub in dict:
   dict[sub] = int(dict[sub])
img = 'triangle.png'
drawWordCloud(dict, '词云6', img, savepath='./results')
