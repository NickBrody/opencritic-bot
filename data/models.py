from peewee import Model, SqliteDatabase, CharField, IntegerField

db = SqliteDatabase('my_database.db')


class User(Model):
    """Класс User, для работы с базой данных."""
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)

    class Meta:
        database = db
