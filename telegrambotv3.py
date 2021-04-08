from telegram.ext import Updater
import emoji
import databasecontrol
import twitterbotv3
import time




#get credentials (api key) from file
tgCredentialFile = open("telegram_credentials.txt","r")
creds = tgCredentialFile.readlines()

#api key to tg
updater = Updater(token=creds[0], use_context=True)
job_queue = updater.job_queue

dispatcher = updater.dispatcher
UpdateDict = {}
#function to call twitterupdate that return a list of new followings
def formMessage():
	#Get dict from twitterbot and loop through keys (influencer handles) and arrays under keys (new followings)
	_message = ""
	_messageArray = []
	UpdateDict = databasecontrol.dumpNewFollows()
	if UpdateDict: #check if dict is empty or not, if not empty form message of data, otherwise inform bot user
		for x,y in UpdateDict.items():
			if _message == "":
				_message = x + " started following:\n"
			else:
				if len(_message) > 3000:
					_messageArray.append(_message)
					_message = ""
				_message = "\n\n" + _message + x + " started following:\n"
			for j in range(len(y)):
				_message = _message + "www.twitter.com/" + y[j] +"\n"
		_messageArray.append(_message)
	else:
		_message = "No new follows by influencers that this bot keeps track of!"
		_messageArray.append(_message)

	return _messageArray

def formMessageTrending():
	_message = ""
	_messageArray = []

	trending8 = databasecontrol.trendingWithinTimePeriod(8)
	if trending8:
		_message = _message +"\n\n"+emoji.emojize(":eyes:")+"These handles seem to be trending in the previous 8 hours:\n"
		for t,r in trending8.items():
			_message = _message + str(r)+" inluencers started following www.twitter.com/"+t+"\n"
		_messageArray.append(_message)
		_message = ""

	trending24 = databasecontrol.trendingWithinTimePeriod(24)
	if trending24:
		_message = _message +"\n\n"+emoji.emojize(":eyes:")+"These handles seem to be trending in the previous 24 hours:\n"
		for z,w in trending24.items():
			_message = _message + str(w)+" inluencers started following www.twitter.com/"+z+"\n"
		_messageArray.append(_message)
		_message = ""
	trending48 = databasecontrol.trendingWithinTimePeriod(48)
	if trending48:
		_message = _message +"\n\n"+emoji.emojize(":eyes:")+"These handles seem to be trending in the previous 48 hours:\n"
		for n,m in trending48.items():
			_message = _message + str(m)+" inluencers started following www.twitter.com/"+n+"\n"
		_messageArray.append(_message)
		_message = ""


	return _messageArray

#message to be send on /start command (useless basically)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Leaking alpha")

def send_message_job(context):
	message = formMessage()
	message2 = formMessageTrending()
	for i in range(len(message)):
		context.bot.send_message(chat_id=-1001486656745,text=message[i])
	time.sleep(10)
	for j in range(len(message2)):
		context.bot.send_message(chat_id=-1001486656745,text=message2[j])
		time.sleep(1)

def request(update, context):
	message = formMessage()
	message2 = formMessageTrending()
	for i in range(len(message)):
		context.bot.send_message(chat_id=update.effective_chat.id, text=message[i])
		time.sleep(1)
	time.sleep(10)
	for j in range(len(message2)):
		context.bot.send_message(chat_id=update.effective_chat.id, text=message2[j])
		time.sleep(1)


def append(update, context):
	if twitterbotv3.appendUserToList(update.message.text.split(" ")[1]):
		context.bot.send_message(chat_id=update.effective_chat.id, text="www.twitter.com/" +update.message.text.split(" ")[1] + " was added to stalked influencers!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Could not find that twitter handle or handle is already stalked!")

def help_command(update, context):
	message = emoji.emojize(":eyes:")+""" This is a bot that stalks influencers on twitter.\n
The bot sends an automatic update every four hours. You can also use /update\n
Use /add *usernamehere* to add another influencer to follow.\n\n
Accounts that are followed by multiple influencers within a time period are considered trending
and the bot keeps track of those too\n\n"""+emoji.emojize(":eyes:")+" Currently followed influencers: " + databasecontrol.getCurrentInfluencersString()
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)

#handles commands such as /start, /update
from telegram.ext import CommandHandler, MessageHandler, Filters, PrefixHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
update_handler = CommandHandler('update', request)
append_handler = PrefixHandler("/","add", append)
dispatcher.add_handler(append_handler)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(CommandHandler("help", help_command))

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, append))

job_queue.run_repeating(send_message_job,interval=14400,first=0.0)

from telegram.ext import MessageHandler, Filters


request_handler = MessageHandler(Filters.text & (~Filters.command), request)


updater.start_polling()