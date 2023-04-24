import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from pytube import YouTube

TOKEN = 'your-bot-token-here'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

reel_handler = MessageHandler(Filters.text & ~Filters.command, download_reel)
dispatcher.add_handler(reel_handler)

updater.start_polling()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a link to an Instagram reel and I will download it for you.")

def download_reel(update, context):
    chat_id = update.effective_chat.id
    message = update.message.text
    if 'instagram.com/reel/' in message:
        response = requests.get(message)
        video_url = response.text.split('video_url":"')[1].split('","')[0]
        try:
            YouTube(video_url).streams.first().download()
            context.bot.send_video(chat_id=chat_id, video=open('output.mp4', 'rb'))
        except:
            context.bot.send_message(chat_id=chat_id, text='Failed to download reel.')
    else:
        context.bot.send_message(chat_id=chat_id, text='Please send a valid link to an Instagram reel.')
