'''
import requests
from bs4 import BeautifulSoup

url = 'https://www.tigerairtw.com/zh-tw'
dom = requests.get(url).text
soup = BeautifulSoup(dom,'html.parser')
print(soup.get_text())

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

browser = webdriver.Chrome()
url = 'https://booking.tigerairtw.com/zh-TW/index' #虎航訂票網站
browser.get(url)
sleep(5)
location_origin = browser.find_element(By.CLASS_NAME,'q-field__inner.relative-position.col.self-stretch') #出發地
sleep(2)
location_origin.click()
sleep(3)
origin = browser.find_element(By.CLASS_NAME,'q-card.station-picker-card.no-shadow')
browser.find_element(By.XPATH,'/html/body/div[9]/div/div/div/div[3]/button/span[2]/span').click()
sleep(2)
#origin.find_element(By.XPATH,'//*[@id="q-portal--menu--4"]/div/div/div/div[3]')
browser.quit()
#q-portal--menu--4 > div > div > div > div:nth-child(3)
#/html/body/div[9]/div/div/div/div[3]/button/span[2]/span'''

# main parse code

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup


def from_to(browser, departure, destination):
    """
    open 'google.com/flights' default page
    then enter departure and destination
    return page source we want
    """
    browser.get('https://www.google.com/flights/#search')
    sleep(0.3)
    keyIn(browser, departure, destination)
    sleep(0.3)

    return browser.page_source


def keyIn(browser, place1, place2):
    """
    因為輸入時div的class會改變，所以先click之後才key關鍵字
    """

    # XPATH
    search_box_XPATH = "//div[@class='LJV2HGB-Ab-a']"
    input_XPATH = "//input[@class='LJV2HGB-Mb-f']"
    # click
    browser.find_elements(By.XPATH,search_box_XPATH)[0].click()
    browser.find_elements(By.XPATH,input_XPATH)[0].send_keys(place1)
    sleep(0.3)
    browser.find_elements(By.XPATH,input_XPATH)[0].send_keys(Keys.RETURN)

    browser.find_elements(By.XPATH,search_box_XPATH)[1].click()
    browser.find_elements(By.XPATH,input_XPATH)[0].send_keys(place2)
    sleep(0.3)
    browser.find_elements(By.XPATH,input_XPATH)[0].send_keys(Keys.RETURN)


def get_tickets(departure, destination):
    """
    get tickets from 'google.com/flights' through selenium
    return a list of Tickets
    """
    browser = webdriver.Chrome()
    html = from_to(browser, departure, destination)
    browser.quit()
    bs = BeautifulSoup(html, 'html.parser')

    tickets = []

    for ele in bs.find_all('div', 'LJV2HGB-d-W'):
        try:
            price = ele.find('div', 'LJV2HGB-d-Ab').text  # 票價
            ticket_type = ele.find('div', 'LJV2HGB-d-Cb').text  # 票種
            time = ele.find('div', 'LJV2HGB-d-Zb').text  # 時間
            company = ele.find('div', 'LJV2HGB-d-j').text  # 航空公司
            duration = ele.find('div', 'LJV2HGB-d-E').text  # 飛行時間
            flight_type = ele.find('div', 'LJV2HGB-d-Qb').text  # 航班資訊(直達/轉機)
        except:
            continue
        ticket = {
            'price': price,
            'ticket_type': ticket_type,
            'time': time,
            'company': company,
            'duration': duration,
            'flight_type': flight_type,
        }
        tickets.append(ticket)
    return tickets
from_to(browser, departure, destination)
get_tickets("TPE","KIX")