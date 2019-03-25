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
        self.userItems = dict() #用户到物品的倒排表 (user,url1、url2...)
        self.C = defaultdict(defaultdict) #用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict) #用户个数   N[节目]：喜欢该节目的人数
        self.W = defaultdict(defaultdict) #相似度矩阵
        self.W_max = dict()  # 记录每一列的最大值
        self.k = 20 #选取前k个最相似的物品计算预测相似度
        #初始化的时候需要载入物品相似度矩阵
        #self.load_matrix_w()

    def _build_inver_table(self):
        doc = self.mongodb.varietyColtest.find()
        count = 0
        for variety in doc:
            print count
            count += 1
            userid = variety['userid']
            if userid not in self.userItems:
                self.userItems[userid] = set()
            for i in variety['like']:
                self.userItems[userid].add(i)
            print self.userItems

        #     if count==3:
        #         break
        # print self.userItems.items()
        # print '-----'
        # for u, items in self.userItems.items():#u ： 用户
        #     print items







    def _cal_corated_users(self):
        for u, items in self.userItems.items():#u ： 用户
            print u
            for i in items:                    #items：推荐的url（快乐大本营、天天向上...
                #print i
                if i not in self.N.keys(): #如果一维字典中没有该键，初始化值为0 ，keys()返回所有键
                    self.N[i] = 0 #N[快乐大本营]=0   //例如i为快乐大本营，且只有该用户喜欢，即初始化为0
                self.N[i] += 1 #N[快乐大本营]=1      //自动加一，因为初始化为0，且该用户喜欢即加一

        for u, items in self.userItems.items():
            print u
            for i in items:
                for j in items:       #items：推荐的url（快乐大本营、天天向上...
                    if i == j:    #i=快乐大本营，j=快乐大本营
                        continue #j=天天向上
                    if j not in self.C[i].keys(): #如果二维字典中没有该键，初始化值为0 ，C[i]
                        self.C[i][j] = 0  #C[快乐大本营][天天向上]
                    self.C[i][j] += 1


        print 'C已计算完成'
        # for i, related_items in self.C.items(): #i 键  related_items 值
        #     #print i,related_items
        #     for j, cij in related_items.items():
        #         print j,cij


    def _cal_matrix_W(self):
        for i, related_items in self.C.items():
            for j, cij in related_items.items():
                self.W[i][j] = cij / math.sqrt(self.N[i] * self.N[j]) #余弦相似度
                #print '节目：'+i+'节目：'+j+'之间的相似度为：'+str(self.W[i][j])

    def _save_matrix_w(self):
        f = open('matrixWtest.txt', 'w')
        pickle.dump(self.W, f)
        f.close()

    def load_matrix_w(self): #载入大概需要7.96s
        f = open('matrixWtest.txt')
        self.W = pickle.load(f)
        f.close()

    def cal_matrix_W(self):
        self.W.clear()
        print len(self.W)
        sleep(3)
        print 'build inver table...'
        self._build_inver_table()
        print 'cal corated users...'
        self._cal_corated_users()
        print 'cal matrix W...'
        self._cal_matrix_W()
        print 'save matrix...'
        self._save_matrix_w()



    #基于物品的协同过滤算法，输入为综艺节目的urls，返回推荐的urls
    def itemCF(self, urls):
        rank = dict() #保存推荐的url及其对应的兴趣度
        for i,rating in urls:
            #print self.W[i]
            # variety = self.mongodb.search_variety_by_url(i)
            # interest = float(variety['score'])

            #print variety['varietyname']
            #j表示某物品，wj表示物品i和物品j的相似度
            #
            #key 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
            #reverse -- 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。
            for j, wj in sorted(self.W[i].items(), key=itemgetter(1), reverse=True)[0:self.k]:
                #print self.W[i]['']
                print j,wj
                #如果已经包含了物品j，跳过
                if j in urls:
                    continue
                #如果物品j是无效节目，跳过
                #根据评分和相似度计算物品j的预测兴趣度
                if j not in rank.keys():
                    rank[j] = 0
                rank[j] += wj*rating
                print  rank[j]
        print rank
        #按照兴趣度排序，返回推荐书籍的urls
        sorted_rank = sorted(rank.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10]
        print 'sorted:\n', sorted_rank
        res = []
        for i in sorted_rank:
            res.append(i[0])
        return res #只返回预测兴趣度前10的urls

    def maxW(self):
        i=1
        res = []
        while i<=20000:
            for j, wj in sorted(self.W[i].items(), key=itemgetter(1), reverse=True)[0:1]:
                print i,j,wj
                res.append(wj)
            i=i+1
        print res
if __name__ == '__main__':
    recommend = Recommend()
    # user=dict()
    # for i in recommend.mongodb.searchvariety(1):
    #     user[i]=recommend.mongodb.searchratings(1,i)
    # print user



    #recommend.maxW()
    #print recommend.W[9014][8736]
    # #print recommend.W
    #
    # recommend._build_inver_table()
    #recommend.cal_matrix_W()
    urls = []
    urls.append(100)

    #urls.append(8736)

    # print '用户收藏的综艺节目：'
    # for i in urls:
    #     variety= recommend.mongodb.search_variety_by_url(i)
    #     print variety['varietyname']
    # print '-----------------------------------------------'
    # print '根据用户收藏的综艺节目，推荐的列表：'
    #
    # for i in recommend.itemCF(urls):
    #     # variety = recommend.mongodb.search_variety_by_url(i)
    #     # interest = variety['varietyname']
    #     print i

    print 'all down!'



