from smartclick import smartclick
from selenium import webdriver
from multiprocessing.pool import ThreadPool
from xml_analysis import GetXml


#多线程功能
def clicklink(line,clickreportpath):
    wb = webdriver.Chrome()
    wb.implicitly_wait(20)
    wb.maximize_window()
    wb.get(line)
    page_source = wb.page_source
    local_path = "/html/body/div/div/div/main"
    pathlist = GetXml().getAllXpath(page_source,local_path)
    print(pathlist)
    for i in pathlist:
        ele = wb.find_element_by_xpath(i)
        wb.execute_script("arguments[0].click()",ele)
        print(line + "click  " + i)
        handles = wb.window_handles
        if len(handles) == 2:
            wb.switch_to.window(handles[1])
            current_url = wb.current_url
            wb.close()
            wb.switch_to.window(handles[0])
            print(line + "链接:  " + current_url)
            report = open(clickreportpath,mode="a",encoding="utf8")
            report.write(line + "链接:  " + current_url)
        else:
            pass
        # except:
        #     print("error")
        #     wb.quit()
        #     break
    wb.quit()


if __name__ == '__main__':
    text = open("smartclick.txt","r",encoding="utf8")
    testData = []
    for line in text.readlines():
        param = line.split("   ")
        url = param[0]
        routepath = param[1]
        asserturl = param[2].replace(" ","")
        testData.append([url,routepath,asserturl])
    pool = ThreadPool(2)
    returnurl = []
    for i in testData:
        pool.apply_async(smartclick,args=(i[0],i[1]),callback=returnurl.append)
    pool.close()
    pool.join()
    print(returnurl)





