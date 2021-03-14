import os
import pymysql
import MySQLdb
import json
import re
import xlsxwriter

db = MySQLdb.connect("localhost", "root", "123456", "websitedb", charset='utf8' )
cursor = db.cursor()
corpus_path = "./save/"
catelist = os.listdir(corpus_path)  # 获取corpus_path下的所有子目录
for mydir in catelist:
    class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径如：train_corpus/art/
    file_list = os.listdir(class_path)  # 获取未分词语料库中某一类别中的所有
    for file_path in file_list:
        newid = file_path.replace(".txt", "")
        sql = "select * from new_copy1 where new_id = '%s'" % (newid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            print("没这个数据啊！")
        else:
            sql = "select new_hot from newhot where new_id = '%s'" % (newid)
            cursor.execute(sql)
            hot_value = cursor.fetchone()
            sql_w = "insert into newtag( new_tag,new_id,new_hot ) values('%s', '%s' ,'%s')" % (mydir, newid, hot_value[0])
            try:
                cursor.execute(sql_w)
                db.commit()
            except:
                print("标签存储失败",mydir,newid, hot_value[0])
                db.rollback()

db.close()
