import queries
import bson
import numpy as np
import pandas as pd
from pymongo import MongoClient

uri = "mongodb://<>:<>@ds215093.mlab.com:15093/medbot"
client = MongoClient(uri)
UL_folder = 'C:/Users/andrey/Documents/Mongo Backend/'
db = client.medbot

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

users = db.users

df_users = pd.read_excel(UL_folder + 'user_UL.xlsx',
                         dtype={'tg_chat_id': np.int32, 'uid': np.int32})

dict_names = list(df_users)

for row in range(0, df_users.shape[0]):
    dict_temp = {}
    for col in range(0, df_users.shape[1]):
        dict_temp.update({dict_names[col]: bson.int64.Int64(df_users.iloc[row, col])})
    users.insert_one(dict_temp)

queries.add_inner_document(users, "services")

queries.add_service_welcome_by_id(users, "welcome", 552)

queries.chng_service_welcome_status_by_id(users, 552, 1)

users.update({"uid": bson.int64.Int64(552)}, {"$pull": {"services": "welcome"}})
