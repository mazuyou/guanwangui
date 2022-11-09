from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
from multiprocessing.pool import ThreadPool
import time


server = Server(r'.\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
server.start()
proxy = server.create_proxy()
# 设置driver options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
wb = webdriver.Chrome(chrome_options=chrome_options)
wb.maximize_window()
wb.implicitly_wait(20)
wb.get("https://www.sangfor.com.cn/info-center/case-center/755")