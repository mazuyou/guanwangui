# -*- coding:utf-8 -*-
import js_analysis
from lxml import html
from selenium import webdriver
import re
from xml_analysis import GetXml


noclick = ["产品与服务","行业","咨询购买","技术支持","合作伙伴","产业教育","更多"]
content = js_analysis.JsAnalysis().getContent("https://www.sangfor.com.cn/_nuxt/995dbfd.js")
a = re.sub("[A-Za-z0-9\!\%\[\]\,\。<>/*=|().:$_]", "", str(content.decode()))
url = "https://www.sangfor.com.cn/"
html1 = GetXml().getHtml(url)
text = GetXml().getText(html1)

#获得貌似有JS的文字
asjs_text = []
for i in text:
    if i in a:
        asjs_text.append(i)
print(asjs_text)
path_text = GetXml().pathText(url)
print(path_text.keys())
#取并集
js_text_all = list(set(asjs_text).intersection(set(path_text.keys())))
#去除noclick
js_text = list(set(js_text_all).difference(set(noclick)))
print(js_text)

#在js中的文字处理
textroute = []
for i in js_text:
    local_path = path_text[i]
    print(local_path)
    wb = webdriver.Chrome()
    wb.implicitly_wait(20)
    wb.get(url)
    try:
        wb.find_element_by_xpath(local_path).click()
    except:
        local_path_js = wb.find_element_by_xpath(local_path)
        wb.execute_script("arguments[0].click()",local_path_js)
    local_handles = wb.window_handles
    if len(local_handles) != 1:
        wb.quit()
    else:
        wb.quit()
        local_text = GetXml().pathText(url,click=local_path)
        print(local_text.keys())
        js_text_sub = list(set(local_text.keys()).difference(set(text)))
        js_text_sub_path = []
        if js_text_sub is not None:
            for i in js_text_sub:
                js_text_sub_path.append(js_text_sub[i])
        textroute.append([i,local_path,js_text_sub,js_text_sub_path])
        print([i,local_path,js_text_sub,js_text_sub_path])

print(textroute)





