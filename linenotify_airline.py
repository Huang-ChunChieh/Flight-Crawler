from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import requests

#========Info Should Be Setting========#
token = "XXX" #Fill in your Token
depart_city = "TPE" #出發地
arrive_city = "KIX" #目的地  若為單程則此欄為""
depart_time = "2024-07-10" #去程時間 XXXX(西元年)-XX(月)-XX(日)
arrive_time = "" #返程時間 XXXX(西元年)-XX(月)-XX(日)  若為單程則此欄為""
cabinclass = "business" #艙等  經濟艙:""  特選經濟艙:"premium"  商務艙:"business"  頭等艙:"first"
directflight = True #是否僅限直飛航班 若是->True  若否->False
#Numbers of Travelers
numOfAdult = 1 #成人數量
numOfStudent = 1 #18歲以上學生數量
numOfTeenager = 0 #青少年(12-17歲)數量
numOfChild = 1 #兒童(2-11)數量
numOfBaby1S = 0 #2歲以下佔坐兒童數量
numOfBaby1L = 0 #2歲以下不佔坐兒童數量
#======================================#
# 旅客人數(轉為網址用)
if numOfAdult == 0:
    adult = ""
else:
    adult = str(numOfAdult) + "adults"
if numOfStudent == 0:
    student = ""
else:
    student = str(numOfStudent) + "students"
if numOfTeenager > 0 or numOfChild > 0 or numOfBaby1S >0 or numOfBaby1L > 0:
    children = "children" + "-17"*numOfTeenager + "-11"*numOfChild + "-1S"*numOfBaby1S + "-1L"*numOfBaby1L
else:
    children = ""

# 艙等(轉為顯示查詢條件用)
if cabinclass == "premium":
    classtype = "特選經濟艙"
elif cabinclass == "business":
    classtype = "商務艙"
elif cabinclass == "first":
    classtype = "頭等艙"
else:
    classtype = "經濟艙"

# 是否直飛(轉為顯示查詢條件用)
if directflight == True:
    fdDir = "fs=fdDir=true;stops=~0"
    directFlight = "是"
else:
    fdDir = ""
    directFlight = "否"

# 目前查詢條件
search_Info = f'''\n目前查詢條件\n出發地:{depart_city}\n目的地:{arrive_city}\n出發日期:{depart_time}\n抵達日期:{arrive_time}
艙等:{classtype}\n僅限直飛航班:{directFlight}\n旅客人數\n成人:{str(numOfAdult)}人\n學生:{str(numOfStudent)}人\n青少年:{str(numOfTeenager)}人\n兒童:{str(numOfChild)}人
2歲以下佔坐嬰兒:{str(numOfBaby1S)}人\n2歲以下不佔坐嬰兒:{str(numOfBaby1L)}人'''
#======================================#

# 人數設定中若Students非0，則會多顯示需驗證學生身分內容，XPATH需重新定位
# 單向航程只會有一行資訊
if numOfStudent >= 1 and arrive_time != "": # 學生!=0 雙向航程
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[3]'
    #flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div'
    GoTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[1]/span[1]'
                             #//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[1]/span[1]
    GoTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[1]/span[3]'
    GoTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[2]/div/div[1]'
    GoTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[2]/div/div[2]'
    GoTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[4]/div[1]/span'
    GoTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[5]/div[1]'
    BackTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[1]/span[1]'
    BackTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[1]/span[3]'
    BackTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[2]/div/div[1]'
    BackTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[2]/div/div[2]'
    BackTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[4]/div[1]/span'
    BackTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[5]/div[1]'
    AirlineNameXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div/div[1]'
    TotalPricePerPersonXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div[1]/div[1]'
elif numOfStudent == 0 and arrive_time != "": # 學生=0 雙向航程
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[3]'
    #flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div'
    GoTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[1]/span[1]'
    GoTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[1]/span[3]'
    GoTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[2]/div/div[1]'
    GoTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[2]/div/div[2]'
    GoTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[4]/div[1]/span'
    GoTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[5]/div[1]'
    BackTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[1]/span[1]'
    BackTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[1]/span[3]'
    BackTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[2]/div/div[1]'
    BackTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[3]/div[2]/div/div[2]'
    BackTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[4]/div[1]/span'
    BackTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[2]/div/div/div[5]/div[1]'
    AirlineNameXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div/div[1]'
    TotalPricePerPersonXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div[1]/div[1]'
elif numOfStudent >= 1 and arrive_time == "":   # 學生!=0 單向航程
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[3]'
    #flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div'
    GoTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[1]/span[1]'
    GoTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[1]/span[3]'
    GoTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[2]/div/div[1]'
    GoTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[2]/div/div[2]'
    GoTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[3]/div[1]/span'
    GoTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[4]/div[1]'
    AirlineNameXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div/div[1]'
    TotalPricePerPersonXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div[1]/div[1]'
