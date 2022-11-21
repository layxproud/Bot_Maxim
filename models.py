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


class Blackjack(peewee.Model):
    class Meta:
        database = db
        db_table = 'BlacjackPlayers'
    vk_id = peewee.IntegerField()
    player_deck = peewee.TextField()
    player_score = peewee.IntegerField()
    dealer_deck = peewee.TextField()
    dealer_score = peewee.IntegerField()
    bet = peewee.IntegerField()
    is_playing = peewee.IntegerField()


if __name__ == "__main__":
    db.create_tables([User])
    db.create_tables([Blackjack])
