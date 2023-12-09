import pymongo
from pymongo.errors import DuplicateKeyError
import structlog
import json

# from constants import TTL, N_SENSORS, MONGO_URI, PORT


structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()

ttl = 3600 & 24 * 30


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()


def query_sensor_districts(idelem: int) -> str:
    collection = mongo.get_collection('sensor_districts')
    try:
        query = {"_id": idelem}
        return collection.find_one(query)['district_name']
    except Exception as e:
        return "unknown"


class MongoInitializer:
    _client = None
    _index = None
    _n_sensors = 4607

    def get_mongo_client(self):
        if self._client is None:
            self._client = self.connect_to_mongo()

        return self._client

    # Check that ttl exist and number of sensors
    def healthz(self):
        client = self.get_mongo_client()
        if self._index is None:
            self.set_ttl('historic', ttl)
            self._index = self.check_index('historic')['fecha_hora_1']

        if new_n_sensors := self.get_n_sensors() != self._n_sensors:
            self.sensor_districts_correspondence()
            self._n_sensors = new_n_sensors

    @staticmethod
    def connect_to_mongo():
        client = pymongo.MongoClient("mongodb://mongo", port=27017)
        # client = pymongo.MongoClient("mongodb://127.0.0.1", port=27017)

        try:
            client.admin.command('ping')
            print('Successfully connected to Mongo')
        except Exception as e:
            log.info(e)

        return client

    def close_connection(self):
        if self._client is not None:
            self._client.close()

    def get_collection(self, col_name):
        client = self.get_mongo_client()
        try:
            db = client.myapp
            collection = db[col_name]
            return collection
        except Exception as e:
            log.info(e)

    # Check if ttl index exists
    def check_index(self, col_name):
        try:
            collection = self.get_collection(col_name)
            id_info = collection.index_information()
            return id_info
        except Exception as e:
            log.info(e)

    # Function to set the ttl index in collection
    def set_ttl(self, col_name, ttl):
        try:
            collection = self.get_collection(col_name)
            collection.create_index("fecha_hora", expireAfterSeconds=ttl)
        except Exception as e:
            log.info(e)

    # Method to load the districts into database. Not used in the app.
    def load_districts(self):
        with open("data/madrid-districts.geojson") as file:
            geojson = json.loads(file.read())
        collection = self.get_collection('districts')
        collection.create_index([("geometry", pymongo.GEOSPHERE)])
        bulk = []

        for feature in geojson['features']:
            bulk.append(pymongo.InsertOne(feature))
        collection.bulk_write(bulk)

    # Method to load a collection with the district in which each sensor is located, bc querying idelem is quicker than
    # doing geospatial queries for each data batch. If new sensors are added, this collection should be updated.
    def sensor_districts_correspondence(self):
        districts = self.get_collection('districts')
        sensor_districts_collection = self.get_collection('sensor_districts')
        sensors = self.get_collection('historic')
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

    def get_n_sensors(self):
        sensors = self.get_collection('historic')
        return len(sensors.distinct("idelem"))


mongo = MongoInitializer()
