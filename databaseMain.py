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

    def read(self, query={}):
        return [item for item in self.collection.find(query)]

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

# damy_dic1 = {
#     "name": "adele",
#     "lastname": "keinan",
#     "email": "adelekeinan@gmail.com",
#     "phone": "0535319985",
#     "date": "01/02/2023",
#     "reletives": [
#         {"name": "yosef", "relationid": "123"},
#         {"name": "hava", "relationid": "4646"},
#         {"name": "rivka", "relationid": "111"}
#     ]

# }
# damy_dic2 = {
#     "name": "Rout",
#     "lastname": "tzadok",
#     "email": "rt123@example.com",
#     "phone": "0523456789",
#     "date": "01/03/2023",
#     "relatives": [
#         {"name": "Avi", "relationid": "321"},
#         {"name": "Yvi", "relationid": "654"},
#         {"name": "Zvi", "relationid": "987"}
#     ]
# }
# mongo = MongoDB(collection="users")


# user1_id = mongo.create(damy_dic1)
# for relative in damy_dic1["reletives"]:
#     relative['user_id'] = str(user1_id)
#     mongo.create(relative)


# user2_id = mongo.create(damy_dic2)
# for relative in damy_dic2["relatives"]:
#     relative['user_id'] = str(user2_id)
#     mongo.create(relative)


# a1 = MongoDB("praying")
# list_of_dicts = a1.read({"phone":"5555555"})
# # print(list_of_dicts)
# for dict in list_of_dicts:
#     if dict["name"]=="adele":
#         print(f"{dict}")
#     else:
#         print("not found")

# a1 = MongoDB("users")
# query = {"phone":"5555555"}
# data = a1.read(query)
# print(data[0])
# return jsonify(data[0])
# docs = a1.read({'name': 'adele'})
# print(docs)


# query = {'phone': '5555555'}
# a1.delete(query)
# new_values = {"$set": {'lastname': 'shofan'}}
# a1.replace(query, new_values)


# my_dict = {
#     "key1": "adele",
#     "key2": "lala",
#     "key3": "dada"
# }

# xname = ""
# xlastname = ""
# xemail = ""
# dic_users = {
#     "name": xname,
#     "lastname": xlastname,
#     "email": xemail
# }
# dic_deceased = {"key": "value"}
# dic_praying = {"key": "value"}
# dic_users["name"] = input("what is your name?")
# dic_users["lastname"] = input("what is your xlastname?")
# dic_users["email"] = input("what is your xemail?")

# dic_deceased["full name"] = input("what is the full name?")
