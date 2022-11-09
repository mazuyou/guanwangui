from selenium import webdriver


url = "https://www.sangfor.com.cn"
wb = webdriver.Chrome()
wb.get(url)
wb.implicitly_wait(20)



