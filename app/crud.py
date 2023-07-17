import pymongo
import structlog
import json


structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()


# TODO Move to config file
ttl = 3600 * 24 * 30


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()


def query_sensor_districts(idelem: int) -> str:
    collection = MongoInitializer.get_collection('sensor_districts')
    query = {"$_id": idelem}
    return collection.find_one(query)['district_name']


class MongoInitializer:
    client = None
    index = None
    # TODO move to config file
    n_sensors = 4607

    def __init__(self):
        if MongoInitializer.client is None:
            MongoInitializer.client = self.connect_to_mongo()

        if MongoInitializer.index is None:
            print('hello there')
            collection = self.get_collection('story')
            self.set_ttl(collection, ttl)
            MongoInitializer.index = self.check_index(collection)['fecha_hora_1']

        if new_n_sensors := MongoInitializer.get_n_sensors() != MongoInitializer.n_sensors:
            self.sensor_districts_correspondence()
            MongoInitializer.n_sensors = new_n_sensors

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
    def get_collection(col_name):
        try:
            db = MongoInitializer.client.myapp
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
        with open("data/madrid-districts.geojson") as file:
            geojson = json.loads(file.read())
        collection = MongoInitializer.get_collection('districts')
        collection.create_index([("geometry", pymongo.GEOSPHERE)])
        bulk = []

        for feature in geojson['features']:
            bulk.append(pymongo.InsertOne(feature))
        result = collection.bulk_write(bulk)

# Method to load a collection with the district in which each sensor is located, bc querying idelem is quicker than
# doing geospatial queries for each data batch. If new sensors are added, this collection should be updated.
    @staticmethod
    def sensor_districts_correspondence():
        districts = MongoInitializer.get_collection('districts')
        sensor_districts_collection = MongoInitializer.get_collection('sensor_districts')
        sensors = MongoInitializer.get_collection('story')
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
            except Exception as e:
                log.info(e)

    @staticmethod
    def get_n_sensors():
        sensors = MongoInitializer.get_collection('story')
        return len(sensors.distinct("idelem"))

    def __str__(self):
        return self.index
