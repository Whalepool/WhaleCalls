#!/usr/bin/python3

from twitter import *
from email.utils import parsedate
import ts3
import time
import datetime
from telegram import *
import telegram
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

def is_number(s):
   try:
        int(s)
        return True
   except:
        return False
 
def addcommas(string):
    words=string.split()
    newcall=""
    for word in words:
        if is_number(word) == True:
            word2="{:,}".format(int(word))
            newcall = newcall + " " + word2
        else:
            newcall = newcall + " " + word
    return str(newcall[1:])


t = Twitter(auth=OAuth('xxxx', 'zzz', 'yyyyy', 'iiiii'))

# fetch last update id from external file
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastmexupdate.txt', encoding='utf-8')
latestid = f.readline().strip()
f.close()

if (latestid == ""):
	latestid=1

# grab tl updates
updates=timeline=t.statuses.user_timeline(screen_name="bitmexrekt", count=100)
wclist=list()
#loop through updates
for update in reversed(updates):
	text = update['text']
	tweetid = str(update['id'])
	print(tweetid)
	if (int(latestid) < int(tweetid)) and (text.split()[0] == "Liquidated"):
		timestamp = update['created_at']
		direction = text.split()[1]
		symbol = text.split()[3]
		symbol=symbol[:-1]
		#amount = addcommas(text.split()[5])

		price = text.split()[7]
		pricef = float(price)
		latestid=tweetid
		amountf = int(text.split()[5].replace(',',''))
		amount = addcommas(str(amountf))
		marginlost100 = addcommas(str(int(0.01*amountf))) 
		marginlost50 = addcommas(str(int(0.02*amountf)))
		#bmexcash24=str(int(pricef*amountf*0.00001*0.005))
		#bmexcash7D=str(pricef*amountf*0.00001*0.01))
		if (amountf<40000):
			continue
		if symbol[:3] == "XBT":
			#total = total + float(bmexcash24)
			wcallmex="BitMEX " + symbol + " futures has liquidated a " + direction + " position of " + amount + " contracts ($" + amount  + ") at " + price + ". Margin lost: $" + marginlost100 + "@100x; $" + marginlost50 + "@50x  -- " + timestamp
			wclist.append(wcallmex)
		f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastmexupdate.txt', '+w', encoding='utf-8')
		f.write(latestid)
		f.close()


if not wclist:
	f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastmexupdate.txt', 'w+', encoding='utf-8')
	f.write(str(latestid))
	f.close()

else:
	with ts3.query.TS3Connection("158.69.115.146", 2009) as ts3conn:
		try:
			ts3conn.login(
			client_login_name="xxx",
			client_login_password="xxxxx"
			)
		except ts3.query.TS3QueryError as err:
			print("Login failed:", err.resp.error["msg"])
			exit(1)
		ts3conn.use(sid=778)
		ts3conn.clientupdate(client_nickname="[WhaleCalls-BOT]")
		token='153606345:AAGDdKnw41oLce5axJfKlqutMEnnb5jfnAQ'
		bot=telegram.Bot(token=token)
		resp = ts3conn.whoami()
		client_id=resp[0]['client_id']
		for s in wclist:
			wcall=s
			bot.sendMessage(chat_id=-1001012147388, text=wcall)
			bot.sendMessage(chat_id="@whalecalls", text=wcall)
			bot.sendMessage(chat_id="@whalepoolbtcfeed", text=wcall)
			if "long" in wcall:
				#ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=44184, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=56600, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=57474, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
			else:
				#ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=44184, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=56600, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=57474, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
		ts3conn.quit()

f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastmexupdate.txt', '+w', encoding='utf-8')
f.write(latestid)
f.close()
