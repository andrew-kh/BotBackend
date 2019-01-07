#!/Users/andrew/anaconda3/bin/python

import queries
from pymongo import MongoClient
import telebot
from config import token
import datetime as dt

# set up DB connection
uri = "mongodb://<user>:<user>@ds215093.mlab.com:15093/medbot"

client = MongoClient(uri)

db = client.medbot

messages = db.message_dump
users = db.users
reminders = db.reminders

bot = telebot.TeleBot(token)

all_reminders = reminders.find({})

for i in all_reminders:
    if i['date_time'] <= dt.datetime.now() and i['send_status'] == 0:
        bot.send_message(i['tg_chat_id'], i['text'])
        reminders.update_one({"tg_chat_id": i['tg_chat_id']}, {'$set': {'send_status': 1}})