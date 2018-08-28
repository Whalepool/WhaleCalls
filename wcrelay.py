#!/usr/bin/python3

from twitter import *
from email.utils import parsedate
import ts3
import time
import datetime
from telegram import *
import telegram

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

t = Twitter(auth=OAuth('xxx', 'yyyy', 'zzzz', 'iiiiii'))

# grab tl updates
updates=timeline=t.statuses.user_timeline(screen_name="whalecalls")

# fetch last update id from external file
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastupdate1.txt', encoding='utf-8')
latestid = f.readline().strip()
f.close()

ts=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

# create newcall array
wclist=list()
relaylist=list()
#loop through updates
for update in reversed(updates):
	#crt = parsedate(update['created_at'])
	theid = update['id']
	print(theid)
	crt = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(update['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
	#if ("margin usage" in update['text']):
	#	f = open('lastmarg.txt', encoding='utf-8')
	#	lasttime = f.readline().strip()
	#	f.close()
	#	timediff=time.mktime(time.strptime(crt,'%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime(lasttime,'%Y-%m-%d %H:%M:%S'))
	#	f = open('lastmarg.txt', 'w+', encoding='utf-8')
	#	f.write(str(crt))
	#	f.close()
		#print(timediff)
	if (int(theid) > int(latestid)):
		#print(update)
		text = update['text']
		if text.startswith("@") or text.startswith(".") or 'retweeted_status' in update:
			continue
		whalecallsupdate=text
		whalecallsupdate=whalecallsupdate.replace("@okcoinbtc", "OKCoin")
		whalecallsupdate=whalecallsupdate.replace("$btcusd", "BTCUSD")
		whalecallsupdate=whalecallsupdate.replace("$BTCUSD", "BTCUSD")
		whalecallsupdate=whalecallsupdate.replace("$LTCUSD", "LTCUSD")
		whalecallsupdate=whalecallsupdate.replace("@OKCoinBTC", "OKCoin")
		whalecallsupdate=whalecallsupdate.replace("Okcoin", "OKCoin")
		whalecallsupdate=whalecallsupdate.replace("OKcoin", "OKCoin")
		whalecallsupdate=whalecallsupdate.replace("@bitfinex", "Bitfinex")
		whalecallsupdate=whalecallsupdate.replace("$BTCCNY", "BTCCNY")
		# removed to fix non plural contracts from OKcoin tweets, example: Okcoin $BTCUSD Weekly futures has liquidated a short position of 2873 contract at 7,088.16 
		# whalecallsupdate=whalecallsupdate.replace("contract at", "contracts at")
		if "has liquidated" in whalecallsupdate:
			if "Bi Weekly" in whalecallsupdate:
				amountf = float(whalecallsupdate.split()[11])
			else:
				amountf = float(whalecallsupdate.split()[10])

			amountusd=int(amountf*100)
			amountmargin=int(amountusd/20)
			amountmargin2=int(amountusd/10)
			whalecallsupdate=whalecallsupdate.replace("contracts", "contracts ($" + addcommas(str(amountusd)) + ")")
			whalecallsupdate=whalecallsupdate.replace(" - ", ". Margin lost: $" + addcommas(str(amountmargin)) + "@20x; $" + addcommas(str(amountmargin2)) + "@10x - ")
		wclist.append(whalecallsupdate)
		#print(whalecallsupdate)
		latestid = theid
		relaylist.append(str(latestid))
		f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastupdate1.txt', 'w+', encoding='utf-8')
		f.write(str(latestid))
		f.close()
		print("relay2")
		f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/relaylogs.txt', 'a', encoding='utf-8')
		f.write(str(crt) + " - NEW TWEET FOUND - " + str(latestid) + "\n")
		f.close()

if not wclist:
	# print("bleh")
	f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastupdate1.txt', 'w+', encoding='utf-8')
	f.write(str(latestid))
	f.close()
else:
	token='zzzzzzz'
	bot=telegram.Bot(token=token) 
	for s in wclist:
		wcall=addcommas(s)
		bot.sendMessage(chat_id=-1001012147388, text=wcall)
		bot.sendMessage(chat_id="@whalecalls", text=wcall)
		bot.sendMessage(chat_id="@whalepoolbtcfeed", text=wcall)

	with ts3.query.TS3Connection("158.69.115.146", 2009) as ts3conn:
		try:
			ts3conn.login(
			client_login_name="zzzz",
			client_login_password="zzzzz"
			)
		except ts3.query.TS3QueryError as err:
			print("Login failed:", err.resp.error["msg"])
			exit(1)
		ts3conn.use(sid=778)
		ts3conn.clientupdate(client_nickname="[WhaleCalls-BOT]")

		
		for s in wclist:

			wcall=addcommas(s)
			#bot.sendMessage(chat_id=-1001012147388, text=wcall)
			#bot.sendMessage(chat_id="@whalecalls", text=wcall)
			#bot.sendMessage(chat_id="@whalepoolbtcfeed", text=wcall)
			#Code to format for Teamspeak
			wcall=wcall.replace(" 5m", " [b]5m[/b]")
			wcall=wcall.replace(" 15m", " [b]15m[/b]")
			wcall=wcall.replace(" 1h", " [b]1h[/b]")
			wcall=wcall.replace(" r1", " [b]r1[/b]")
			wcall=wcall.replace(" r2", " [b]r2[/b]")
			wcall=wcall.replace(" r3", " [b]r3[/b]")
			wcall=wcall.replace(" s1", " [b]s1[/b]")
			wcall=wcall.replace(" s2", " [b]s2[/b]")
			wcall=wcall.replace(" s3", " [b]s3[/b]")
			wcall=wcall.replace(" 6h", " [b]6h[/b]")
			wcall=wcall.replace(" 12h", " [b]12h[/b]")
			wcall=wcall.replace(" 24h", " [b]24h[/b]")
			wcall=wcall.replace(" pivot:", " [u]pivot[/u]:")

			resp = ts3conn.whoami()
			client_id=resp[0]['client_id']
			if "liquidated" in wcall and "long" in wcall:
				#ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=44184, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=56600, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
				ts3conn.clientmove(cid=57474, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=red]" + wcall)
			elif "liquidated" in wcall and "short" in wcall:
				#ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=44184, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=56600, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
				ts3conn.clientmove(cid=57474, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg="[b][color=green]" + wcall)
			else:
				#ts3conn.sendtextmessage(targetmode=2, target=1, msg=wcall)
				ts3conn.clientmove(cid=44184, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg=wcall)
				ts3conn.clientmove(cid=56600, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg=wcall)
				ts3conn.clientmove(cid=57474, clid=client_id)
				ts3conn.sendtextmessage(targetmode=2, target=1, msg=wcall)

		ts3conn.quit()
		print("relay2")
		f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/relaylogs.txt', 'a', encoding='utf-8')
		f.write("Teamspeak & tg messages sent.\n")
		f.close()


f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/lastupdate1.txt', 'w+', encoding='utf-8')
f.write(str(latestid))
f.close()
print("relay3")
f = open('/home/ubuntu/volume1/stakepool/teamspeakbots/relaylogs.txt', 'a', encoding='utf-8')
f.write(str(ts) + " - " + str(latestid) + "\n")
f.close()
