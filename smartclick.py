# -*- coding:utf-8 -*-
from selenium import webdriver
from xml_analysis import GetXml
import time
from selenium.webdriver import ActionChains
import requests


'''
根据中文智能点击的UI自动化
# url = "https://www.sangfor.com.cn/"
# routepath = "产品与服务-云计算-安全虚拟化aSEC"
'''
def smartclick(url,routepath):
    wb = webdriver.Chrome()
    wb.get(url)
    wb.implicitly_wait(20)
    wb.maximize_window()
    #记录查找时间
    print(time.strftime("%Y-%m-%d-%H-%M-%S"))
    urllabel = "new"
    route_path_sub = routepath.split("-")
    local_path = ""
    click_lable = ""
    new_url = ""
    for i in route_path_sub:
        if new_url == url and click_lable == "open":
            local_xml = wb.page_source
            local_path = GetXml().searchKeyword(local_xml,local_path,i)
            print(local_path)
            ele = wb.find_element_by_xpath(local_path)
            wb.execute_script("arguments[0].click()",ele)
        else:
            if urllabel == "new":
                local_url = wb.current_url
                local_xml = wb.page_source
                pathjson = GetXml().searchNearbyText(local_xml,"/html/body")
                print(pathjson)
                local_path = []
                for k in pathjson.keys():
                    if pathjson[k] == i:
                        local_path.append(k)
                local_text = ""
                #异常处理
                for j in local_path:
                    try:
                        local_text = wb.find_element_by_xpath(j).text
                        local_path = j
                        break
                    except:
                        pass
                print(local_path)
                #异常处理
                try:
                    wb.find_element_by_xpath(local_path).click()
                except:
                    ele = wb.find_element_by_xpath(local_path)
                    wb.execute_script("arguments[0].click()",ele)
            else:
                local_url = wb.current_url
                local_xml = wb.page_source
                print(i,local_path)
                local_path = GetXml().searchKeyword(local_xml,local_path,i)
                print("searchKeyword"+local_path)
                #异常处理
                try:
                    action = ActionChains(wb)
                    ele1 = wb.find_element_by_xpath(local_path)
                    action.move_to_element(ele1)
                    wb.find_element_by_xpath(local_path).click()
                    click_lable = "open"
                except:
                    ele = wb.find_element_by_xpath(local_path)
                    wb.execute_script("arguments[0].click()",ele)
            #判断页面是否跳转
            if new_url != local_url:
                urllabel = "new"
            else:
                urllabel = "old"
            print(urllabel)
    windows = wb.window_handles
    wb.switch_to.window(windows[-1])
    new_url = wb.current_url
    print(new_url)
    print(time.strftime("%Y-%m-%d-%H-%M-%S"))
    wb.quit()
    return new_url

# url = "https://www.sangfor.com.cn/"
# routepath = "产品与服务-云计算-安全虚拟化aSEC"
# aaa = smartclick(url,routepath)
# print(aaa)
if __name__ == '__main__':
    url = "https://www.baidu.com"
    routepath = "智安全-安全产品-云安全访问服务（SASE）"
    aaa = smartclick(url,routepath)
    print(aaa)