import requests
import url_analysis
from multiprocessing.pool import ThreadPool


def urlTest(urllist,path):
    for i in urllist:
        res = requests.get(i)
        res_status = res.status_code
        if str(res_status)[0] == "4" or str(res_status)[0] == "5":
            netreport = open(path + "\error-url.txt", mode="a", encoding="utf8")
            netreport.write("URL错误:" + i + "\n")
            print("URL解析错误:" + i + "\n")
            print(res_status)
        else:
            print(i,res_status)

def processUrlTest(url,path,k = 3):
    urllist = url_analysis.interfaceGetUrl(url)
    print(urllist)
    pool = ThreadPool(k)
    step = len(urllist)//k + 1
    spilt_urllist = [urllist[i:i+step] for i in range(0,len(urllist),step)]
    print(spilt_urllist)
    for i in spilt_urllist:
        pool.apply_async(urlTest,args=(i,path))
    pool.close()
    pool.join()

if __name__ == '__main__':
    path = r"D:\深信服官网测试2022-04-18-17-22"
    url = "https://www.sangfor.com.cn/"
    processUrlTest(url,path)
