<h1 align="center">
    Flight-Crawler
</h1>

<h3 align="center">
A simple LineNotify & LineBot for querying airlines.
</h3>
<p align="center">
    <a href="#line-notify">Line Notify</a>
    ·
    <a href="#line-developer">Line Developer</a>
    ·
    <a href="#ngrok">Ngrok</a>
</p>

# Line Notify Setting
<p align="center">
	<img src="https://github.com/Huang-ChunChieh/Flight-Crawler/blob/main/linenotify.gif" width="200" alt="screenshot">
</p>

* Register & Login [LINE Notify](https://notify-bot.line.me/)
* Generate Token & Fill in the token in `linenotify_airline.py`
* Setting file(depart_city/arrive_city/depart_time...)
* Run `linenotify_airline.py` and get flight info!


# LineBot Setting 

## Line Developer
<p align="center">
	<img src="https://github.com/Huang-ChunChieh/Flight-Crawler/blob/main/linebot.gif" width="200" alt="screenshot">
</p>

* Register & Login [LINE Developer](https://developers.line.biz/zh-hant/)
* Create Provider
* Create New Channel
  - **Channel type** - Messaging API
  - **Provider** - Select Provider U create
  - Complete the remaining settings
* Click Channel U create
  - **Basic setting** - Copy Channel secret
  - **Messaging API** - Generate & Copy Channel access token
* Fill in **Channel secret** & **Channel access token** in `linebot_airline.py`

## Ngrok
* Register & Login ngrok and Generate token
  - Register & Login [ngrok](https://ngrok.com/)
  - Download Ngrok from website or Unzip [file](/ngrok-v3-stable-windows-amd64.zip)
  - Copy your [Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
* Authenticate your ngrok agent using [ngrok.exe](/ngrok-v3-stable-windows-amd64.zip)
  - Setting server(Following the [Website](https://dashboard.ngrok.com/get-started/your-authtoken))
	``` 
	#ngrok config add-authtoken <your_token>
	#ngrok http http://127.0.0.1:5000
	```
  -  Should Generate **Public URL** after server setting
* Update **Public URL** to [LINE BOT(Webhook settings)](https://developers.line.biz/zh-hant/)
  - Click Channel U create --> Messaging API settings --> Webhook settings
  - Fill in **Public URL**
  - Enabled **Use webhook**

## After Complete [Line Developer](#line-developer) & [Ngrok](#ngrok)
* Run `linebot_airline.py` and Chat with linebot to get flight info!
