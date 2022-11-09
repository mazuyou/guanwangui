from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from multiprocessing.pool import ThreadPool
import time
import json


def networkTest(urllist,path):
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    wb = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities=d)
    wb.get_log('performance').clear()
    wb.get_log('browser').clear()
    for url in urllist:
        wb.maximize_window()
        wb.implicitly_wait(20)
        wb.get(url)
        time.sleep(5)
        for item in wb.get_log('performance'):
            message = json.loads(item['message'])
            message1 = message['message']
            if message1["method"] == "Network.responseReceived" :
                status = message1["params"]["response"]["status"]
                if str(status)[0] == "5" or str(status)[0] == "4":
                    net_port = open(path + "\error-network.txt",mode= "a", encoding="utf8")
                    js_url = message1["params"]["response"]["url"]
                    net_port.write("异常URL：" + url + "\n" + "原因：" + js_url + "请求失败" + "\n")
                    net_port.close()
                    print("异常URL：" + url + "\n" + "原因：" + js_url + "请求失败" + "\n")
                    break
        for item in wb.get_log('browser'):
            if item["level"] == "SEVERE":
                print("异常URL：" + url + "原因：" + "控制台报错" + "\n")
                print(item["message"])
                net_port = open(path + "\error-console.txt", mode="a", encoding="utf8")
                net_port.write("异常URL：" + url + "原因：" + "控制台报错" + "\n")
                net_port.close()
                break
    wb.close()

def processInfo(path,filename = r"\info-center-file.txt",k = 3):
    file = open(path +filename,mode="r",encoding="utf8")
    urllist = []
    for line in file.readlines():
        urllist.append(line[:-1])
    print(urllist)
    pool = ThreadPool(k)
    step = len(urllist)//k + 1
    spilt_urllist = [urllist[i:i+step] for i in range(0,len(urllist),step)]
    print(spilt_urllist)
    for i in spilt_urllist:
        pool.apply_async(networkTest,args=(i,path))
    pool.close()
    pool.join()

def processNews(path,k = 3):
    filename = r"\news-center-file.txt"
    processInfo(path,filename = filename,k=k)

def processOther(path,k = 3):
    processInfo(path,filename = r"\other-file.txt",k=k)
    processInfo(path,filename = r"\product-file.txt",k=k)
    processInfo(path,filename = r"\vide-ofile.txt",k=k)


if __name__ == '__main__':
    path = r"D:\深信服官网测试2022-04-19-08-51"
    url = "https://www.sangfor.com.cn/"
    processNews(path,k=5)
