# coding=utf-8
'''
Created on 2016/4/3
 @author: moverzp
 description: 
'''
from bs4 import BeautifulSoup
import re, html_downloader
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class HtmlParser(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()  # html网页下载器

    def _get_new_urls(self, soup):
        # print soup
        try:
            new_urls = []
            # 同样喜欢区域：<div class="recommendations-bd">
            # soup = BeautifulSoup(soup,'html.parser')
            # print soup
            recommend = soup.find(class_='recommendations-bd')
            # print ''''''''
            # print recommend
            all_dd = recommend.find_all('dd')
            # print all_dd
            for dd in all_dd:
                '''<dd>
                    <a href="https://movie.douban.com/subject/25909168/?from=subject-page" class="" data-moreurl-dict={&#34;subject_id&#34;:&#34;25908008&#34;,&#34;from&#34;:&#34;tv-recommended-subject&#34;,&#34;bid&#34;:&#34;OHBo61e_WsA&#34;}>天天向上</a>
                  </dd>'''
                links = dd.find_all('a', href=re.compile(r"https://movie\.douban\.com/subject/\d"))
                for link in links:
                    new_url = link['href']
                    print new_url
                    new_urls.append(new_url)
            return new_urls
        except:
            return None

    def _get_new_data(self, page_url, soup, threshold):
        res_data = {}
        new_actor = []

        # print soup
        # try:  # 舍弃页面信息不完全的url
        # url
        res_data['url'] = page_url
        bq = soup.find('div', class_="tags-body")
        all_href = bq.find_all('a')
        a = 0
        zy = "综艺"
        zyjm = "综艺节目"

        for link in all_href:
            if link.get_text() == zy or link.get_text() == zyjm:
                print link.get_text()
                a=1
        if a==1:
            if soup.find('span', property='v:itemreviewed').string:
                res_data['varietyname'] = soup.find('span', property='v:itemreviewed').string

            if soup.find('strong', class_='ll rating_num').string:
                res_data['score'] = soup.find('strong', class_='ll rating_num').string
            info = soup.find('div', id='info')
            if soup.find('span', property='v:summary'):
                intro = soup.find('span', property='v:summary')
                res_data['intro'] = intro.get_text().strip()
                print res_data['intro']

            if soup.find('span', class_='attrs'):  # 主演
                href = soup.find('span', class_='attrs')
                all_href = href.find_all('a')
                for link in all_href:
                    new_actor.append(link.get_text())
                res_data['actor'] = new_actor
            if info.find(property='v:genre'):
                res_data['type'] = info.find(property='v:genre').next_element.strip()
                print res_data['type']
            if info.find(text='制片国家/地区:'):
                res_data['area'] = info.find(text='制片国家/地区:').next_element.strip()
                print res_data['area']

            if info.find(text='语言:'):
                res_data['language'] = info.find(text='语言:').next_element.strip()
                print res_data['language']

            if info.find(property='v:initialReleaseDate'):
                res_data['first'] = info.find(property='v:initialReleaseDate').next_element.strip()
                print res_data['first']

            if info.find(text='单集片长:'):
                res_data['time'] = info.find(text='单集片长:').next_element
                print res_data['time']
            return res_data
        else:
            return None




        # <span property="v:itemreviewed">快乐大本营</span>
        '''if soup.find('span', property='v:itemreviewed').string:
            res_data['varietyname'] = soup.find('span', property='v:itemreviewed').string

        if soup.find('strong', class_='ll rating_num').string:
            res_data['score'] = soup.find('strong', class_='ll rating_num').string
            # <strong class="ll rating_num" property="v:average">6.9</strong>'''

            # print res_data['url']#,res_data['varietyname'],res_data['score']
        '''if float(res_data['score']) < float(threshold):  # 评分低于阈值，舍弃
            print 'invalid data'
            return None'''

        '''<div id="info">      
            <span class="actor"><span class='pl'>主演</span>: <span class='attrs'><a href="/celebrity/1313023/" rel="v:starring">何炅</a> / <a href="/celebrity/1274270/" rel="v:starring">谢娜</a> / <a href="/celebrity/1318460/" rel="v:starring">吴昕</a> / <a href="/celebrity/1313024/" rel="v:starring">杜海涛</a> / <a href="/celebrity/1313025/" rel="v:starring">李维嘉</a> / <a href="/celebrity/1312936/" rel="v:starring">李湘</a></span></span><br/>
            <span class="pl">类型:</span> <span property="v:genre">脱口秀</span><br/>
            <span class="pl">官方网站:</span> <a href="http://www.mgtv.com/v/1/290346/index.html?cxid=95kqkw8n6" rel="nofollow" target="_blank">www.mgtv.com/v/1/290346/index.html?cxid=95kqkw8n6</a><br/>
            <span class="pl">制片国家/地区:</span> 中国大陆<br/>
            <span class="pl">语言:</span> 汉语普通话<br/>
            <span class="pl">首播:</span> <span property="v:initialReleaseDate" content="1997-07-11(中国大陆)">1997-07-11(中国大陆)</span><br/>
        
        
            <span class="pl">单集片长:</span> 90分钟<br/>
            <span class="pl">又名:</span> Happy Camp<br/>
            <span class="pl">IMDb链接:</span> <a href="http://www.imdb.com/title/tt5830218" target="_blank" rel="nofollow">tt5830218</a><br>

            </div>'''

        '''info = soup.find('div', id='info')
        if soup.find('span', property='v:summary'):
            intro = soup.find('span', property='v:summary')
            res_data['intro'] = intro.get_text().strip()
            print res_data['intro']

        if soup.find('span', class_='attrs'):  # 主演
            href = soup.find('span', class_='attrs')
            all_href = href.find_all('a')
            for link in all_href:
                new_actor.append(link.get_text())
            res_data['actor'] = new_actor'''

        # print href

        #print info

        '''if info.find(property='v:genre'):
            res_data['type'] = info.find(property='v:genre').next_element.strip()
            print res_data['type']
        if info.find(text='制片国家/地区:'):
            res_data['area'] = info.find(text='制片国家/地区:').next_element.strip()
            print res_data['area']

        if info.find(text='语言:'):
            res_data['language'] = info.find(text='语言:').next_element.strip()
            print res_data['language']

        if info.find(property='v:initialReleaseDate'):
            res_data['first'] = info.find(property='v:initialReleaseDate').next_element.strip()
            print res_data['first']

        if info.find(text='单集片长:'):
            res_data['time'] = info.find(text='单集片长:').next_element
            print res_data['time']'''



        #return res_data
        '''if res_data['intro'] == None or res_data['hotReview'] == None or res_data['hotReview'] == 'None':
            print 'invalid data'
            return None'''

    def parse(self, page_url, html_cont, threshold):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup, threshold)
        if new_data is None:
            new_urls = None
        else:
            new_urls = self._get_new_urls(soup)

        return new_urls, new_data


if __name__ == "__main__":
    Url = "https://movie.douban.com/subject/2155284"
    downloader = html_downloader.HtmlDownloader()
    parser = HtmlParser()
    # print downloader.download(Url)
    parser.parse(Url, downloader.download(Url), 0)
