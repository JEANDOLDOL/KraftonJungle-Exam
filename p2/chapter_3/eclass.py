
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome("C:\Users\82109\Downloads\chromedriver_win32")
url = 'https://nid.naver.com/nidlogin.login'
driver.get(url)

