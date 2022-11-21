import peewee

db1 = peewee.SqliteDatabase('users.db')
db2 = peewee.SqliteDatabase('bjplayers.db')


class User(peewee.Model):
    class Meta:
        database = db1
        db_table = 'Users'
    vk_id = peewee.IntegerField()
    warns = peewee.IntegerField()
    chips = peewee.IntegerField()
    name = peewee.TextField()


class Blackjack(peewee.Model):
    class Meta:
        database = db2
        db_table = 'BlacjackPlayers'
    vk_id = peewee.IntegerField()
    player_deck = peewee.TextField()
    player_score = peewee.IntegerField()
    dealer_deck = peewee.TextField()
    dealer_score = peewee.IntegerField()
    bet = peewee.IntegerField()
    is_playing = peewee.IntegerField()


if __name__ == "__main__":
    db1.create_tables([User])
    db2.create_tables([Blackjack])