else: # 學生=0 單向航程
    cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[1]'
    bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[2]'
    fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[1]/div[3]'
    #flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div'
    GoTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[1]/span[1]'
    GoTripArriveTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[1]/span[3]'
    GoTripDepartAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[2]/div/div[1]'
    GoTripArriveAirportXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[2]/div[2]/div/div[2]'
    GoTripDirectFlightOrNotXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li/div/div/div[3]/div[1]/span'
    GoTripTotalTimeXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div[1]/div[1]'
    AirlineNameXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div/div[1]'
    TotalPricePerPersonXPATH = '//*[@id="listWrapper"]/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/a/div/div/div[1]/div[1]'


#URL Setting
url = f"https://www.tw.kayak.com/flights/{depart_city}-{arrive_city}/{depart_time}/{arrive_time}/{cabinclass}/{adult}/{student}/{children}?fs=cabin=-m;{fdDir}"
url_Price = url + "&sort=price_a" # 價格優先排序
url_Best = url + "&sort=bestflight_a" # 超值優先排序
url_Duration = url + "&sort=duration_a" # 最快優先排序
browser = webdriver.Chrome()
browser.get(url)
sleep(10)

def get_Flight_Result(): # 獲取所需資訊
    if numOfStudent >= 1:   # 查詢條件中包含學生，需要驗證以獲取學生票價 => 回傳已通知使用者
        info_StudentOrNot = "**查詢條件中包含學生，需要驗證以獲取學生票價**\n" 
    else:
        info_StudentOrNot = ""

    if arrive_time == "":   # 單向航程
        info_GoTripDepartTime = browser.find_element(By.XPATH,GoTripDepartTimeXPATH).text                   # 去程出發時間
        info_GoTripArriveTime = browser.find_element(By.XPATH,GoTripArriveTimeXPATH).text                   # 去程抵達時間
        info_GoTripDepartAirport = browser.find_element(By.XPATH,GoTripDepartAirportXPATH).text             # 去程出發機場
        info_GoTripArriveAirport = browser.find_element(By.XPATH,GoTripArriveAirportXPATH).text             # 去程抵達機場
        info_GoTripDirectFlightOrNot = browser.find_element(By.XPATH,GoTripDirectFlightOrNotXPATH).text     # 去程航班直飛與否?
        info_GoTripTotalTime = browser.find_element(By.XPATH,GoTripTotalTimeXPATH).text                     # 去程總時長
        info_AirlineName = browser.find_element(By.XPATH,AirlineNameXPATH).text                             # 航空公司名
        info_TotalPricePerPerson = browser.find_element(By.XPATH,TotalPricePerPersonXPATH).text             # 總價格(/人)
        flightResult = f'''{info_StudentOrNot}去程\n時間:{info_GoTripDepartTime}-{info_GoTripArriveTime}\n出發機場:{info_GoTripDepartAirport}\n目的地機場:{info_GoTripArriveAirport}\n直飛航班or轉機:{info_GoTripDirectFlightOrNot}\n總飛行時間:{info_GoTripTotalTime}
====================\n航空公司:{info_AirlineName}\n價格:{info_TotalPricePerPerson}/人\n'''
    else:   # 雙向航程
        info_GoTripDepartTime = browser.find_element(By.XPATH,GoTripDepartTimeXPATH).text                   # 去程出發時間
        info_GoTripArriveTime = browser.find_element(By.XPATH,GoTripArriveTimeXPATH).text                   # 去程抵達時間
        info_GoTripDepartAirport = browser.find_element(By.XPATH,GoTripDepartAirportXPATH).text             # 去程出發機場
        info_GoTripArriveAirport = browser.find_element(By.XPATH,GoTripArriveAirportXPATH).text             # 去程抵達機場
        info_GoTripDirectFlightOrNot = browser.find_element(By.XPATH,GoTripDirectFlightOrNotXPATH).text     # 去程航班直飛與否?
        info_GoTripTotalTime = browser.find_element(By.XPATH,GoTripTotalTimeXPATH).text                     # 去程總時長
        info_BackTripDepartTime = browser.find_element(By.XPATH,BackTripDepartTimeXPATH).text               # 返程出發時間
        info_BackTripArriveTime = browser.find_element(By.XPATH,BackTripArriveTimeXPATH).text               # 返程抵達時間
        info_BackTripDepartAirport = browser.find_element(By.XPATH,BackTripDepartAirportXPATH).text         # 返程出發機場
        info_BackTripArriveAirport = browser.find_element(By.XPATH,BackTripArriveAirportXPATH).text         # 返程抵達機場
        info_BackTripDirectFlightOrNot = browser.find_element(By.XPATH,BackTripDirectFlightOrNotXPATH).text # 返程直飛與否?
        info_BackTripTotalTime = browser.find_element(By.XPATH,BackTripTotalTimeXPATH).text                 # 返程總時長
        info_AirlineName = browser.find_element(By.XPATH,AirlineNameXPATH).text                             # 航空公司名
        info_TotalPricePerPerson = browser.find_element(By.XPATH,TotalPricePerPersonXPATH).text             # 總價格(/人)
        flightResult = f'''{info_StudentOrNot}去程\n時間:{info_GoTripDepartTime}-{info_GoTripArriveTime}\n出發機場:{info_GoTripDepartAirport}\n目的地機場:{info_GoTripArriveAirport}\n直飛航班or轉機:{info_GoTripDirectFlightOrNot}\n總飛行時間:{info_GoTripTotalTime}
====================\n返程\n時間:{info_BackTripDepartTime}-{info_BackTripArriveTime}\n出發機場:{info_BackTripDepartAirport}\n目的地機場:{info_BackTripArriveAirport}\n直飛航班or轉機:{info_BackTripDirectFlightOrNot}\n總飛行時間:{info_BackTripTotalTime}
====================\n航空公司:{info_AirlineName}\n價格:{info_TotalPricePerPerson}/人\n'''
    print(flightResult)
    return flightResult

