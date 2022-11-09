# -*- coding:utf-8 -*-
from lxml import etree
from selenium import webdriver
import re
from lxml import html
import time


#xml分析功能
class GetXml(object):
    # 获得源代码
    def getHtml(self,url,click = ""):
        self.url = url
        wb = webdriver.Chrome()
        wb.get(url)
        wb.implicitly_wait(20)
        if click != "":
            wb.find_element_by_xpath(click).click()
        xml_file = wb.page_source
        wb.close()
        return xml_file

    #获得页面所有文本
    def getText(self,xml_file):
        xml = xml_file.split("<body>")
        newxml = xml[1].replace(">",">xxx")
        html = etree.HTML(newxml)
        content = html.xpath('string(.)')
        content = content.split("xxx")
        xml_content_list = []
        for i in content:
            rei = i.replace("\n", "")
            recon = rei.replace(" ", "")
            if "{" not in recon and recon !="":
                xml_content_list.append(recon)
        return xml_content_list

    #获得js链接
    def codeJs(self,xml_file):
        parturl = re.findall('"/(.+?)"',str(xml_file))
        js_url = []
        for i in parturl:
            if ".js" in i:
                js_url.append("/%s"%i)
        jsurllist = list(set(js_url))
        return jsurllist

    #获得图片
    def getPicture(self,xml_file):
        picurl = re.findall('"data:image/png(.+?)"',str(xml_file))
        picture_url = []
        for i in picurl:
            picture_url.append("data:image/png"+i)
        pictureurllist = list(set(picture_url))
        return pictureurllist

    #获得页面URL
    def getUrl(self,xml_file):
        xmlurl1 = re.findall('"/(.+?)"',str(xml_file))
        xmlurl2 = re.findall('"https:(.+?)"',str(xml_file))
        xml_urllist = []
        for i in xmlurl2:
            xml_urllist.append("https:"+i)
        xmlurl = list(set(xml_urllist))
        return xml_urllist

    #获得页面所有xpath
    def getAllXpath(self,xml_file,path = ""):
        root = html.fromstring(xml_file)
        tree = root.getroottree()
        result = root.xpath(path + '//*')
        xpathlist=[]
        for r in result:
            xpathlist.append(tree.getpath(r))
        return xpathlist

    #页面text对应的xpath，path为key，中文为value
    def pathText(self,url,click = ""):
        xpathlist = GetXml().getAllXpath(url,click)
        xpathtextDict = {}
        wb = webdriver.Chrome()
        wb.get(url)
        wb.implicitly_wait(20)
        if click != "":
            wb.find_element_by_xpath(click).click()
        for i in xpathlist:
            #异常处理
            try:
                j = wb.find_element_by_xpath(i).text
                if j is not None and "\n" not in j:
                    xpathtextDict[j] = i
            except:
                pass
        wb.close()
        return xpathtextDict

    #页面text对应的xpath，path为value，中文为key
    def textPath(self,xml_file,path):
        root = html.fromstring(xml_file)
        tree = root.getroottree()
        result = root.xpath(path + '//*')
        xpathlist=[]
        for i in result:
            locat_path = tree.getpath(i)
            xpathlist.append(locat_path)
        textPathDict = {}
        for j in xpathlist:
            local_xml = etree.HTML(xml_file,etree.HTMLParser())
            local_content1 = local_xml.xpath(j+"/text()")
            local_content2 = str(local_content1).replace("\n","").replace(" ","").replace("[","").replace("]","").replace("'","")
            local_content2 = local_content2.replace(r"\n","")
            if local_content2 != "":
                textPathDict[local_content2] = j
        return textPathDict


    #搜索path层级下的text
    def searchNearbyText(self,xml_file,path):
        root = html.fromstring(xml_file)
        tree = root.getroottree()
        result = root.xpath(path + '//*')
        xpathlist=[]
        for i in result:
            locat_path = tree.getpath(i)
            xpathlist.append(locat_path)
        textPathDict = {}
        for j in xpathlist:
            local_xml = etree.HTML(xml_file,etree.HTMLParser())
            local_content1 = local_xml.xpath(j+"/text()")
            local_content2 = str(local_content1).replace("\n","").replace(" ","").replace("[","").replace("]","").replace("'","")
            local_content2 = local_content2.replace(r"\n","")
            if local_content2 != "":
                textPathDict[j] = local_content2
        return textPathDict


    #搜索path下面的关键字
    def searchKeyword(self,xml_file,path,keyword):
        part_path = path.split("/")
        for i in range(len(part_path)):
            part_path = path.split("/")
            path_last = part_path[-1]
            path = path[0:-(len(path_last) + 1)]
            route_text = GetXml().searchNearbyText(xml_file,path).values()
            if keyword in route_text:
                local_json = GetXml().searchNearbyText(xml_file,path)
                return list(local_json.keys())[list(local_json.values()).index(keyword)]
        print("Can't find %s"%keyword)
        return None

if __name__ == '__main__':
    xml = open(r"C:\Users\Administrator\Desktop\new 2.html",mode="r",encoding="utf8")
    xml_file = xml.read()
    xpathlist = GetXml().getAllXpath(xml_file,"/html/body/div/div/div/main")
    for i in xpathlist:
        print(i)

# url = "https://www.sangfor.com.cn"
# routepath = "企业-可口可乐-了解详情"
# wb = webdriver.Chrome()
# wb.get(url)
# wb.implicitly_wait(20)
# aa = wb.find_element_by_xpath("/html/body/div/div/div/main/div/div[3]/div/div[1]/div[1]/div[2]/div/p")
# wb.execute_script("arguments[0].click()",aa)

