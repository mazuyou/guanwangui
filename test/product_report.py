import time
from multiprocessing.pool import ThreadPool
import requests
from selenium import webdriver
import re
from urllib.parse import urlparse


def clicklink(urllist,path):
    wb = webdriver.Chrome()
    wb.implicitly_wait(20)
    wb.maximize_window()
    for url in urllist:
        wb.get(url)
        time.sleep(8)
        print(url)
        local_url = urlparse(url)
        page_source = wb.page_source
        page_source_i = str(page_source).split("<main")
        page_source_j = page_source_i[1].split("</main>")
        all_link = re.findall('href="(.+?)"',page_source_j[0])
        print(all_link)
        for i in all_link:
            if i[0] == r"/":
                report = open(path + "\clickreport.txt",mode="a",encoding="utf8")
                report.write(url + "----" + local_url.scheme +"://"+ local_url.netloc + i+ "\n")
            elif i[:4] == "http":
                if "mp4" in i:
                    report = open(path + "\clickreport.txt",mode="a",encoding="utf8")
                    report.write(url + "----" + i+ "\n")
                else:
                    req = requests.get(i)
                    res = req.status_code
                    if str(res)[0] == "4" or str(res)[0] == "5":
                        err_report = open(path + "\error_clickreport.txt",mode="a",encoding="utf8")
                        err_report.write(url + "----" + i+ "\n")
                    else:
                        report = open(path + "\clickreport.txt",mode="a",encoding="utf8")
                        report.write(url + "----" + i+ "\n")
    wb.close()

def processProduct(path,filename = r"\product-file.txt",k = 5):
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
        pool.apply_async(clicklink,args=(i,path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    path = r"D:\深信服官网测试2022-04-26-09-43"
    processProduct(path,k=3)
