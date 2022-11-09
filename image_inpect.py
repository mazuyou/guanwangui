# -*- coding:utf-8 -*-
from selenium import webdriver


#图片检查功能
def loadimg(path,errpath,url):
    wb = webdriver.Chrome()
    wb.get(url)
    wb.implicitly_wait(20)
    page_source = wb.page_source
    if "无法连接" in str(page_source):
        report = open(errpath,mode="a",encoding="utf8")
        report.write(url+"\n"+"false"+"\n")
        report.close()
    else:
        report = open(path,mode="a+",encoding="utf8")
        report.write(url+"\n"+"true"+"\n")
        report.close()
    wb.quit()

