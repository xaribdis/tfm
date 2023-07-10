import pymongo

def load_to_mongo(df):
    df.write.format("mongodb").mode("append").save()
