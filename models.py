import peewee

db = peewee.SqliteDatabase('data.db')


class User(peewee.Model):
    class Meta:
        database = db
        db_table = 'Users'
    vk_id = peewee.IntegerField()
    warns = peewee.IntegerField()
    chips = peewee.IntegerField()
    name = peewee.TextField()


if __name__ == "__main__":
    db.create_tables([User])
