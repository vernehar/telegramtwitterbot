from telegram.ext import Updater
import twitterbotv2

#get credentials (api key) from file
tgCredentialFile = open("telegram_credentials.txt","r")
creds = tgCredentialFile.readlines()

#api key to tg
updater = Updater(token=creds[0], use_context=True)

dispatcher = updater.dispatcher
UpdateDict = {}
#function to call twitterupdate that return a list of new followings
def formMessage():
	#Get dict from twitterbot and loop through keys (influencer handles) and arrays under keys (new followings)
	_message = ""
	UpdateDict = twitterbotv2.twitterupdate()
	if UpdateDict: #check if dict is empty or not, if not empty form message of data, otherwise inform bot user
		for x,y in UpdateDict.items():
			if _message == "":
				_message = x + " started following:\n"
			else:
				_message = "\n\n" + _message + x + " started following:\n"
			for j in range(len(y)):
				_message = _message + "www.twitter.com/" + y[j] +"\n"
	else:
		_message = "No new follows by influencers that this bot keeps track of!"

	return _message

#message to be send on /start command (useless basically)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Leaking alpha")


def request(update, context):
	message = formMessage()
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)



#handles commands such as /start, /update
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
update_handler = CommandHandler('update', request)
dispatcher.add_handler(update_handler)

from telegram.ext import MessageHandler, Filters


request_handler = MessageHandler(Filters.text & (~Filters.command), request)


updater.start_polling()