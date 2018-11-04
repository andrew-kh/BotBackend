import queries
import bson
import numpy as np
import pandas as pd
from pymongo import MongoClient

# enter user/pwd wo <>
uri = "mongodb://andrey.khuhlin:andrey.khuhlinABT1@ds215093.mlab.com:15093/medbot"
client = MongoClient(uri)
UL_folder = '/Users/andrew/PycharmProjects/MedBot/'
db = client.medbot

# insert/append data from excel file to collection "message_dump"
# this code will create this collection if it doesn't exist in DB
messages = db.message_dump

df_msgs = pd.read_excel(UL_folder + 'messages_UL.xlsx',
                        dtype={'tg_chat_id': np.int32, 'time_received': np.int32,
                               'message': str, 'uid': np.int32})

dict_names = list(df_msgs)

for row in range(0, df_msgs.shape[0]):
    dict_temp = {}
    for col in range(0, df_msgs.shape[1]):
        if col != 2:
            dict_temp.update({dict_names[col]: bson.int64.Int64(df_msgs.iloc[row, col])})
        else:
            dict_temp.update({dict_names[col]: df_msgs.iloc[row, col]})
    messages.insert_one(dict_temp)

# insert/append data from excel file to collection "users"
# this code will create this collection if it doesn't exist in DB
users = db.users

df_users = pd.read_excel(UL_folder + 'user_UL.xlsx',
                         dtype={'tg_chat_id': np.int32, 'uid': np.int32})

dict_names = list(df_users)

for row in range(0, df_users.shape[0]):
    dict_temp = {}
    for col in range(0, df_users.shape[1]):
        dict_temp.update({dict_names[col]: bson.int64.Int64(df_users.iloc[row, col])})
    users.insert_one(dict_temp)

# add an array "services" to all users
queries.add_inner_document(users, "services")

# assign an instance of "welcome" service to user with specific id
queries.add_service_welcome_by_id(users, 552)

# change status of service (when welcome message is sent)
queries.chng_service_welcome_status_by_id(users, 552, 1)