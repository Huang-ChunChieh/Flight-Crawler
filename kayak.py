from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import requests

depart_city = "TPE" #出發地
arrive_city = "KIX" #目的地
depart_time = "2024-07-01" #去程時間 XXXX(西元年)/XX(月)/XX(日)
arrive_time = "2024-07-04" #返程時間 XXXX(西元年)/XX(月)/XX(日)  若為單程則此欄為""
cabinclass = "" #艙等 經濟艙:""/特選經濟艙:"premium"/商務艙:"business"/頭等艙:"first"
numOfAdult = 1
numOfStudent = 1
numOfTeenager = 0
numOfChild = 1
numOfBaby1S = 0
numOfBaby1L = 0
adult = str(numOfAdult) + "adults" #成人數量 格式:人數填入numOfAdult  若無則此欄為""
student = str(numOfStudent) + "students" #18歲以上學生數量  格式:人數填入numOfStudent  若無則此欄為""
children = "children" + "-17"*numOfTeenager + "-11"*numOfChild + "-1S"*numOfBaby1S + "-1L"*numOfBaby1L#18歲以下數量 格式:青少年(12-17):-17 / 兒童(2-11):-11 / 2歲以下佔坐兒童:-1S / 2歲以下不佔坐兒童:-1L / 若無則此欄為""
#範例:兩位青少年、1位兒童、2位2歲以下佔坐兒童、1位2歲以下不佔坐兒童 ==> -17-17-11-1S-1S-1L
directflight = "?fs=fdDir=true;stops=~0" #是否僅限直飛航班 若是:"fs=fdDir=true;stops=~0" / 或否則此欄為""

if cabinclass=="premium":
    classtype = "特選經濟艙"
elif cabinclass=="business":
    classtype = "商務艙"
elif cabinclass=="first":
    classtype = "頭等艙"
else :
    classtype = "經濟艙"

search_Info = f'''目前查詢條件\n出發地:{depart_city}\n目的地:{arrive_city}\n出發日期:{depart_time}\n抵達日期:{arrive_time}
艙等:{classtype}\n旅客人數\n成人:{str(numOfAdult)}人\n學生:{str(numOfStudent)}人\n青少年:{str(numOfTeenager)}人\n兒童:{str(numOfChild)}人
2歲以下佔坐嬰兒:{str(numOfBaby1S)}人\n2歲以下不佔坐嬰兒:{str(numOfBaby1L)}人\n
'''

#若人數設定中students非0，則會多顯示需驗證學生身分內容，XPATH需重新定位
if numOfStudent >= 1:
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[3]'
    flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div'
else:
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[3]'
    flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div'

url = f"https://www.tw.kayak.com/flights/{depart_city}-{arrive_city}/{depart_time}/{arrive_time}/{cabinclass}/{adult}/{student}/{children}{directflight}"
url_price = url + "&sort=price_a"
url_bestflight = url + "&sort=bestflight_a"
url_duration = url + "&sort=duration_a"
browser = webdriver.Chrome()
browser.get(url)
sleep(10)

def get_SUG_flight(): #獲取最便宜/超值/最快三項簡易資訊
    print("推薦航班資訊")
    print("==========================")
    result_SUG = browser.find_elements(By.CLASS_NAME,"Hv20-option")
    for z in result_SUG:
        print(z.text)
    sug_result_message = "推薦航班資訊\n==== ==== ====\n" + "\n".join(a.text for a in result_SUG)
    return sug_result_message

def get_cheapest_result():
    print("最優惠航班資訊")
    print("============")
    cheapest_result_summary = browser.find_element(By.XPATH,cheapestFlightSummary_XPATH) #cheapest_result_box_summary
    cheapest_result_summary.click() #click cheapest_result_box
    sleep(3)
    result_cheapest = browser.find_elements(By.XPATH,flightInfo_XPATH) #get cheapest flight info
    for j in result_cheapest:
        print(j.text)
    cheapest_result_message = "最優惠航班資訊\n==== ==== ====\n" + j.text + "詳細資訊歡迎點擊下方連結\n" + url_price
    return cheapest_result_message

def get_best_result():
    print("超值航班資訊")
    print("===========")
    best_result_summary = browser.find_element(By.XPATH,bestFlightSummary_XPATH) #best_result_box_summary
    best_result_summary.click() #click best_result_box
    sleep(3)
    result_best = browser.find_elements(By.XPATH,flightInfo_XPATH) #get best flight info
    for i in result_best:
        print(i.text)
    best_result_message = "最佳航班資訊\n==== ==== ====\n" + i.text + "詳細資訊歡迎點擊下方連結\n" + url_bestflight
    return best_result_message


def get_fast_result():
    print("最快航班資訊")
    print("===========")
    fast_result_summary = browser.find_element(By.XPATH,fastFlightSummary_XPATH) #fast_result_box_summary
    fast_result_summary.click() #click fast_result_box
    sleep(3)
    result_fast = browser.find_elements(By.XPATH,flightInfo_XPATH) #get fast flight info
    for k in result_fast:
        print(k.text)
    fast_result_message = "最快航班資訊\n==== ==== ====\n" + k.text + "詳細資訊歡迎點擊下方連結\n" + url_duration
    return fast_result_message

def lineNotify(token, msg):
    headers = {
        "Authorization" : "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message' : msg}
    r = requests.post("https://notify-api.line.me/api/notify",headers = headers, params = payload)
    print(r.status_code)
    return r.status_code

def main():
    # sug_flight_result = get_SUG_flight()
    # cheapest_flight_result = get_cheapest_result()
    # best_flight_result = get_best_result()
    # fast_flight_result = get_fast_result()
    lineNotify(token, search_Info)
    sleep(2)
    # lineNotify(token, sug_flight_result)
    # sleep(2)
    # lineNotify(token, cheapest_flight_result)
    # sleep(2)
    # lineNotify(token, best_flight_result)
    # sleep(2)
    # lineNotify(token, fast_flight_result)
    # sleep(2)

token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
main()