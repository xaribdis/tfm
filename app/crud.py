import pymongo
from pymongo.errors import DuplicateKeyError
import structlog
import json


structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()


# TODO Move to config file
ttl = 3600 * 24 * 30


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()


def query_sensor_districts(idelem: int) -> str:
    client = MongoInitializer.get_mongo_client()
    collection = MongoInitializer.get_collection(client, 'sensor_districts')
    try:
        query = {"_id": idelem}
        return collection.find_one(query)['district_name']
    except Exception as e:
        return "unknown"


class MongoInitializer:
    _client = None
    _index = None
    # TODO move to config file
    _n_sensors = 4607

    @staticmethod
    def get_mongo_client():
        if MongoInitializer._client is None:
            MongoInitializer._client = MongoInitializer.connect_to_mongo()

        return MongoInitializer._client

    @staticmethod
    def healthz():
        client = MongoInitializer.get_mongo_client()
        if MongoInitializer._index is None:
            collection = MongoInitializer.get_collection(client, 'story')
            MongoInitializer.set_ttl(collection, ttl)
            MongoInitializer._index = MongoInitializer.check_index(collection)['fecha_hora_1']

        if new_n_sensors := MongoInitializer.get_n_sensors(client) != MongoInitializer._n_sensors:
            MongoInitializer.sensor_districts_correspondence(client)
            MongoInitializer._n_sensors = new_n_sensors

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
            # TODO load from config
            collection.create_index("fecha_hora", expireAfterSeconds=ttl)
        except Exception as e:
            log.info(e)

    # Method to load the districts into database. Not used in the app.
    @staticmethod
    def load_districts():
        client = MongoInitializer.get_mongo_client()
        with open("data/madrid-districts.geojson") as file:
            geojson = json.loads(file.read())
        collection = MongoInitializer.get_collection(client, 'districts')
        collection.create_index([("geometry", pymongo.GEOSPHERE)])
        bulk = []

        for feature in geojson['features']:
            bulk.append(pymongo.InsertOne(feature))
        result = collection.bulk_write(bulk)

# Method to load a collection with the district in which each sensor is located, bc querying idelem is quicker than
# doing geospatial queries for each data batch. If new sensors are added, this collection should be updated.
    @staticmethod
    def sensor_districts_correspondence(client):
        districts = MongoInitializer.get_collection(client, 'districts')
        sensor_districts_collection = MongoInitializer.get_collection(client, 'sensor_districts')
        sensors = MongoInitializer.get_collection(client, 'story')
        pipeline = [{"$group":
                     {"_id": "$idelem",
                      "latitud": {"$first": "$latitud"},
                      "longitud": {"$first": "$longitud"}}}]
        sensor_cursor = sensors.aggregate(pipeline)

        for doc in sensor_cursor:
            query = {"geometry":
                     {"$geoIntersects":
                      {"$geometry":
                       {"type": "Point",
                                "coordinates": [doc['longitud'],
                                                doc['latitud']]
                        }}}}

            district_cursor = districts.find_one(query)
            try:
                sensor_district = district_cursor['properties']['name']
                sensor_districts_collection.insert_one({"district_name": sensor_district,
                                                        "_id": doc['_id']})
            except DuplicateKeyError:
                continue
            except Exception as e:
                log.info(e)

    @staticmethod
    def get_n_sensors(client):
        sensors = MongoInitializer.get_collection(client, 'story')
        return len(sensors.distinct("idelem"))
