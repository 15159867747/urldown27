# coding=utf-8
import mongoDB, math, pickle, time
from collections import defaultdict #可以直接使用下标访问二维字典不存在的元素
import sys, operator
from operator import itemgetter
#from numpy import rank
from time import sleep


class Recommend(object):
    def __init__(self):
        self.mongodb = mongoDB.MongoDB() #数据库操作器
        self.userItems = dict() #用户到物品的倒排表
        self.C = defaultdict(defaultdict) #用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict) #用户个数


    def _build_inver_table(self):
        doc = self.mongodb.varietyCol.find()
        count = 0
        for variety in doc:
            print count
            count += 1
            url = variety['url']
            if url not in self.userItems:
                self.userItems[url] = set()
            if variety['recommendUrls'] is None: #有些综艺没有推荐的url
                continue
            for i in variety['recommendUrls']:
                item = self.mongodb.search_book_by_url(i)
                #如果为“无效综艺”，舍弃
                if item is None:
                    continue
                self.userItems[url].add(i)
            print self.userItems[url]
            if count==3:
                break
        print self.userItems.items()
        print '-----'
        for u, items in self.userItems.items():#u ： 用户
            print items






    def _cal_corated_users(self):
        for u, items in self.userItems.items():#u ： 用户

            for i in items:                    #items：推荐的url（快乐大本营、天天向上...
                if i not in self.N.keys(): #如果一维字典中没有该键，初始化值为0
                    self.N[i] = 0 #N[快乐大本营]=0
                self.N[i] += 1 #N[快乐大本营]=1
                for j in items:
                    if i == j:
                        continue
                    if j not in self.C[i].keys(): #如果二维字典中没有该键，初始化值为0
                        self.C[i][j] = 0
                    self.C[i][j] += 1
        print self.C.items()
        for i, related_items in self.C.items(): #i 键  related_items 值
            for j, cij in related_items.items():
                print j,cij






    def cal_matrix_W(self):
        self.W.clear()
        print len(self.W)
        sleep(3)
        print 'build inver table...'
        self._build_inver_table()
        print 'cal corated users...'
        self._cal_corated_users()





if __name__ == '__main__':
    recommend = Recommend()
    #recommend._build_inver_table()
    recommend.cal_matrix_W()
    print 'all down!'



