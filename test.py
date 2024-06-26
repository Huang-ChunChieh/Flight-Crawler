from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    #獲取收到的訊息內容
    try:
        json_data = json.loads(body)
        #json格式化訊息內容
        channel_Access_Token = 'XXX'
        channel_Secret = 'XXX'
        line_bot_api = LineBotApi(channel_Access_Token)
        #Confirm Channel Access Token
        handler = WebhookHandler(channel_Secret)
        #Confirm Channel Secret 
        signature = request.headers['X-Line-Signature']      
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        if type=='text':
            msg = json_data['events'][0]['message']['text']  
            #取得LINE收到的文字訊息
            reply = fun0(msg)
        else:
            reply = '格式錯誤 請以文字格式傳輸'
        print(reply)
        line_bot_api.reply_message(tk,TextSendMessage(reply))
        #回傳訊息
    except:
        print(body)
    return 'OK'

def display_cities_by_region(region):
    df = pd.read_csv('city.csv', sep=' ')
    filtered_df = df[df['地區'] == region]
    filtered_df = filtered_df.to_string(index=False)
    #更改filtered_df(Any)類型為str
    #print(filtered_df)
    return filtered_df

def region_Result(msg):
    region = msg[1]
    return display_cities_by_region(region)

def flight_Result(msg):
    depart_city = msg[1] #出發地
    arrive_city = msg[2] #目的地
    depart_time = msg[3] #去程時間 XXXX(西元年)/XX(月)/XX(日)
    arrive_time = msg[4] #返程時間 XXXX(西元年)/XX(月)/XX(日)  若為單程則此欄為""
    cabinclass = msg[5] #艙等 經濟艙:""/特選經濟艙:"premium"/商務艙:"business"/頭等艙:"first"
    directflight = msg[6] #是否僅限直飛航班 若是->True  若否->False
    #=========Numbers of Travelers=========#
    numOfAdult = msg[7] #成人數量
    numOfStudent = msg[8] #18歲以上學生數量
    numOfTeenager = msg[9] #青少年(12-17歲)數量
    numOfChild = msg[10] #兒童(2-11)數量
    numOfBaby1S = msg[11] #2歲以下佔坐兒童數量
    numOfBaby1L = msg[12] #2歲以下不佔坐兒童數量
    #==========================================================================#
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
    #==========================================================================#
    if cabinclass == "premium":
        classtype = "特選經濟艙"
    elif cabinclass == "business":
        classtype = "商務艙"
    elif cabinclass == "first":
        classtype = "頭等艙"
    else:
        classtype = "經濟艙"
    #==========================================================================#
    if directflight == True:
        fdDir = "fs=fdDir=true;stops=~0"
        directFlight = "是"
    else:
        fdDir = ""
        directFlight = "否"
    #==========================================================================#
    search_Info = f"""目前查詢條件\n出發地:{depart_city}\n目的地:{arrive_city}\n出發日期:{depart_time}\n抵達日期:{arrive_time}\n艙等:{classtype}\n僅限直飛航班:{directFlight}\n旅客人數\n成人:{str(numOfAdult)}人\n學生:{str(numOfStudent)}人\n青少年:{str(numOfTeenager)}人\n兒童:{str(numOfChild)}人\n2歲以下佔坐嬰兒:{str(numOfBaby1S)}人\n2歲以下不佔坐嬰兒:{str(numOfBaby1L)}人\n\n"""

    #若人數設定中students非0，則會多顯示需驗證學生身分內容，XPATH需重新定位
    if numOfStudent >= 1:
        cheapestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[1]'
        bestFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[2]'
        fastFlightSummary_XPATH = '//*[@id="listWrapper"]/div/div[2]/div[3]'
        #flightInfo_XPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div'
        GoTripDepartTimeXPATH = '//*[@id="listWrapper"]/div/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/ol/li[1]/div/div/div[3]/div[1]/span[1]'
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
    else:
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


    #URL Setting
    url = f"https://www.tw.kayak.com/flights/{depart_city}-{arrive_city}/{depart_time}/{arrive_time}/{cabinclass}/{adult}/{student}/{children}?{fdDir}"
    url_Price = url + "&sort=price_a"
    url_Best = url + "&sort=bestflight_a"
    url_Duration = url + "&sort=duration_a"
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(10)

    def get_Flight_Result():
        info_GoTripDepartTime = browser.find_element(By.XPATH,GoTripDepartTimeXPATH).text
        info_GoTripArriveTime = browser.find_element(By.XPATH,GoTripArriveTimeXPATH).text
        info_GoTripDepartAirport = browser.find_element(By.XPATH,GoTripDepartAirportXPATH).text
        info_GoTripArriveAirport = browser.find_element(By.XPATH,GoTripArriveAirportXPATH).text
        info_GoTripDirectFlightOrNot = browser.find_element(By.XPATH,GoTripDirectFlightOrNotXPATH).text
        info_GoTripTotalTime = browser.find_element(By.XPATH,GoTripTotalTimeXPATH).text
        info_BackTripDepartTime = browser.find_element(By.XPATH,BackTripDepartTimeXPATH).text
        info_BackTripArriveTime = browser.find_element(By.XPATH,BackTripArriveTimeXPATH).text
        info_BackTripDepartAirport = browser.find_element(By.XPATH,BackTripDepartAirportXPATH).text
        info_BackTripArriveAirport = browser.find_element(By.XPATH,BackTripArriveAirportXPATH).text
        info_BackTripDirectFlightOrNot = browser.find_element(By.XPATH,BackTripDirectFlightOrNotXPATH).text
        info_BackTripTotalTime = browser.find_element(By.XPATH,BackTripTotalTimeXPATH).text
        info_AirlineName = browser.find_element(By.XPATH,AirlineNameXPATH).text
        info_TotalPricePerPerson = browser.find_element(By.XPATH,TotalPricePerPersonXPATH).text
        if numOfStudent >= 1:
            info_StudentOrNot = "**查詢條件中包含學生，需要驗證以獲取學生票價**\n"
        else:
            info_StudentOrNot = ""
        flightResult = f'''{info_StudentOrNot}去程\n時間:{info_GoTripDepartTime}-{info_GoTripArriveTime}\n出發機場:{info_GoTripDepartAirport}\n目的地機場:{info_GoTripArriveAirport}\n直飛航班or轉機:{info_GoTripDirectFlightOrNot}\n總飛行時間:{info_GoTripTotalTime}
====================\n返程\n時間:{info_BackTripDepartTime}-{info_BackTripArriveTime}\n出發機場:{info_BackTripDepartAirport}\n目的地機場:{info_BackTripArriveAirport}\n直飛航班or轉機:{info_BackTripDirectFlightOrNot}\n總飛行時間:{info_BackTripTotalTime}
====================\n航空公司:{info_AirlineName}\n價格:{info_TotalPricePerPerson}/人\n'''
        print(flightResult)
        return flightResult

    def get_Reco_Flight(): #獲取最便宜/超值/最快三項簡易資訊
        print("推薦航班資訊")
        print("==========================")
        result_Reco = browser.find_elements(By.CLASS_NAME,"Hv20-option")
        for z in result_Reco:
            print(z.text)
        reco_Result_Message = "\n推薦航班資訊\n==== ==== ====\n" + "\n".join(a.text for a in result_Reco)
        return reco_Result_Message

    def get_Cheapest_Flight():
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

    def get_Best_Flight():
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

    def get_Fast_Flight():
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

    return search_Info + get_Reco_Flight() + get_Cheapest_Flight() + get_Best_Flight() + get_Fast_Flight()

def help(msg):
    return "輸入1+[區域]  顯示各地區機場\n範例: 1 東北亞\n\n輸入2+[設定格式]  顯示機票\n範例: 2 TPE KIX 2024-07-01 2024-07-04"

outfit_suggestions = {
    '1' : region_Result,
    '2' : flight_Result,
    'help' : help
}

def fun0(msg):
    fun_num = msg.split(" ")
    return outfit_suggestions.get(fun_num[0], lambda: '無')(fun_num)

if __name__ == "__main__":
    app.run()