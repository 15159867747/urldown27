#!/usr/bin/python
# -*- coding:utf-8 -*-
# 基于项目的协同过滤推荐算法实现
import random,pickle

import math
from operator import itemgetter
from math import sqrt

class ItemBasedCF():
    # 初始化参数
    def __init__(self):
        # 找到相似的20部电影，为目标用户推荐10部电影
        self.n_sim_movie = 20
        self.n_rec_movie = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.movie_sim_matrix = {}
        self.movie_popular = {}
        self.movie_count = 0
        #用户平均评分
        self.average = {}
        #用户对物品的平均评分
        self.averagetv={}


        print('Similar movie number = %d' % self.n_sim_movie)
        print('Recommneded movie number = %d' % self.n_rec_movie)
        self.load_data()

    # 读文件得到“用户-电影”数据
    def get_dataset(self, filename, pivot=0.875):
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, movie, rating, timestamp = line.split('::')
            if(random.random() < pivot):
                self.trainSet.setdefault(user, {})  #相当于trainSet.get(user)，若该键不存在，则设trainSet[user] = {}，典中典

                #键中键：形如{'1': {'1287': '2.0', '1953': '4.0', '2105': '4.0'}, '2': {'10': '4.0', '62': '3.0'}}
                #用户1看了id为1287的电影，打分2.0
                self.trainSet[user][movie] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        self._save_data()
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

    def _save_data(self):
        f = open('trainset.txt', 'w')
        pickle.dump(self.trainSet, f)
        f.close()
        f1 = open('TestSet.txt', 'w')
        pickle.dump(self.testSet, f1)
        f1.close()

    def load_data(self):  # 载入大概需要7.96s
        f = open('trainset.txt')
        self.trainSet = pickle.load(f)
        f.close()
        f1 = open('TestSet.txt')
        self.testSet = pickle.load(f1)
        f1.close()


    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)


    # 计算电影之间的相似度 precisioin=0.1440	recall=0.0695	coverage=0.0364      改进后precisioin=0.0897	recall=0.0433	coverage=0.3298
    def calc_movie_sim(self):
        for user, movies in self.trainSet.items():  #循环取出一个用户和他看过的电影
            for movie in movies:
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                    self.averagetv[movie]=0

                self.averagetv[movie]+=float(movies[movie])
                self.movie_popular[movie] += 1  #统计每部电影共被看过的次数


        self.movie_count = len(self.movie_popular)  #得到电影总数

        print("Total movie number = %d" % self.movie_count)

    #求出每一个user评价物品的均值
        for key,ratings in self.trainSet.items():
            sum=0
            for i in ratings:
                sum=sum+float(ratings[i])
            self.average[key]=sum/len(ratings.values())
            #self.average[key] = (float(sum(float(str(ratings.values())))) /  len(ratings.values()))
        print '用户平均评分计算完成'
    #求



        for user, movies in self.trainSet.items():  #得到矩阵C，C[i][j]表示同时喜欢电影i和j的用户数

            for m1 in movies:

                for m2 in movies:
                    if m1 == m2:
                        continue

                    self.movie_sim_matrix.setdefault(m1, {})
                    self.movie_sim_matrix[m1].setdefault(m2, 0)

                    if m1 in movies and m2 in movies:


                        num = (float(movies[m1]) - float(self.averagetv[m1])/float(self.movie_popular[m1])) * (float(movies[m2]) - float(self.averagetv[m2])/float(self.movie_popular[m2]))
                        dem1= (float(movies[m1]) - float(self.averagetv[m1])/float(self.movie_popular[m1])) ** 2
                        dem2= (float(movies[m2]) - float(self.averagetv[m2])/float(self.movie_popular[m2])) ** 2
                        if (sqrt(dem1) * sqrt(dem2))!=0:
                            self.movie_sim_matrix[m1][m2]+=num / (sqrt(dem1) * sqrt(dem2))
                    #self.movie_sim_matrix[m1][m2] += 1  #同时喜欢电影m1和m2的用户+1    21.75  10.5   16.67
                    #self.movie_sim_matrix[m1][m2] += 1 /math.log(1 + len(movies)) #ItemCF-IUF改进，惩罚了 活跃用户 22.00 10.65 14.98
        print("Build co-rated users matrix success!")


        # # 计算电影之间的相似性
        # print("Calculating movie similarity matrix ...")
        # for m1, related_movies in self.movie_sim_matrix.items():    #电影m1，及m1这行对应的电影们
        #     for m2, count in related_movies.items():    #电影m2 及 同时看了m1和m2的用户数
        #         # 注意0向量的处理，即某电影的用户数为0
        #         if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
        #             self.movie_sim_matrix[m1][m2] = 0
        #         else:
        #             #计算出电影m1和m2的相似度
        #             self.movie_sim_matrix[m1][m2] = count / math.sqrt(self.movie_popular[m1] * self.movie_popular[m2])
        #             print self.movie_sim_matrix[m1][m2]
        # print('Calculate movie similarity matrix success!')

        #添加归一化    precisioin=0.2177	recall=0.1055	coverage=0.1497
        # maxDict = {}
        # max = 0
        # for m1, related_movies in self.movie_sim_matrix.items():
        #     for m2, _ in related_movies.items():
        #         maxDict.setdefault(m2,0.0)
        #         if self.movie_sim_matrix[m1][m2] > maxDict[m2]:
        #             maxDict[m2] = self.movie_sim_matrix[m1][m2]
        #
        # for m1, related_movies in self.movie_sim_matrix.items():    #归一化
        #     for m2, _ in related_movies.items():
        #         # self.movie_sim_matrix[m1][m2] = self.movie_sim_matrix[m1][m2] / maxDict[m2]
        #         self.movie_sim_matrix[m1][m2] = self.movie_sim_matrix[m1][m2] / maxDict[m2]


    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影
    def recommend(self, user):
        K = self.n_sim_movie    #找到相似的20部电影
        N = self.n_rec_movie    #为用户推荐10部
        rank = {}
        watched_movies = self.trainSet[user]    #该用户看过的电影
        #print '用户看过的电影',watched_movies #用户看过的电影 {'1266': '5', '1265': '5', '2094': '2',
        for movie, rating in watched_movies.items():    #遍历用户看过的电影及对其评价
            #print '遍历用户看过的电影及对其评价','电影',movie,'评分',rating #遍历用户看过的电影及对其评价 电影 1266 评分 5
            #找到与movie最相似的K部电影,遍历电影及与movie相似度
            for related_movie, w in sorted(self.movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
                #print self.movie_sim_matrix[movie][related_movie]
                #print '相似电影',related_movie,'相似度',w #相似电影 553 相似度 0.082808075006
                if related_movie in watched_movies: #如果用户已经看过了，不推荐了
                    continue
                if float(w)!=0:
                    rank.setdefault(related_movie, 0)
                #rank[related_movie] += w * float(rating)    #计算用户对该电影的兴趣
                    ri=float(self.averagetv[movie])/float(self.movie_popular[movie])
                    rj=float(self.averagetv[related_movie])/float(self.movie_popular[related_movie])
                    rank[related_movie] += w*(float(rating)-rj)/abs(w)   #计算用户对该电影的兴趣
        for i in rank:
            rank[i]=float(self.averagetv[i])/float(self.movie_popular[i])+rank[i]


        #返回用户最感兴趣的N部电影
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]


    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print('Evaluating start ...')
        N = self.n_rec_movie    #要推荐的电影数
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_movies = set()

        for i, user in enumerate(self.trainSet):
            test_moives = self.testSet.get(user, {})    #测试集中用户喜欢的电影
            rec_movies = self.recommend(user)   #得到推荐的电影及计算出的用户对它们的兴趣

            for movie, w in rec_movies: #遍历给user推荐的电影
                if movie in test_moives:    #测试集中有该电影
                    hit += 1                #推荐命中+1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))


if __name__ == '__main__':
    rating_file = 'C://ratings.dat'
    itemCF = ItemBasedCF()
    # itemCF.get_dataset(rating_file)
    itemCF.calc_movie_sim()
    itemCF.evaluate()# coding = utf-8
