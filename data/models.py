from peewee import Model, SqliteDatabase, CharField, IntegerField, ForeignKeyField, TextField

db = SqliteDatabase('my_database.db')


class User(Model):
    """Класс User, для работы с базой данных.
    user_id - поле типа IntegerField, являющееся первичным ключом (primary_key=True).
    username - поле типа CharField с возможностью принимать значение null=True.
    first_name - поле типа CharField.
    last_name - поле типа CharField с возможностью принимать значение null=True."""
    user_id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)

    class Meta:
        """Meta - внутренний класс, который содержит атрибут database, указывающий на базу данных db"""
        database = db


class Commands(Model):
    """Класс Command, для работы с базой данных.
    user - поле типа ForeignKeyField, которое ссылается на класс User и использует поле user_id в качестве
    внешнего ключа (to_field=User.user_id).
    user_message - поле типа CharField.
    user_params - поле типа TextField с возможностью принимать значение null=True."""
    user = ForeignKeyField(User, to_field=User.user_id)
    user_message = CharField()
    user_params = TextField(null=True)

    class Meta:
        """Meta - внутренний класс, который содержит атрибут database, указывающий на базу данных db"""
        database = db