def get_Reco_Flight(): # 獲取最便宜/超值/最快三項簡易資訊
    print("推薦航班資訊")
    print("==========================")
    result_Reco = browser.find_elements(By.CLASS_NAME,"Hv20-option")
    for z in result_Reco:
        print(z.text)
    reco_Result_Message = "\n推薦航班資訊\n====================\n" + "\n".join(a.text for a in result_Reco)
    return reco_Result_Message

def get_Cheapest_Flight():  # 獲取最便宜航空資訊
    print("最優惠航班資訊")
    print("============")
    cheapest_Result_Summary = browser.find_element(By.XPATH,cheapestFlightSummary_XPATH) #cheapest_result_box_summary
    cheapest_Result_Summary.click() #click cheapest_result_box
    sleep(3)
    #result_Cheapest = browser.find_elements(By.XPATH,flightInfo_XPATH) #get cheapest flight info
    #for j in result_Cheapest:
    #    print(j.text)
    cheapest_Result_Message = "\n最優惠航班資訊\n====================\n" + get_Flight_Result() + "詳細資訊請點擊下方連結\n" + url_Price
    return cheapest_Result_Message

def get_Best_Flight():  # 獲取最佳(超值)航空資訊
    print("超值航班資訊")
    print("===========")
    best_Result_Summary = browser.find_element(By.XPATH,bestFlightSummary_XPATH) #best_result_box_summary
    best_Result_Summary.click() #click best_result_box
    sleep(3)
    # result_Best = browser.find_elements(By.XPATH,flightInfo_XPATH) #get best flight info
    # for i in result_Best:
    #     print(i.text)
    best_Result_Message = "\n超值航班資訊\n====================\n" + get_Flight_Result() + "詳細資訊請點擊下方連結\n" + url_Best
    return best_Result_Message

def get_Fast_Flight(): # 獲取最快航空資訊
    print("最快航班資訊")
    print("===========")
    fast_Result_Summary = browser.find_element(By.XPATH,fastFlightSummary_XPATH) #fast_result_box_summary
    fast_Result_Summary.click() #click fast_result_box
    sleep(3)
    # result_Fast = browser.find_elements(By.XPATH,flightInfo_XPATH) #get fast flight info
    # for k in result_Fast:
    #     print(k.text)
    fast_Result_Message = "\n最快航班資訊\n====================\n" + get_Flight_Result() + "詳細資訊請點擊下方連結\n" + url_Duration
    return fast_Result_Message

#LineNotify
def lineNotify(token, msg):
    headers = {
        "Authorization" : "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message' : msg}
    r = requests.post("https://notify-api.line.me/api/notify",headers = headers, params = payload)
    print(r.status_code)
    return r.status_code #return 200->success

def main():
    #reco_Flight_Result = get_Reco_Flight()
    cheapest_Flight_Result = get_Cheapest_Flight()
    best_Flight_Result = get_Best_Flight()
    fast_Flight_Result = get_Fast_Flight()
    lineNotify(token, search_Info) #Send current setting Info
    sleep(2)
    #lineNotify(token, reco_Flight_Result) #Send Recommendation Info
    #sleep(2)
    lineNotify(token, cheapest_Flight_Result) #Send Cheapest Flight Info
    sleep(2)
    lineNotify(token, best_Flight_Result) #Send Best Flight Info
    sleep(2)
    lineNotify(token, fast_Flight_Result) #Send Fast Flight Info
    sleep(2)

main()