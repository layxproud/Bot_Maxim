from peewee import *

db = SqliteDatabase('data.db')

class User(Model):
    class Meta:
        database = db
        db_table = 'Users'
    vk_id = IntegerField()
    warns = IntegerField()
    chips = IntegerField()
    name = TextField()
    
if __name__ == "__main__":
    db.create_tables([User])