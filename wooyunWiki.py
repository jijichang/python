#/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
   采集wooyun知识库

'''
import urllib2
import re
import sys
import hashlib
import math
import threading  
reload(sys)
sys.setdefaultencoding( "utf-8" )

#读取远程内容
def file_get_contents(url):
    response = urllib2.urlopen(url);
    return response.read();

#获取总页数
def get_total_page_number(url):
    patt = re.compile(r"class='nextpostslink'>»</a><a href='http://drops.wooyun.org/page/(.*?)' class='last'>.*?</a>")
    content = file_get_contents(url)
    total = patt.findall(content)
    print 'Success get total number:[{0}]'.format(total[0])
    return int(total[0])

#所有列表页面URL
def get_page_list_url(TotalPage):
    PageListUrls = []
    for i in range(TotalPage):
        PageListUrls.append('http://drops.wooyun.org/page/%d' % i)
    return PageListUrls


#采集文章链接
def get_article_url(PageListUrls):
    PageUrls = []
    for url in PageListUrls:
        patt = re.compile(r"<h2 class=\"entry-title\"><a href=\"(.*?)\" rel=\"bookmark\" title=\".*?\">.*?</a></h2>")
        content = file_get_contents(url)
        article = patt.findall(content)
        for aurl in article:
            print 'Article URL:[{0}]'.format(aurl)
            PageUrls.append(aurl)
    return PageUrls


#采集文章内容并且缓存本地
def get_article_content(PageUrls):
    for url in PageUrls:
        #抓取页面
        content = file_get_contents(url)
        #获取标题
        patt_title = re.compile(r"<h1 class=\"entry-title ng-binding\">(.*?)</h1>")
        title = patt_title.findall(content)
        #获取作者
        path_author = re.compile(r"<a href=\"/author/.*?\" class=\"title ng-binding\">(.*?)</a>")
        author = path_author.findall(content)
        #获取文章内容
        path_section = re.compile(r"<section class=\"entry-content ng-binding\" ng-bind-html=\"postContentTrustedHtml\">([\w\W]*?)</section>")
        section = path_section.findall(content)
        #将采集数据缓存本地
        cache_Articles(title[0],author[0],section[0])

#将采集数据缓存本地
def cache_Articles(title, author, content):
    cache_file = hashlib.md5(title.encode('utf-8')).hexdigest()
    fr = open('config/template.html','r')
    fw = open('books/{0}.html'.format(cache_file),'w+')
    try:
        text = fr.read()
        s = text.replace('${title}

,str(title)).replace('${author}

,str(author)).replace('${content}

,str(content))
        fw.write(s)
        print 'Success Cache file URL:{0}.html'.format(cache_file)

    finally:
        fr.close()
        fw.close()

def main():

    ThreadNum  = 30

    threads = []
     
    #采集网站地址
    SiteUrl = "http://drops.wooyun.org/"

    #总页数
    TotalPage = 0

    #所有列表页面URL
    PageListUrls = []

    #所有文章URL
    PageUrls = []

    #文章内容
    Articles = []

    #获取总页数
    TotalPage = get_total_page_number( SiteUrl )

    #构建列表页面URL
    PageListUrls = get_page_list_url(TotalPage)

    #采集文章链接
    PageUrls = get_article_url(PageListUrls)

    #获取每个线程执行条数
    ThreadExceNum = math.ceil( len(PageUrls) / ThreadNum  )

    #分组
    PageUrlGroup = []
    j = 0
    for i in range(0,len(PageUrls)):

        if j % ThreadExceNum == 0:
            #加入线程
            t1 = threading.Thread(target=get_article_content,args=(PageUrlGroup,))
            threads.append(t1)
            PageUrlGroup = []
        else:
            PageUrlGroup.append(PageUrls[i])
        j = j + 1

    for t in threads:
        try:
            t.setDaemon(True)
            t.start()
        except Exception,ex:
            print Exception,":",ex
    t.join()
    print "采集完成!!!"

if __name__ == '__main__':
    main()
