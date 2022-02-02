from flask_mongoengine import MongoEngine


db = MongoEngine()


class Yak(db.Document):
    name = db.StringField(max_length=60, required=True, unique=True)
    age = db.FloatField(min_value=0)
    sex = db.StringField(max_length=1)
    creation_date = db.DateTimeField()
    meta = {
        'auto_create_index': True
    }


class Tribe(db.Document):
    tribe = db.ListField()
    total_milk = db.FloatField()
    total_wool = db.IntField()
    meta = {
        'auto_create_index': True
    }