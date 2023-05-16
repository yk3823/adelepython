from pymongo import MongoClient
import datamodel


class MongoDB:
    def __init__(self, uri, database, collection):
        self.client = MongoClient(uri)
        self.database = self.client[database]
        self.collection = self.database[collection]

    def insert_document(self, document):
        return self.collection.insert_one(document)


xname = ""
xlastname = ""
xemail = ""
dic_users = {
    "name": xname,
    "lastname": xlastname,
    "email": xemail
}
dic_deceased = {"key": "value"}
dic_praying = {"key": "value"}
dic_users["name"] = input("what is your name?")
dic_users["lastname"] = input("what is your xlastname?")
dic_users["email"] = input("what is your xemail?")

db_users = MongoDB(
    'mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/', 'projectdb', 'users')
# db_deceased = MongoDB(
#     'mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/', 'projectdb', 'deceased')
# db_praying = MongoDB(
#     'mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/', 'projectdb', 'praying')


db_users.insert_document(dic_users)
# db_deceased.insert_document(datamodel.dic_deceased)
# db_praying.insert_document(datamodel.dic_praying)
