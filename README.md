<h3 align="center">
    Flight-Crawler
</h3>

<p align="center">
A simple Line Bot for querying airlines.
</p>

<p align="center">
    <a href="#line-bot">Line Bot</a>
    ·
    <a href="ngrok">Ngrok</a>
 </p>

 <p align="center">
	<img src="https://github.com/Huang-ChunChieh/Flight-Crawler/blob/main/linebot.gif" width="550" alt="screenshot">
</p>

## Line Bot
Register [LINE Developer](/https://developers.line.biz/zh-hant/)
Create Provider
Create Channel
Generate Access Token & Channel Secret for program

## Ngrok
Register ngrok and generate token
Native environment using [ngrok](/ngrok-v3-stable-windows-amd64.zip)
Setting server
``` 
#ngrok config add-authtoken <token>
#ngrok http http://127.0.0.1:5000
``` 
Push public URL to LINE BOT(Webhook setting)