# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import redis
reload(sys)
sys.setdefaultencoding('utf-8')
class RedisManage(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
        self.rdb = redis.Redis(connection_pool=self.pool)

    def setSim(self,movie1,movie2,sim):
        self.rdb.set(movie1+movie2,sim)     # key是"gender" value是"male" 将键值对存入redis缓存

    def getSim(self,movie1,movie2):
        return self.rdb.get(movie1+movie2)

if __name__ == "__main__":
    mongotv=RedisManage()
    #mongotv.addsim('m1','m2','0.2212')
    print mongotv.getSim('m1','m1')