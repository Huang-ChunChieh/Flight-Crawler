<h1 align="center">
    Flight-Crawler
</h1>

<p align="center">
A simple LineNotify & LineBot for querying airlines.
</p>

<p align="center">
    <a href="#line-Notify">Line Notify</a>
    ·
    <a href="#line-bot">Line Bot</a>
    ·
    <a href="ngrok">Ngrok</a>
</p>

## Line Notify
<p align="center">
	<img src="https://github.com/Huang-ChunChieh/Flight-Crawler/blob/main/linenotify.gif" width="200" alt="screenshot">
</p>

- Register [LINE Notify](https://notify-bot.line.me/)
- Generate Token & Fill in the token in `linenotify_aiirline.py`
- Setting file(depart_city/arrive_city/depart_time...)
- Run file and get flight!

## Line Bot
<p align="center">
	<img src="https://github.com/kuanhaolin/Flight-Crawler/blob/main/linebot.gif" width="200" alt="screenshot">
</p>

- Register [LINE Developer](/https://developers.line.biz/zh-hant/)
- Create Provider
- Create Channel
- Generate Access Token & Channel Secret for program

## Ngrok
- Register ngrok and generate token
- Native environment using [Ngrok](/ngrok-v3-stable-windows-amd64.zip)
- Setting server
``` 
#ngrok config add-authtoken <token>
#ngrok http http://127.0.0.1:5000
``` 
- Push public URL to LINE BOT(Webhook setting)
