# -*- coding:utf-8 -*-
import os
import time
import document_test
import url_analysis
import network_test
import product_report
import url_report


#主文件，一定执行
#url = "https://www.sangfor.com.cn/"
#url = "https://www-uat.sangfor.com.cn/"
url = "http://10.6.128.84/"
standardurl = "https://www.sangfor.com.cn/"
nowtime = time.strftime("%Y-%m-%d-%H-%M")
path = r"D:\深信服官网测试%s"%nowtime
os.mkdir(path)
url_analysis.getUsefulUrl(url,path)

# # url 测试，选择执行测试
url_report.processUrlTest(url,path)

#文档测试，选择执行测试
document_test.processPDF(path,url)

# #net_work测试，选择执行测试
network_test.processNews(path,k=5)
network_test.processInfo(path,k=5)
network_test.processOther(path,k=5)

#根据smartclick文档点击，请运行 smartclick_report 文件，选择执行测试


#获得product全部链接，选择执行测试
product_report.processProduct(path,k=5)
