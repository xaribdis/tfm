import pymongo


def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()





if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://127.0.0.1", port=27017)

    try:
        print('Hello there')
        client.admin.command('ping')
        print('General Kenobi')
    except Exception as e:
        print('Asno!')

    db = client.myapp
    collection = db["story"]

    collection.create_index("fecha_hora", expireAfterSeconds=60)
