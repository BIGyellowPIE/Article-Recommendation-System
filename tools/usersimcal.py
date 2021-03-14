# -*- coding: utf-8 -*-

import os
import MySQLdb
import json
import re
import xlsxwriter
import numpy as np
import ast

def pearson(p,q):
#只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same +=1
    n = same
    #分别求p，q的和
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    #分别求出p，q的平方和
    sumxsq = sum([p[i]**2 for i in range(n)])
    sumysq = sum([q[i]**2 for i in range(n)])
    #求出p，q的乘积和
    sumxy = sum([p[i]*q[i] for i in range(n)])
    # print sumxy
    #求出pearson相关系数
    up = sumxy - sumx*sumy/n
    down = ((sumxsq - pow(sumxsq,2)/n)*(sumysq - pow(sumysq,2)/n))**.5
    #若down为零则不能计算，return 0
    if down == 0 :return 0
    r = up/down
    return r

db = MySQLdb.connect("localhost", "root", "123456", "websitedb", charset='utf8' )
cursor = db.cursor()

sql =  "select * from login_user_info a where a.read > 10 "
cursor.execute(sql)
result = cursor.fetchall()
users_cor_list = list()
end = len(result)-1
print(end)
for i in range(end):
    user_dict1 = ast.literal_eval(result[end-i][5])
    for sub in user_dict1:
       user_dict1[sub] = int(user_dict1[sub])
    user1 = list(user_dict1.values())
    for j in range(end-i):
        user_dict2 = ast.literal_eval(result[j][5])
        for sub in user_dict2:
           user_dict2[sub] = int(user_dict2[sub])
        user2 = list(user_dict2.values())
        cor = pearson(user1,user2)
        print(cor)
        if cor > -1.0:
            users_cor_list.append([result[end-i][1],result[j][1],format(cor,".2f")])
            users_cor_list.append([result[j][1],result[end-i][1],format(cor,".2f")])

sql = """truncate table usersim"""
try:
   cursor.execute(sql)
   db.commit()
   print("delete successfully!")
except:
   db.rollback()
for row in users_cor_list:
    sql_w = "insert into usersim( user_id_base,user_id_sim,user_correlation ) values('%s', '%s' ,'%s')" % (row[0], row[1], row[2])
    try:
        cursor.execute(sql_w)
        db.commit()
    except:
        print("rollback", row)
        db.rollback()
print("相似度数据写入数据库：usersim")
            






