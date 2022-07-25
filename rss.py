import sqlite3, feedparser, os, asyncio, logging
from aiogram import Bot, Dispatcher, executor
from telegram import ParseMode
scriptDir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(scriptDir + '/bd_rss.sqlite3')
db = db_connection.cursor()

#Token telegram bot
TOKEN_BOT = '' 
#id user to send rss
ID_USER = ['']
#url feed
URL = ''

bot = Bot(token=TOKEN_BOT)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

feed_url = URL
bot_id = ID_USER

async def bot_send(title, link, iduser):
	result= "<b>"+title + "</b>\n\n"  + link
	await bot.send_message(iduser, result, parse_mode=ParseMode.HTML)

def update_id(postid):
	db.execute("UPDATE bd SET idbd = ?", (int(postid), ) )
	db_connection.commit()


def is_has(postid):
	db.execute("SELECT idbd from bd")
	for row in db.fetchall():
		idbd = row[0]
	db_connection.commit()
	if str(idbd) < str(postid):
		return True
	else:
		return False


async def feed():
	feed = feedparser.parse(feed_url)
	n = 0
	for article in feed['entries']:
		if(n==0):
			n = n + 1
			if(is_has(article['post-id'])):
				for x in bot_id:
					await bot_send(article['title'], article['link'], x)
				update_id(article['post-id'])
	await asyncio.sleep(2)
			

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    