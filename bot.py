import telepot #모듈 임포트

def send(msg):
	#봇 API Token
	
	f = open("./api_token", 'r')
	token = f.readline()
	f.close()

	#target ID
	f = open("./target", 'r')
	mc = f.readline()
	f.close()
	bot = telepot.Bot(token)


	bot.sendMessage(mc,"test")
	bot.sendPhoto(mc,"https://steamcdn-a.akamaihd.net/steam/apps/57300/header.jpg?t=1574253555",disable_notification=True)