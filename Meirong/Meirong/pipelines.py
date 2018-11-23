# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import pymysql
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "sminuo2018",
        charset = "utf8",
        use_unicode = False
    )
    return conn

class MeirongPipeline(object):
    def __init__(self):
        self.file = codecs.open('baixing.json', 'w', encoding='utf-8')
        self.file.write('[')
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE scrapy")

        isphone = "select 1 from meirong where phone='"+item['phone']+"' limit 1"
        cursor.execute(isphone)
        resisphone = cursor.fetchone()

        if resisphone is None:
            sql = "INSERT INTO meirong(title,phone) VALUES(%s,%s)"
            try:
                cursor.execute(sql,(item['title'],item['phone']))
                cursor.connection.commit()
            except BaseException as e:
                print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
                dbObject.rollback()
            return item
        
    def spider_closed(self, spider):
        self.file.close()
