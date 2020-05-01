#crontab으로 20~30분마다...?
#업데이트를 체크한 뒤, 결과가 200이 아니면 경고.
#결과가 200이라면 최신 /tmp의 게시판 번호 이상의 모든 게시글을 가져온다.

import bot
import requests
import sys


if len(sys.argv) == 1:
	latest = 0
else:
	latest = int(sys.argv[1])


f = open("./site_link", 'r')
URL = f.readline()
f.close()

response = requests.get(URL)
# print("CODE : ",response.status_code)

if response.status_code != 200 :
	err = "서버 에러인지 확인하자 : %d" % response.status_code
	# print(err)
	bot.send(err)
	# exec("python /send.py '%s'" % err)
	import sys
	sys.exit()

# print(response.text)
# tableFrom = response.text.find("class=\"bd_lst bd_tb_lst bd_tb\"")
# tableTo = response.text.find("<div class=\"btm_mn clear\">")


# 정규식으로 검색
from bs4 import BeautifulSoup
html = BeautifulSoup(response.text, 'html.parser')


lists = html.find('table',{'class':'bd_lst bd_tb_lst bd_tb'}).find('tbody')


# print(lists)

rNum = "href=\"/game_news/()\" class=\"hx"
rFree = "<td class=\"cate\"><span style=\"color:#0000bf\">()</span>"


list = []
maxArt = latest
for idx, l in enumerate(lists.find_all('tr')[0:]):
	
	n = int(l.find('a')['href'][11:])

	maxArt = max(n,maxArt)
	if n <= latest :
		# last = "%s.. 이미 읽은 게시물입니다" % n
		# print(last)
		continue
		# bot.send(last)
	
	if l.find('td',{'class':'cate'}).text != '무료':
		continue
	
	if  l.find('span').get_text().strip() == '기타' :
		producer = '기타'
	else :
		producer = l.find('span').find('img')['title']
	
	title = l.find('a')['title']
	url = "%s%d" % (URL,n)
	list.append("(%s) %s\n=>%s\n\n" % (producer,title,url))

if len(list) != 0:
	bot.send('\n'.join(list))

print(maxArt)