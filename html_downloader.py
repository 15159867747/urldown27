# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
import urllib2
from time import sleep
import cookielib
import random
import winsound
import html_parser
import requests
from requests.exceptions import ConnectionError


class HtmlDownloader(object):
    useCookie1 = False #是否使用cookie
    changeCookie = False #是否需要更改cookie状态
    '''
    proxy = None
    max_count = 5'''

    def __init__(self):
        pass
        #self.proxy = None
        #self.max_count = 5

    '''def get_proxy(self):
        try:
            proxy_pool_url = 'http://127.0.0.1:5000/get'
            response = requests.get(proxy_pool_url)
            if response.status_code == 200:
                return response.text
            else:
                return self.get_proxy()
        except ConnectionError:
            return None

    def get_html(self, url, count=1):
        #global proxy
        print('crawling', url)
        print('try count', count)
        if count >= self.max_count:
            print('请求次数过多')
            return None
        try:
            if self.proxy:
                proxies = {
                    'https': 'https://' + self.proxy,

                    #  'http': 'http://39.137.107.98:80'
                }
                Header = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'  # 浏览器头描述
                proxy_support = urllib2.ProxyHandler(self.proxy)
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                request = urllib2.Request(url, headers=Header,proxies=self.proxy)

                # response = requests.get(url, headers=headers,proxies=proxies)
            else:
                self.proxy = self.get_proxy()
                proxies = {
                    'https': 'https://' + self.proxy,

                    #  'http': 'http://39.137.107.98:80'
                }
                Header = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'  # 浏览器头描述
                proxy_support = urllib2.ProxyHandler(self.proxy)
                opener = urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                request = urllib2.Request(url, headers=Header,proxies=self.proxy)
                response = urllib2.urlopen(request)
            print(response.status_code)
            if response.status_code == 200:
                return response.read()
            if response.status_code == 302:
                print(response.status_code)
                proxy = self.get_proxy()
            if response.status_code == 403:
                print("403")
                print(response.status_code)
                self.proxy = self.get_proxy()
            if self.proxy:
                print("use proxy", proxy)

                return self.get_html(url)
            else:
                print('get Proxy failed')
                return None

        except ConnectionError, e:
            print('error occurred', e.args)
            self.proxy = self.get_proxy()
            count += 1
            return self.get_html(url)'''

    def _set_cookie(self, fileName):
        cookie = cookielib.MozillaCookieJar()
        cookie.load(fileName, ignore_discard=True, ignore_expires=True)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
    
    def save_cookie(self, fileName, url): #不能在有别的实例运行时执行
        #声明一个MozillaCookieJar实例保存cookie
        cookie = cookielib.MozillaCookieJar(fileName)
        #构建opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')
        response = urllib2.urlopen(request)
        print response.getcode()
        cookie.save(ignore_discard=True, ignore_expires=True)
        print 'Successfully saved'

    def _download(self, url):
        # 设置cookie信息
        if HtmlDownloader.changeCookie == True:
            HtmlDownloader.changeCookie = False
            if HtmlDownloader.useCookie1 == True: 
                print 'set cookie1'
                self._set_cookie('cookie1.txt')
            else:
                print 'set cookie2'
                self._set_cookie('cookie2.txt')

        Header = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'  # 浏览器头描述
        '''headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

        }'''
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', Header)

            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
            if e.code == 403:
                winsound.Beep(600, 1000)  # 蜂鸣发出警告，音量600， 时常1000ms
                return 403
            if e.code == 404:
                winsound.Beep(600, 300)  # 蜂鸣发出警告，音量600， 时常300ms
                sleep(0.1)
                winsound.Beep(600, 300)  # 蜂鸣发出警告，音量600， 时常300ms
                return 404
        if response.getcode() == 200:  # 200表示读取成功
            return response.read()

    def download(self, url):
        times = 1
        if url is None:
            return None
        while True:

            html_cont = self._download(url)
            #html_cont = self.get_html(url)
            if html_cont == 404:  # 404错误，返回404，然后将url放入404Urls
                return 404
            elif html_cont == 403:  # 如果出现403等错误，等待后继续爬取
                HtmlDownloader.changeCookie = True
                HtmlDownloader.useCookie1 = not HtmlDownloader.useCookie1

                sleeptime = random.randint(20, 30) * times  # 递增等待时间
                print 'sleeping %d times...' % times
                times += 1
                sleep(sleeptime)
            else:
                # print html_cont
                return html_cont


if __name__ == "__main__":
    Url = "https://movie.douban.com/subject/25908008/"
    downloader = HtmlDownloader()
    parser = html_parser.HtmlParser()
    # print downloader.download(Url)
    parser._get_new_urls(downloader.download(Url))
