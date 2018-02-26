from peewee import *
from datetime import date


db = SqliteDatabase("data.db")

class Transaction(Model):
	amount = IntegerField()
	created_at = DateField(default=date.today)
	status = BooleanField(default=False)

	class Meta:
		database = db