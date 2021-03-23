from telegram.ext import Updater
import twitterbotv2
import emoji

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

def append(update, context):
	if twitterbotv2.appendUserToList(update.message.text.split(" ")[1]):
		context.bot.send_message(chat_id=update.effective_chat.id, text="www.twitter.com/" +update.message.text.split(" ")[1] + " was added to stalked influencers!")
	else:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Could not find that twitter handle or handle is already stalked!")

def help_command(update, context):
	message = emoji.emojize(":eyes:")+""" This is a bot that stalks influencers on twitter.\n
Use /update to get new followings by influencers that are followed.
Use /add *usernamehere* to add another influencer to follow.\n\n"""+emoji.emojize(":eyes:")+" Currently followed influencers: " + twitterbotv2.getCurrentInfluencers()
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

from telegram.ext import MessageHandler, Filters


request_handler = MessageHandler(Filters.text & (~Filters.command), request)


updater.start_polling()