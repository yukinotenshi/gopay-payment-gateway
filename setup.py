from base import Gopay
from random import choice
from model import db, Transaction

email = input("Your gopay email address : ")
gopay = Gopay(email)

key = ""
seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
for i in range(30):
    key += choice(seed)

token = gopay.login()

with open("config.py", "w") as f:
    to_be_written = 'TOKEN = "%s"\n' % token
    to_be_written += 'API_KEY = "%s"\n' % key

    f.write(to_be_written)

db.connect()
db.create_tables([Transaction])
db.close()
