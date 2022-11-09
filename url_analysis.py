# -*- coding:utf-8 -*-
import time
from js_analysis import JsAnalysis
import requests
import json
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options

def getInnerJoin(url,urlset,standardurl = "https://www.sangfor.com.cn/"):
    for i in url:
        if i[:27] == standardurl:
            urlset.add(i)
    return urlset

def getAllUrl(url,standardurl):
    urlset = set()
    subcontent = JsAnalysis().getContent(url)
    suburl = JsAnalysis().getUrl(subcontent)
    #取内部连接
    urlset = getInnerJoin(suburl,urlset,standardurl)
    listurl = list(urlset)
    for j in listurl:
        local_content = JsAnalysis().getContent(j)
        local_url = JsAnalysis().getUrl(local_content)
        urlset = getInnerJoin(suburl,urlset,standardurl)
    print(urlset)
    #取js连接
    ajs = []
    for z in urlset:
        if z[-3:] == ".js":
            ajs.append(z)
    jsurlset =set()
    for a in ajs:
        alocal_content = JsAnalysis().getContent(a)
        alocal_url = JsAnalysis().getUrl(alocal_content)
        jsurlset = getInnerJoin(alocal_url,jsurlset,standardurl)
    allurl = jsurlset|urlset
    usefulurl = []
    for b in allurl:
        if r"'\\" not in b and r':id' not in b and r".js" not in b and "," not in b and "_nuxt" not in b:
            print(b)
            usefulurl.append(b)
    return usefulurl


def getUsefulUrl(url,path,standardurl = ""):
    if standardurl == "":
        usefulurl = interfaceGetUrl(url)
    else:
        usefulurl = getAllUrl(url,standardurl)
    print(len(usefulurl))
    videofile = open(path + r"\vide-ofile.txt",mode="a",encoding="utf8")
    news_center = open(path + r"\news-center-file.txt",mode="a",encoding="utf8")
    info_center = open(path + r"\info-center-file.txt",mode="a",encoding="utf8")
    productfile = open(path + r"\product-file.txt",mode="a",encoding="utf8")
    otherfile = open(path + r"\other-file.txt",mode="a",encoding="utf8")
    for i in usefulurl:
        if r"/video" in i:
            videofile.write(i+"\n")
        elif r"/news" in i or r"case" in i:
            news_center.write(i+"\n")
        elif r"/document" in i:
            info_center.write(i+"\n")
        elif r"/solution" in i:
            productfile.write(i+"\n")
        else :
            otherfile.write(i+"\n")
    videofile.close()
    news_center.close()
    info_center.close()
    productfile.close()
    otherfile.close()
# standardurl = "https://www.sangfor.com.cn/"
# url = "https://www.sangfor.com.cn/"



#官方方法
def interfaceGetUrl(localurl) -> list:
    if localurl[-1] == "/":
        localurl = localurl[:-1]
    server = Server(r'D:\sangfor\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    wb = webdriver.Chrome(chrome_options=chrome_options)
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
    wb.get(localurl)
    wb.implicitly_wait(20)
    time.sleep(10)
    res = proxy.har
    Cookie = ""
    for entry in res['log']['entries']:
        req_url = entry['request']['url']
        if req_url[-4:] == ".ico":
            headers = entry['request']['headers']
            for header in headers:
                if header["name"] == "Cookie":
                    Cookie = header["value"]
    print(Cookie)
    wb.close()
    server.stop()
    url =  localurl + "/sf-sangfor-site/openapi/content/xss-api/htList"
    this_json = {"page":"1","pageSize":"2000","infoType":"2"}
    headers = {'cookie': Cookie}
    res = requests.post(url,json=this_json,headers=headers)
    content = res.json()

    #视频 contentSource:3
    videoPath = '/video/'

    #旧文档 contentSource:1  newData:0
    documentPath = '/document-list/'

    # 新文档 contentSource:1  newData:1
    newDocumentPath = '/document/'

    urllist = []
    initialurl = content["rows"]["ids"]
    for i in initialurl:
        local_json = dict(i)
        if local_json["contentSource"] == "3":
            local_url = local_json["contentSort"]
            urllist.append(local_url)
        elif local_json["contentSource"] == "1":
            local_url = local_json["contentVideoImgUrl"]
            urllist.append(local_url)
        else:
            print(i + "\n" + "解析url异常")
            return None
    parturl = content["rows"]["pathAll"]
    all_list =list(set(parturl + urllist))

    print(len(all_list))
    usefulurl = []
    for j in all_list:
        k = localurl + j
        usefulurl.append(k)
    return usefulurl



# url = "http://200.200.4.115:9200/sf-sangfor-site/openapi/content/xss-api/htList"
if __name__ == '__main__':
    url = "https://www-uat.atrust.sangfor.com/"
    path = r"D:\深信服官网测试2022-10-25-09-13"
    usefulurl = getUsefulUrl(url,path)




