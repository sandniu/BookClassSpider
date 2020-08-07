# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import time

import  logging
 
logger  = logging.getLogger(__name__)

userName = "book"
password = "book"
ipAddress = ""
port = 3306
dbName = ""
charset = "utf8"

class BookclassSpiderPipeline:
    mydb = None
    mycursor = None 
    guid = int(time.time())

     # 开启爬虫时执行，只执行一次
    def open_spider(self, spider):
        # spider.hello = "world"  # 为spider对象动态添加属性，可以在spider模块中获取该属性值
        # 可以开启数据库等

        self.mydb = pymysql.connect(host=ipAddress, port=port, user=userName,
                     password=password, db=dbName, charset=charset)
        self.mycursor = self.mydb.cursor()
        pass

    def reconnect_db(self):
        # 检查连接是否断开，如果断开就进行重连
        self.mydb.ping(reconnect=True) 


    # 关闭爬虫时执行，只执行一次。 (如果爬虫中间发生异常导致崩溃，close_spider可能也不会执行)
    def close_spider(self, spider):
        if self.mycursor :
            self.mycursor.close()
        if self.mydb:
            self.mydb.close()


     # 处理提取的数据(保存数据)
    def process_item(self, item, spider):
        print(item)
        self.guid = self.guid + 1
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = "insert into t_book_category_tmp(ID,LibraryClassficationID, CateLevel,ParentID,Name,CreateTime,UpdateTime) \
        values({},'{}',{},'{}','{}','{}','{}')".format(self.guid,item["code"],item["level"],item["pcode"],item["name"],now,now)
        print(sql)
        try:
             # 检查连接是否断开，如果断开就进行重连
            self.mydb.ping(reconnect=True)
            if self.mycursor:
                self.mycursor.execute(sql)
        except Exception as ex:
            print(ex)
            logger.error("process_item error:{}{}".format(ex,sql))
        self.mydb.commit()

        
