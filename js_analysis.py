# -*- coding:utf-8 -*-
import requests
import re


#js分析功能
class JsAnalysis(object):
    #获得content
    def getContent(self,url):
        jscontent = requests.get(url)
        content = jscontent.content
        return content

    #获得js返回的URL
    def getUrl(self,content):
        urllist = []
        try:
            content = content.decode("unicode-escape")
        except:
            content = content.decode()
        #提取半链接
        content = content.replace('"/"',"")
        parturl = re.findall('"/(.+?)"',str(content))
        if "200" in parturl:
            parturl.remove("200")
        if "404" in parturl:
            parturl.remove("404")
        if "500" in parturl:
            parturl.remove("500")
        for i in parturl:
            urllist.append("https://www.sangfor.com.cn/"+i)
        #提取全链接
        urllist1 = re.findall('"https:(.+?)"',str(content))
        for i in urllist1:
            i = "https:" + i
            urllist.append(i)
        return urllist

    #获得js返回的图片
    def getPicture(self,content):
        picurl = re.findall('"data:image/png(.+?)"',str(content))
        picture_url = []
        for i in picurl:
            picture_url.append("data:image/png"+i)
        pictureurl = list(set(picture_url))
        return pictureurl

if __name__ == '__main__':
    content = JsAnalysis().getContent("https://www.sangfor.com.cn/_nuxt/90466e5.js")
    urllist = JsAnalysis().getUrl(content)
    for i in urllist:
        print(i)
#
# for i in partlist:
#     print(i)
# a = JsAnalysis().getContent("https://www.sangfor.com.cn/_nuxt/static/1648130143/product-and-solution/sangfor-security/SASE/payload.js")
# b = JsAnalysis().getUrl(a)
# print(b)
# print(len(b["complete"]))






