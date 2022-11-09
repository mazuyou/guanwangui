# -*- coding:utf-8 -*-
import os
import time
import multithreading
from multiprocessing.pool import ThreadPool
import url_network
import xml_analysis
import image_inpect
import js_analysis
import url_analysis
from selenium import webdriver


#获得点击的文字
# url = "https://www.sangfor.com.cn/"
# standardurl = "https://www.sangfor.com.cn/"
# nowtime = time.strftime("%Y-%m-%d-%H-%M")
# path = r"D:\深信服官网测试%s"%nowtime
# os.mkdir(path)
# url_analysis.getUsefulUrl(url,standardurl,path)
# path = r"D:\深信服官网测试2022-04-08-21-12"
# otherfile = open(path + r"\otherfile.txt",mode="r",encoding="utf8")
# pool = ThreadPool(3)
# clickreportpath = path + r"\clickreport.txt"
# for line in otherfile.readlines():
#     print(line)
#     pool.apply_async(multithreading.clicklink,args=(line,clickreportpath))
# pool.close()
# pool.join()




# 点击连接,生成报告
'''
path = path
url = url
htmltext = 点击的文字
'''
def click_report(path,url,htmltext):
    pool = ThreadPool(5)
    urlpath = path + r"\click_report.txt"
    for i in htmltext:
        pool.apply_async(multithreading.clicklink,args=(urlpath,url,i))
    pool.close()
    pool.join()


#生成network报告
'''
path = path
url = url
'''
def network_report(url,path):
    network_report = url_network.urlNetwork(url)
    report = open(path + r"\network_report.txt",mode="w",encoding="utf8")
    err_report = open(path + r"\network_err_report.txt",mode="w",encoding="utf8")
    for i in network_report:
        if i[1] != 200:
            err_report.write(str(i))
            err_report.close()
        else:
            report.write(str(i))
            report.close()

# #生成图像加载报告
'''
path = path
html = html源代码
'''
def img_report(html,path):
    xml_img_url = xml_analysis.GetXml().getPicture(html)
    xml_js_url = xml_analysis.GetXml().codeJs(html)
    js_url = []
    for i in xml_js_url:
        localcontent = js_analysis.JsAnalysis().getContent(url+i)
        localurl = js_analysis.JsAnalysis().getPicture(localcontent)
        if localurl is not None:
            for j in localurl:
                js_url.append(j)

    all_img_url = js_url + xml_img_url
    img_url = list(set(all_img_url))
    print(len(img_url))
    imgpath = path + r"\imgload_report.txt"
    imgerrpath = path + r"\imgerr_report.txt"
    pool = ThreadPool(5)
    for i in img_url:
        pool.apply_async(image_inpect.loadimg,args=(imgpath,imgerrpath,i))
    pool.close()
    pool.join()








