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
        self.k = 20 #选取前k个最相似的物品计算预测相似度
        #初始化的时候需要载入物品相似度矩阵
        self.load_matrix_w()

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
                item = self.mongodb.search_variety_by_url(i)
                #如果为“无效综艺”，舍弃
                if item is None:
                    continue
                self.userItems[url].add(i)
            print self.userItems[url]
            '''if count==3:
                break
        print self.userItems.items()
        print '-----'
        for u, items in self.userItems.items():#u ： 用户
            print items'''






    def _cal_corated_users(self):
        for u, items in self.userItems.items():#u ： 用户

            for i in items:                    #items：推荐的url（快乐大本营、天天向上...
                if i not in self.N.keys(): #如果一维字典中没有该键，初始化值为0 ，keys()返回所有键
                    self.N[i] = 0 #N[快乐大本营]=0   //例如i为快乐大本营，且只有该用户喜欢，即初始化为0
                self.N[i] += 1 #N[快乐大本营]=1      //自动加一，因为初始化为0，且该用户喜欢即加一
                for j in items:       #items：推荐的url（快乐大本营、天天向上...
                    if i == j:    #i=快乐大本营，j=快乐大本营
                        continue #j=天天向上
                    if j not in self.C[i].keys(): #如果二维字典中没有该键，初始化值为0 ，C[i]
                        self.C[i][j] = 0  #C[快乐大本营][天天向上]
                    self.C[i][j] += 1
        '''print self.C.items()
        for i, related_items in self.C.items(): #i 键  related_items 值
            #print i,related_items
            for j, cij in related_items.items():
                print j,cij'''


    def _cal_matrix_W(self):
        for i, related_items in self.C.items():
            for j, cij in related_items.items():
                self.W[i][j] = cij / math.sqrt(self.N[i] * self.N[j]) #余弦相似度
                #print '节目：'+i+'节目：'+j+'之间的相似度为：'+str(self.W[i][j])

    def _save_matrix_w(self):
        f = open('matrixW.txt', 'w')
        pickle.dump(self.W, f)
        f.close()

    def load_matrix_w(self): #载入大概需要7.96s
        f = open('matrixW.txt')
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
        #self._save_matrix_w()



    #基于物品的协同过滤算法，输入为综艺节目的urls，返回推荐的urls
    def itemCF(self, urls):
        rank = dict() #保存推荐的url及其对应的兴趣度
        for i in urls:

            variety = self.mongodb.search_variety_by_url(i)
            interest = float(variety['score'])

            #print variety['varietyname']
            #j表示某物品，wj表示物品i和物品j的相似度
            #
            #key 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
            #reverse -- 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。
            for j, wj in sorted(self.W[i].items(), key=itemgetter(1), reverse=True)[0:self.k]:
                #print self.W[i]['']
                #print j,wj
                #如果已经包含了物品j，跳过
                if j in urls:
                    continue
                #如果物品j是无效节目，跳过
                if self.mongodb.search_variety_by_url(j) is None:
                    continue
                #根据评分和相似度计算物品j的预测兴趣度
                if j not in rank.keys():
                    rank[j] = 0
                rank[j] += interest * wj
        #按照兴趣度排序，返回推荐书籍的urls
        sorted_rank = sorted(rank.iteritems(), key=operator.itemgetter(1), reverse=True)[0:10]
        #print 'sorted:\n', sorted_rank
        res = []
        for i in sorted_rank:
            res.append(i[0])
        return res #只返回预测兴趣度前10的urls

if __name__ == '__main__':
    recommend = Recommend()

    #recommend._build_inver_table()
    #recommend.cal_matrix_W()
    urls = []
    urls.append('https://movie.douban.com/subject/25894460/?from=subject-page')
    urls.append('https://movie.douban.com/subject/26709000/?from=subject-page')
    print '用户收藏的综艺节目：'
    for i in urls:
        variety= recommend.mongodb.search_variety_by_url(i)
        print variety['varietyname']
    print '-----------------------------------------------'
    print '根据用户收藏的综艺节目，推荐的列表：'

    for i in recommend.itemCF(urls):
        variety = recommend.mongodb.search_variety_by_url(i)
        interest = variety['varietyname']
        print interest

    print 'all down!'



