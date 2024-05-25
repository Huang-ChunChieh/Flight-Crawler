from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    #取得收到的訊息內容
    try:
        json_data = json.loads(body)
        #json格式化訊息內容
        access_token = 'XXX'
        secret = 'XXX'
        line_bot_api = LineBotApi(access_token)
        #確認token
        handler = WebhookHandler(secret)
        #確認secret 
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

def fun1(msg):
    region = msg[1]
    return display_cities_by_region(region)

def fun2(msg):
    depart_city = msg[1] #出發地
    arrive_city = msg[2] #目的地
    depart_time = msg[3] #去程時間 XXXX(西元年)/XX(月)/XX(日)
    arrive_time = "" #返程時間 XXXX(西元年)/XX(月)/XX(日)  若為單程則此欄為""
    cabinclass = "" #艙等 經濟艙:""/特選經濟艙:"premium"/商務艙:"business"/頭等艙:"first"
    directflight = False #是否僅限直飛航班 若是->True  若否->False
    #===============旅客數量===============#
    numOfAdult = 1 #成人數量
    numOfStudent = 0 #18歲以上學生數量
    numOfTeenager = 0 #青少年(12-17歲)數量
    numOfChild = 0 #兒童(2-11)數量
    numOfBaby1S = 0 #2歲以下佔坐兒童數量
    numOfBaby1L = 0 #2歲以下不佔坐兒童數量
    #=====================================#
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
    #=====================================#
    if cabinclass == "premium":
        classtype = "特選經濟艙"
    elif cabinclass == "business":
        classtype = "商務艙"
    elif cabinclass == "first":
        classtype = "頭等艙"
    else:
        classtype = "經濟艙"
    #=====================================#
    if directflight == True:
        fdDir = "fs=fdDir=true;stops=~0"
    else:
        fdDir = ""
    #=====================================#
    search_Info = f"""目前查詢條件\n出發地:{depart_city}\n目的地:{arrive_city}\n出發日期:{depart_time}\n抵達日期:{arrive_time}艙等:{classtype}\n旅客人數\n成人:{str(numOfAdult)}人\n學生:{str(numOfStudent)}人\n青少年:{str(numOfTeenager)}人\n兒童:{str(numOfChild)}人\n2歲以下佔坐嬰兒:{str(numOfBaby1S)}人\n2歲以下不佔坐嬰兒:{str(numOfBaby1L)}人"""

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

    #URL Setting
    url = f"https://www.tw.kayak.com/flights/{depart_city}-{arrive_city}/{depart_time}/{arrive_time}/{cabinclass}/{adult}/{student}/{children}?{fdDir}"
    url_Price = url + "&sort=price_a"
    url_Best = url + "&sort=bestflight_a"
    url_Duration = url + "&sort=duration_a"
    browser = webdriver.Chrome()
    browser.get(url)
    #sleep(10)

    def get_Reco_Flight(): #獲取最便宜/超值/最快三項簡易資訊
        print("推薦航班資訊")
        print("==========================")
        result_Reco = browser.find_elements(By.CLASS_NAME,"Hv20-option")
        for z in result_Reco:
            print(z.text)
        reco_Result_Message = "推薦航班資訊\n==== ==== ====\n" + "\n".join(a.text for a in result_Reco)
        return reco_Result_Message

    def get_Cheapest_Flight():
        print("最優惠航班資訊")
        print("============")
        cheapest_Result_Summary = browser.find_element(By.XPATH,cheapestFlightSummary_XPATH) #cheapest_result_box_summary
        cheapest_Result_Summary.click() #click cheapest_result_box
        #sleep(3)
        result_Cheapest = browser.find_elements(By.XPATH,flightInfo_XPATH) #get cheapest flight info
        for j in result_Cheapest:
            print(j.text)
        cheapest_Result_Message = "最優惠航班資訊\n==== ==== ====\n" + j.text + "詳細資訊請點擊下方連結\n" + url_Price
        return cheapest_Result_Message

    def get_Best_Flight():
        print("超值航班資訊")
        print("===========")
        best_Result_Summary = browser.find_element(By.XPATH,bestFlightSummary_XPATH) #best_result_box_summary
        best_Result_Summary.click() #click best_result_box
        #sleep(3)
        result_Best = browser.find_elements(By.XPATH,flightInfo_XPATH) #get best flight info
        for i in result_Best:
            print(i.text)
        best_Result_Message = "超值航班資訊\n==== ==== ====\n" + i.text + "詳細資訊請點擊下方連結\n" + url_Best
        return best_Result_Message

    def get_Fast_Flight():
        print("最快航班資訊")
        print("===========")
        fast_Result_Summary = browser.find_element(By.XPATH,fastFlightSummary_XPATH) #fast_result_box_summary
        fast_Result_Summary.click() #click fast_result_box
        #sleep(3)
        result_Fast = browser.find_elements(By.XPATH,flightInfo_XPATH) #get fast flight info
        for k in result_Fast:
            print(k.text)
        fast_Result_Message = "最快航班資訊\n==== ==== ====\n" + k.text + "詳細資訊請點擊下方連結\n" + url_Duration
        return fast_Result_Message

    return search_Info + get_Reco_Flight() + get_Cheapest_Flight() + get_Best_Flight() + get_Fast_Flight()

def help(msg):
    return "開頭輸入1 顯示各地區機場\n範例: 1 東北亞\n開頭輸入2 顯示機票\n範例 2 TPE KIX 2024-07-01"

outfit_suggestions = {
    '1' : fun1,
    '2' : fun2,
    'help' : help
}

def fun0(msg):
    fun_num = msg.split(" ")
    return outfit_suggestions.get(fun_num[0], lambda: '無')(fun_num)

if __name__ == "__main__":
    app.run()