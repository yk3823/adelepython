from pymongo import MongoClient
import datamodel
from typing import List, Dict, Any


class MongoDB:
    def __init__(self, collection, uri="mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/", database="projectdb"):
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def create(self, data):
        return self.collection.insert_one(data).inserted_id

    def read(self, query={}, skip=0, limit=None, sort=None):
        cursor = self.collection.find(query).skip(
            skip).limit(limit if limit else 0)
        if sort:
            cursor = cursor.sort(sort)
        return [item for item in cursor]

    def update(self, query, new_data):
        return self.collection.update_one(query, {'$set': new_data}).modified_count

    def delete(self, query):
        return self.collection.delete_one(query).deleted_count

    def create_images_collection(self):
        self.images_collection = self.database["images"]

    def create_image(self, data):
        return self.images_collection.insert_one(data).inserted_id

    def return_one_value(self, query={}):
        cursor = self.collection.find(query, {"_id": 1})
        return list(cursor)

    def find_one(self, query):
        return self.collection.find_one(query)

    def update_array(self, query, arr):
        return self.collection.update_one(query, {"$push": {"deceased": {"$each": arr}}})

    def count(self, query={}):
        return self.collection.count_documents(query)
