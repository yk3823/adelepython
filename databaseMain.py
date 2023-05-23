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


damy_dic1 = {
    "name": "adele",
    "lastname": "keinan",
    "email": "yk3823",
    "phone": "0546565236",
    "date": "01/02/2023",
    "reletives": [{
            "name": "Alice",
            "relationid": "123"
    },
        {
            "name": "Bob",
            "relationid": "4646"
    },
        {
            "name": "Charlie",
            "relationid": "Brother"
    }]

}
damy_dic2 = {
    "name": "Jon",
    "lastname": "Don",
    "email": "jd1234@example.com",
    "phone": "0123456789",
    "date": "01/03/2023",
    "relatives": [
        {"name": "Jane", "relationid": "321"},
        {"name": "Bob", "relationid": "654"},
        {"name": "Charlie", "relationid": "987"}
    ]
}

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
