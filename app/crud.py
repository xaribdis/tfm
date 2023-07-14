import pymongo
import structlog


structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()


ttl = 3600 * 24 * 30


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()


class MongoInitializer:
    index = None

    def __init__(self):
        if MongoInitializer.index is None:
            client = self.connect_to_mongo()
            collection = self.get_collection(client, 'story')
            MongoInitializer.index = self.check_index(collection)['fecha_hora_1']
            self.set_ttl(collection, ttl)
            client.close()

    @staticmethod
    def connect_to_mongo():
        # TODO load from config
        client = pymongo.MongoClient("mongodb://127.0.0.1", port=27017)

        try:
            client.admin.command('ping')
            print('Successfully connected to Mongo')
        except Exception as e:
            log.info(e)

        return client

    @staticmethod
    def get_collection(client, col_name):
        try:
            db = client.myapp
            collection = db[col_name]
            return collection
        except Exception as e:
            log.info(e)

    # Check if ttl index exists
    @staticmethod
    def check_index(collection):
        try:
            id_info = collection.index_information()
            return id_info
        except Exception as e:
            log.info(e)

    # Function to set the ttl index in collection
    @staticmethod
    def set_ttl(collection, ttl):
        try:
            # TODO read from config
            collection.create_index("fecha_hora", expireAfterSeconds=ttl)
        except Exception as e:
            log.info(e)

    def __str__(self):
        return self.index
