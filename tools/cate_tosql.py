import os
import pymysql
import MySQLdb
import json
import re
import xlsxwriter

dict0 = {'财经':'经济', '彩票':'经济', '房产':'经济','股票':'经济','军事':'时政','政治':'时政','计算机':'科技','科技':'科技','社会':'生活','家居':'生活','星座':'生活','时尚':'生活','体育':'生活','娱乐':'娱乐','游戏':'娱乐','教育':'教育','历史':'文化','文化':'文化','艺术':'文化'}
dict1 = {'时政':'3','科技':'4','经济':'5','生活':'6','教育':'7','文化':'8','娱乐':'9'}
db = MySQLdb.connect("localhost", "root", "123456", "websitedb", charset='utf8' )
cursor = db.cursor()
corpus_path = "./save/"
catelist = os.listdir(corpus_path)  # 获取corpus_path下的所有子目录
for mydir in catelist:
    class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径如：train_corpus/art/
    file_list = os.listdir(class_path)  # 获取未分词语料库中某一类别中的所有
    for file_path in file_list:
        newid = file_path.replace(".txt", "")
        new_cate = dict1[dict0[mydir]]
        sql = "select * from new where new_id = '%s'" % (newid)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            print("没这个数据啊！")
        else:
            sql = "UPDATE new SET new_cate_id = %s WHERE new_id='%s'" % (new_cate,newid)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                print("cate提交失败")


db.close()
