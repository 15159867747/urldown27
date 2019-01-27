#-*-coding:UTF-8-*-
'''
Created on 2016年4月27日
 @author: moverzp
 description: mongoDB相关的操作，替代原先的url管理器和html输出器
'''
import sys
import pymongo
from pyExcelerator import *

reload(sys)
sys.setdefaultencoding('utf-8')

class MongoDB(object):
    def __init__(self):
        #client = pymongo.MongoClient('localhost', 27017) #连接服务器
        client = pymongo.MongoClient('localhost')
        db = client['VarietyShows'] #选择数据库
        self.newUrlsCol = db.newUrls #选择集合newUrls
        self.oldUrlsCol = db.oldUrls #选择集合oldUrls
        self.varietyCol = db.variety #选择集合variety
        self.notFoundUrls = db.notFoundUrls #选择集合notFoundUrls
        self.userCol = db.user #选择集合user

    #url管理器功能
    #保存一个新的url
    def add_new_url(self, url):
        if url is None:
            return
        #只有既不在未爬取集合，也不在已爬取集合，才加入该url
        if self.newUrlsCol.find({'url':url}).count() == self.oldUrlsCol.find({'url':url}).count() == 0:
            self.newUrlsCol.insert({'url': url})
    #在一堆url中取新的url进行保存    1
    def add_new_urls(self, urls, data):
        if urls is None or len(urls) == 0:
            return
        if data is None: #舍弃书籍的推荐url也舍弃
            return
        for url in urls:
            self.add_new_url(url)
    #强制加入一个新的url
    def add_new_url_forcibly(self, url):
        self.oldUrlsCol.remove({'url': url})
        self.newUrlsCol.insert({'url': url})

    def has_new_url(self):
        return self.newUrlsCol.find().count() != 0

    def get_new_url(self):
        urlDoc = self.newUrlsCol.find_one()
        self.newUrlsCol.remove(urlDoc)
        self.oldUrlsCol.insert(urlDoc)
        return urlDoc['url']

    def add_404_url(self, url):
        self.notFoundUrls.insert({'url':url})

    #html输出器功能
    def collect_data(self, data,recommendUrls):
        if data is None:
            return
        data['recommendUrls'] = recommendUrls
        self.varietyCol.insert(data)

    def get_user_docs(self):
        doc = self.userCol.find()
        return doc

    def add_data_to_user(self, data):
        #需要防止反复添加同一节目
        if 0 == self.userCol.find({'url':data['url']}).count():
            self.userCol.insert(data)
    def remove_data_from_user(self, url):
        self.userCol.remove({'url':url})

    def search_book_by_url(self, url):
        doc = self.varietyCol.find_one({'url':url}) #正常情况下url唯一
        return doc

if __name__ == "__main__":
    rootUrl = "https://book.douban.com/subject/1477390/"
    mdb=MongoDB()
    mdb.add_new_url(rootUrl)



