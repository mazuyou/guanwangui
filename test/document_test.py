from selenium import webdriver
import time
from multiprocessing.pool import ThreadPool

'''
info-center/document测试
'''
def damagePDF(urllist,path):
    wb = webdriver.Chrome()
    wb.maximize_window()
    wb.implicitly_wait(20)
    for url in urllist:
        print(url)
        if "document" in url:
            wb.get(url)
            time.sleep(15)
            frame = wb.find_element_by_tag_name('iframe')
            wb.switch_to.frame(frame)
            page_source = wb.page_source
            if "无效或损坏的" in page_source:
                print("无效或损坏的PDF文件:" + url)
                report = open(path + "\error-PDF-file.txt",mode="a",encoding="utf8")
                report.write("无效或损坏的PDF文件:" + url + "\n")
    wb.close()


def processPDF(path,url,k = 5):
    file = open(path + r"\info-center-file.txt",mode="r",encoding="utf8")
    urllist = []
    for line in file.readlines():
        urllist.append(line[:-1])
    print(urllist)
    try:
        urllist.remove(url + "info-center/document/index")
    except:
        pass
    print(len(urllist))
    pool = ThreadPool(k)
    step = len(urllist)//k + 1
    spilt_urllist = [urllist[i:i+step] for i in range(0,len(urllist),step)]
    print(spilt_urllist)
    for i in spilt_urllist:
        pool.apply_async(damagePDF,args=(i,path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    path = r"D:\深信服官网测试2022-04-09-13-55"
    url = "https://www.sangfor.com.cn/"
    processPDF(path,url)

