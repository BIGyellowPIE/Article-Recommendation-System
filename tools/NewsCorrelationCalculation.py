# -*- coding: utf-8 -*-
import os
import pymysql
import collections

class Correlation:
    def __init__(self, file):
        self.db = self.connect()
        self.cursor = self.db.cursor()

        self.file = file
        self.news_tags = self.loadData()
        self.news_cor_list = self.getCorrelation()

    # 连接mysql数据库
    def connect(self):
        db = pymysql.Connect("localhost", "root", "123456", "websitedb", charset='utf8')
        return db

    # 加载数据
    def loadData(self):
        print("开始加载文件数据：%s" % self.file)
        news_tags = collections.OrderedDict()
        for line in open(self.file, "r", encoding="utf-8").readlines():
            try:
                newid, newtags = line.strip().split("\t")
                news_tags[newid] = newtags
            except:
                print("读取分词数据过程中出现错误，错误行为：{}".format(line))
                pass
        return news_tags

    # 计算相关度
    def getCorrelation(self):
        news_cor_list = list()
        new_val = list(self.news_tags.values())
        new_key = list(self.news_tags.keys())
        for i in range(len(new_key)):
            id1_tags = set(new_val[i].split(","))
            for j in range(i+1,len(new_key)):
                id2_tags = set(new_val[j].split(","))
                print( new_key[i] + "\t" + new_key[j] + "\t" + str(id1_tags & id2_tags) )
                cor = ( len(id1_tags & id2_tags) ) / len (id1_tags | id2_tags)
                if cor > 0.0:
                    news_cor_list.append([new_key[i],new_key[j],format(cor,".2f")])
                    news_cor_list.append([new_key[j],new_key[i],format(cor,".2f")])
        return news_cor_list

    # 将相似度数据写入数据库
    def writeToMySQL(self):
        for row in self.news_cor_list:
            sql_w = "insert into newsim_copy1( new_id_base,new_id_sim,new_correlation ) values('%s', '%s' ,'%s')" % (row[0], row[1], row[2])
            try:
                self.cursor.execute(sql_w)
                self.db.commit()
            except:
                print("rollback", row)
                self.db.rollback()
        print("相似度数据写入数据库：newsrec.newsim")

if __name__ == "__main__":
    # 原始数据文件路径
    original_data_path = "./key_word/"
    files = os.listdir(original_data_path)
    for file in files:
        print("开始计算文件 %s 下的新闻相关度。" % file)
        cor = Correlation(original_data_path + file)
        cor.writeToMySQL()
    print("\n相关度计算完毕，数据写入路径 /correlation")
