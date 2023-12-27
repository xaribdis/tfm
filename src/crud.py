import pymongo
from pymongo.errors import DuplicateKeyError
import structlog
import json

# from config import settings


# Constants
TTL = 3600 * 24 * 30
N_SENSORS = 4607
MONGO_URI = "mongodb://mongo"
PORT = 27017
MONGO_DB = "myapp"
GEOJSON_FILE = "data/madrid-districts.geojson"

# Configure structlog for logging
structlog.configure(processors=[structlog.processors.JSONRenderer()])
log = structlog.getLogger()


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()


def query_sensor_districts(idelem: int) -> str:
    collection = mongo.get_collection('sensor_districts')
    try:
        query = {"_id": idelem}
        return collection.find_one(query)['district_name']
    except Exception as e:
        return "unknown"


class MongoManager:
    def __init__(self):
        self._client = None
        self._index = None
        self._n_sensors = N_SENSORS

    def get_mongo_client(self):
        """Return a MongoDB client"""
        if self._client is None:
            self.connect_to_mongo()
        return self._client

    def health_check(self):
        """Perform health check on MongoDB"""
        self.get_mongo_client()

        # Check TTL index
        if self._index is None:
            self.set_ttl('historic', TTL)
            self._index = self.check_index('historic')['fecha_hora_1']

        # Check number of sensors has not changed and update otherwise
        if new_n_sensors := self.get_n_sensors() != self._n_sensors:
            self.sensor_districts_correspondence()
            self._n_sensors = new_n_sensors

    def connect_to_mongo(self):
        """Connect to MongoDB"""
        self._client = pymongo.MongoClient(MONGO_URI, port=PORT)
        try:
            self._client.admin.command('ping')
            print('Successfully connected to Mongo')
        except Exception as e:
            log.error(e)

    def close_connection(self):
        """Close connection to MongoDB"""
        if self._client is not None:
            self._client.close()

    def get_collection(self, col_name):
        """Return a MongoDB collection"""
        client = self.get_mongo_client()
        try:
            db = client[MONGO_DB]
            collection = db[col_name]
            return collection
        except Exception as e:
            log.error(e)

    # Check if ttl index exists
    def check_index(self, col_name):
        """Check if TTL index exists"""
        try:
            collection = self.get_collection(col_name)
            id_info = collection.index_information()
            return id_info
        except Exception as e:
            log.error(e)

    def set_ttl(self, col_name, ttl):
        """Set the ttl index in collection"""
        try:
            collection = self.get_collection(col_name)
            collection.create_index("fecha_hora", expireAfterSeconds=ttl)
        except Exception as e:
            log.error(e)

    def load_districts(self):
        """Load districts into database. (Not used in the app)"""
        with open(GEOJSON_FILE) as file:
            geojson = json.loads(file.read())
        collection = self.get_collection('districts')
        collection.create_index([("geometry", pymongo.GEOSPHERE)])
        bulk = []

        for feature in geojson['features']:
            bulk.append(pymongo.InsertOne(feature))
        collection.bulk_write(bulk)

    def sensor_districts_correspondence(self):
        """Load a collection with the district of each sensor"""
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
                log.error(e)

    def get_n_sensors(self):
        sensors = self.get_collection('historic')
        return len(sensors.distinct("idelem"))


mongo = MongoManager()
