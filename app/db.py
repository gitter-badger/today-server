from mongoengine import connect, Document, IntField, DateTimeField, EmbeddedDocument, StringField
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connection(object):
    is_connected = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        pass

    def connect(self, config=None):
        if config is not None:
            # connect mysql
            engine = create_engine(config.sqlalchemy.uri, **config.sqlalchemy.kwargs)
            self.session = (sessionmaker(bind=engine))()

            # connect mongodb
            connect(config.mongoengine.database, **config.mongoengine.kwargs)

            # connect redis
            self.redis = redis.StrictRedis(host=config.redis.host, port=config.redis.port, db=config.redis.db)

            # TODO: validate
            self.is_connected = True


class Post(Document):
    post_id = IntField(required=True)
    user_id = IntField(required=True)
    text = StringField()


class Comment(EmbeddedDocument):
    id = StringField()
    user_id = IntField()
    content = StringField()
    created_dt = DateTimeField()

