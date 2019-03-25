#!/usr/bin/python
# -*- coding:utf-8 -*-
from math import sqrt

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
                    "Lorde": 4, "Fall Out Boy": 1},
          "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
                   "Lorde": 4, "Fall Out Boy": 1},
          "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
                  "Lorde": 3, "Fall Out Boy": 1},
          "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
                    "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
          "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
                   "Daft Punk": 5, "Fall Out Boy": 3}}


def computeSimilarity(band1,band2,userRatings):
    average = {}
    #求出每一个user评价物品的均值
    for (key,ratings) in userRatings.items():
        print ratings
        for i in ratings:
            print i,ratings[i]
        #print key #    David
        #print ratings #{'Daft Punk': 5, 'Lorde': 4, 'Fall Out Boy': 1, 'Imagine Dragons': 3}
        average[key] = (float(sum(ratings.values())) /  len(ratings.values()))


    num  = 0 #分子
    dem1 = 0 #分母一部分
    dem2 = 0 #分母另一部分
    for (user,ratings) in userRatings.items():
        if band1 in ratings and band2 in ratings:
            avg = average[user]
            num += (ratings[band1] - avg) * (ratings[band2] - avg)
            dem1 += (ratings[band1] - avg) ** 2
            dem2 += (ratings[band2] - avg) ** 2


    return num / (sqrt(dem1) * sqrt(dem2))

if __name__ == '__main__':
    print computeSimilarity('Kacey Musgraves', 'Lorde', users3)
    # print computeSimilarity('Imagine Dragons', 'Lorde', users3)
    # print computeSimilarity('Daft Punk', 'Lorde', users3)



