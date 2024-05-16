from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from time import sleep
from bs4 import BeautifulSoup
import random
import time


depart_city = "tpe"
arrive_city = "kmj"
depart_time = "240602"
arrive_time = "240605"
adultsv2 = "1"
cabinclass = "economy"
childrenv2 = ""
inboundaltsenabled = "false"
outboundaltsenabled = "false"
preferdirects = "false"

bestFlightSummary_XPATH = '//*[@id="app-root"]/div[1]/div/div/div/div[1]/div[3]/div[1]'
cheapestFlightSummary_XPATH = '//*[@id="app-root"]/div[1]/div/div/div/div[1]/div[3]/div[2]'
fastFlightSummary_XPATH = '//*[@id="app-root"]/div[1]/div/div/div/div[1]/div[3]/div[3]'
flightInfo_XPATH = '//*[@id="app-root"]/div[1]/div/div/div/div[1]/div[4]/div[1]/div/div/a/div/div[1]/div/div[1]'


ua = UserAgent()
user_agent = ua.random
chrome_options = Options()
chrome_options.add_argument(f"--user-agent={user_agent}")
browser = webdriver.Chrome(options=chrome_options)
url = f"https://www.skyscanner.com.tw/transport/flights/{depart_city}/{arrive_city}/{depart_time}/{arrive_time}/?adultsv2={adultsv2}&cabinclass={cabinclass}&childrenv2={childrenv2}&inboundaltsenabled={inboundaltsenabled}&outboundaltsenabled={outboundaltsenabled}&preferdirects={preferdirects}&ref=home&rtn=1"
browser.get(url)
sleep(10)

def get_SUG_flight(): #獲取最佳/最便宜/最快三項簡易資訊
    print("推薦航班資訊")
    print("==========================")
    result = browser.find_elements(By.CLASS_NAME,"FqsTabs_tooltipTargetContainer__ZWJkO")
    for z in result:
        print(z.text)

def get_best_result():
    print("最佳航班資訊")
    print("===========")
    best_result_summary = browser.find_element(By.XPATH,bestFlightSummary_XPATH) #best_result_box_summary
    best_result_summary.click() #click best_result_box
    time.sleep(random.uniform(3,10))
    result = browser.find_elements(By.XPATH,flightInfo_XPATH) #get best flight info
    for i in result:
        print(i.text)

def get_cheapest_result():
    print("最優惠航班資訊")
    print("============")
    cheapest_result_summary = browser.find_element(By.XPATH,cheapestFlightSummary_XPATH) #cheapest_result_box_summary
    cheapest_result_summary.click() #click cheapest_result_box
    time.sleep(random.uniform(3,10))
    result = browser.find_elements(By.XPATH,flightInfo_XPATH) #get cheapest flight info
    for j in result:
        print(j.text)

def get_fast_result():
    print("最快航班資訊")
    print("===========")
    fast_result_summary = browser.find_element(By.XPATH,fastFlightSummary_XPATH) #fast_result_box_summary
    fast_result_summary.click() #click fast_result_box
    time.sleep(random.uniform(3,10))
    result = browser.find_elements(By.XPATH,flightInfo_XPATH) #get fast flight info
    for k in result:
        print(k.text)

get_SUG_flight()
sleep(2)
get_best_result()
sleep(2)
get_cheapest_result()
sleep(2)
get_fast_result()
sleep(2)
browser.quit()