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
            # print key ,ratings     #5842 {'1304': '5', '2949': '3', '1220': '3', ...
            sum=0
            for i in ratings:
                sum=sum+float(ratings[i])
            self.average[key]=sum/len(ratings.values())
            #self.average[key] = (float(sum(float(str(ratings.values())))) /  len(ratings.values()))
        print '用户平均评分计算完成'




        for user, movies in self.trainSet.items():  #得到矩阵C，C[i][j]表示同时喜欢电影i和j的用户数
            #print 'user：：',user           #user： 3519
            #print 'movies',movies          #{'165': '2', '3258': '1', '3259': '3', '3552': '2', '3250': '3', '3253': '3', '3255': '5', '3257': '2', '344': '3', '345': '4', '3854': '4', '340': '2', '3851': '5', '349': '3', '2858': '5', '2915': '3', '2916': '3', '420': '2', '1498': '2', '1701': '2', '1707': '1', '1060': '1', '2314': '3', '296': '2', '294': '3', '3773': '2', '590': '3', '593': '5', '592': '4', '595': '3', '597': '4', '3774': '2', '195': '2', '194': '5', '1124': '2', '1126': '2', '1127': '2', '3145': '4', '276': '2', '277': '2', '279': '4', '3671': '2', '2822': '3', '3386': '2', '2545': '3', '3024': '2', '2987': '3', '3388': '2', '1090': '3', '2268': '3', '1408': '2', '520': '2', '523': '3', '2262': '4', '2263': '3', '1401': '1', '1011': '2', '1405': '4', '1234': '2', '2447': '2', '443': '3', '442': '3', '444': '3', '102': '2', '107': '3', '104': '3', '105': '3', '39': '5', '2100': '2', '2042': '2', '31': '4', '1840': '4', '1240': '3', '2168': '3', '647': '4', '1246': '5', '2165': '4', '648': '4', '3098': '3', '2161': '1', '430': '2', '431': '2', '2616': '2', '3809': '2', '337': '1', '3298': '4', '3299': '1', '2288': '3', '3450': '4', '2953': '2', '543': '2', '1081': '4', '3893': '3', '3897': '4', '1468': '2', '2701': '3', '2140': '2', '94': '5', '1466': '4', '3203': '3', '2700': '5', '3208': '1', '3398': '5', '555': '3', '3635': '3', '551': '3', '553': '3', '552': '2', '3067': '4', '234': '3', '235': '3', '236': '3', '237': '3', '231': '1', '232': '4', '1191': '4', '1059': '3', '1194': '2', '1197': '5', '2942': '3', '1': '4', '1753': '3', '1279': '5', '1172': '3', '140': '3', '141': '4', '1270': '4', '613': '2', '617': '4', '1179': '3', '998': '5', '1885': '2', '1884': '2', '1883': '4', '3705': '2', '1285': '5', '3194': '2', '2127': '4', '2082': '1', '2083': '4', '3114': '3', '2539': '4', '1475': '2', '2710': '1', '1307': '4', '2716': '4', '2717': '2', '2657': '3', '1225': '3', '3412': '2', '3418': '4', '25': '4', '27': '2', '20': '4', '3793': '4', '2407': '2', '2402': '2', '1377': '3', '1376': '3', '1379': '2', '1378': '4', '2409': '2', '1345': '3', '1955': '3', '1954': '3', '1959': '4', '3249': '3', '3248': '3', '3243': '2', '2502': '4', '3568': '3', '3247': '3', '3246': '4', '3844': '4', '3846': '2', '371': '4', '372': '5', '2907': '1', '2908': '5', '1483': '1', '1485': '3', '82': '3', '1488': '3', '87': '1', '1711': '5', '2450': '3', '2302': '4', '2798': '1', '2412': '2', '7': '3', '1271': '5', '586': '3', '587': '3', '581': '4', '413': '2', '1136': '3', '588': '3', '589': '3', '3152': '2', '3157': '4', '3155': '4', '249': '4', '3391': '3', '1380': '4', '2574': '1', '2797': '5', '2378': '3', '2379': '2', '2374': '3', '2375': '3', '2372': '3', '516': '3', '3591': '4', '2459': '1', '1221': '3', '2455': '3', '628': '5', '455': '3', '457': '3', '175': '4', '173': '2', '170': '3', '3699': '2', '2599': '4', '2054': '1', '3690': '2', '656': '4', '1500': '5', '187': '1', '2110': '3', '3087': '3', '1509': '4', '2114': '3', '3083': '5', '2117': '3', '339': '2', '2628': '3', '3874': '4', '3877': '2', '3526': '3', '1918': '1', '3525': '2', '193': '3', '1912': '4', '3528': '2', '1916': '1', '3448': '3', '17': '4', '3882': '4', '19': '2', '866': '3', '2020': '5', '2021': '1', '2751': '3', '3082': '4', '2692': '2', '2690': '2', '2081': '5', '3902': '3', '888': '2', '1968': '5', '1965': '2', '1614': '3', '1961': '3', '1610': '3', '1611': '3', '321': '4', '327': '1', '2871': '3', '2875': '4', '830': '3', '74': '3', '71': '1', '2971': '3', '3052': '5', '3050': '4', '3051': '2', '2331': '5', '1046': '4', '3527': '3', '1681': '1', '1682': '3', '1268': '5', '3499': '3', '1265': '2', '2094': '2', '2966': '3', '2985': '3', '3653': '3', '1544': '3', '3129': '3', '1541': '3', '2950': '3', '3127': '4', '3174': '2', '542': '3', '2846': '3', '2269': '2', '2249': '2', '2245': '2', '2247': '3', '68': '3', '2243': '3', '2463': '3', '2706': '5', '2468': '3', '2469': '3', '1015': '3', '3408': '4', '69': '4', '2799': '1', '1824': '3', '1821': '3', '2410': '2', '2413': '3', '2144': '5', '1388': '3', '2142': '3', '2141': '2', '2416': '3', '920': '3', '1387': '3', '2064': '1', '1381': '3', '2794': '1', '2795': '3', '3949': '2', '317': '2', '316': '1', '3274': '3', '1923': '3', '369': '4', '1231': '4', '832': '3', '3476': '2', '3477': '4', '835': '4', '839': '2', '3': '3', '368': '2', '2762': '3', '367': '3', '364': '3', '380': '2', '381': '3', '3317': '4', '1645': '3', '785': '3', '780': '4', '1729': '3', '1396': '1', '1079': '4', '1722': '4', '3614': '3', '2291': '3', '3004': '1', '62': '3', '2193': '3', '2194': '5', '3000': '2', '252': '2', '253': '4', '3163': '1', '2804': '3', '1421': '3', '2000': '3', '1580': '5', '1586': '4', '3361': '3', '3362': '3', '2369': '3', '736': '2', '2150': '2', '1030': '3', '505': '2', '502': '2', '500': '4', '1213': '3', '1210': '4', '1358': '4', '1214': '3', '2580': '2', '2420': '3', '2421': '2', '2422': '2', '2423': '3', '461': '4', '1356': '3', '2436': '4', '1863': '2', '168': '3', '3729': '3', '2014': '3', '1641': '4', '161': '2', '3689': '2', '3688': '4', '3686': '3', '3684': '2', '2109': '3', '1457': '3', '2518': '3', '1100': '2', '1101': '4', '408': '3', '2104': '2', '2735': '3', '2639': '3', '3863': '1', '2739': '4', '1097': '4', '3536': '3', '3538': '3', '1275': '3', '3438': '2', '3439': '1', '1810': '5', '877': '3', '3185': '4', '3186': '4', '2746': '4', '3915': '4', '3913': '3', '438': '3', '3911': '4', '434': '2', '1608': '4', '432': '3', '356': '3', '355': '2', '260': '5', '353': '3', '352': '2', '47': '4', '801': '3', '266': '3', '216': '3', '769': '3', '762': '2', '1784': '4', '218': '5', '765': '2', '3325': '2', '3040': '2', '3044': '5', '3046': '5', '1777': '3', '2324': '5', '2329': '5', '1073': '3', '4': '2', '280': '3', '282': '4', '1673': '3', '1094': '3', '3763': '3', '3764': '2', '1091': '3', '1092': '3', '3481': '5', '3480': '3', '673': '3', '261': '3', '3136': '4', '3130': '3', '265': '5', '3138': '3', '58': '5', '2012': '2', '1554': '4', '2991': '3', '50': '5', '3033': '2', '2395': '4', '532': '2', '2259': '3', '1036': '3', '2253': '3', '1416': '3', '65': '1', '2474': '3', '2470': '2', '2770': '3', '2774': '5', '203': '5', '2478': '3', '2802': '3', '111': '2', '110': '3', '2803': '3', '2174': '3', '1397': '3', '2072': '2', '1394': '3', '1393': '3', '427': '3', '912': '5', '1569': '3', '2607': '3', '305': '2', '307': '4', '3261': '3', '3263': '4', '3264': '3', '3268': '2', '3509': '3', '3504': '2', '848': '2', '2671': '3', '539': '3', '2677': '5', '538': '4', '2929': '2', '3360': '3', '2926': '3', '708': '5', '3210': '4', '1639': '3', '2815': '3', '569': '3', '2817': '1', '2816': '2', '508': '5', '562': '3', '509': '5', '3071': '4', '3072': '4', '3077': '4', '225': '3', '224': '3', '223': '3', '222': '5', '3176': '4', '1027': '2', '1020': '1', '1188': '5', '1186': '4', '1187': '5', '1183': '4', '2352': '4', '2357': '3', '605': '3', '153': '2', '3308': '3', '157': '2', '156': '5', '1088': '3', '608': '4', '1894': '2', '1897': '5', '2134': '4', '2133': '2', '48': '3', '2003': '4', '46': '3', '3105': '3', '44': '3', '3107': '3', '3100': '3', '3101': '2', '1353': '1', '1444': '4', '5': '2', '1293': '3', '1290': '4', '2504': '2', '1296': '2', '1297': '2', '1449': '4', '1295': '4', '2640': '4', '2641': '4', '450': '3', '1562': '3', '487': '2', '485': '2', '480': '3', '3428': '3', '3421': '2', '3426': '4', '3425': '3', '3424': '3', '2002': '2', '1367': '3', '470': '2', '471': '4', '1363': '2', '2004': '1', '2005': '3'}

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
        #print '用户看过的电影',watched_movies             #'1266': '5', '1265': '5', '2094': '2',...
        for movie, rating in watched_movies.items():    #遍历用户看过的电影及对其评价
            #print '遍历用户看过的电影及对其评价','电影',movie,'评分',rating              #遍历用户看过的电影及对其评价 电影 1266 评分 5
            #找到与movie最相似的K部电影,遍历电影及与movie相似度
            for related_movie, w in sorted(self.movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
                #print self.movie_sim_matrix[movie][related_movie]
                #print '相似电影',related_movie,'相似度',w #相似电影 553 相似度 0.082808075006
                if related_movie in watched_movies: #如果用户已经看过了，不推荐了
                    continue
                if float(w)!=0:
                    rank.setdefault(related_movie, 0)

                    rj=float(self.averagetv[related_movie])/float(self.movie_popular[related_movie])
                    rank[related_movie] += w*(float(rating)-rj)/abs(w)   #计算用户对该电影的兴趣
        for i in rank:
            print 'rank',rank
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
