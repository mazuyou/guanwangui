# -*- coding:utf-8 -*-
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options


#监控网页network请求
def urlNetwork(url):
    #启动
    server = Server(r'.\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()
    #设置driver options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    wb = webdriver.Chrome(chrome_options=chrome_options)
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
    wb.maximize_window()
    wb.get(url)
    wb.implicitly_wait(20)
    res = proxy.har
    network = []
    for entry in res['log']['entries']:
        req_url = entry['request']['url']
        res_status = entry['response']['status']
        res_time = str(entry['time']) + "ms"
        network.append([req_url,res_status,res_time])
    server.stop()
    return network

if __name__ == '__main__':
    for i in urlNetwork("https://www.sangfor.com.cn/news-center/news-list/2020/10/202101300932"):
         print(i)
    # print(urlNetwork("https://www.sangfor.com.cn"))

