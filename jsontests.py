test = {
  "_id": "646c7aecfe80ba9fc7feed47",
  "name": "Jon",
  "lastname": "Don",
  "email": "jd1234@example.com",
  "phone": "0123456789",
  "date": "01/03/2023",
  "relatives": [
    {
      "name": "Jane",
      "relationid": "321"
    },
    {
      "name": "Bob",
      "relationid": "654"
    },
    {
      "name": "Charlie",
      "relationid": "987"
    }
  ]
}
# print(test.get("date"))
# print(test["relatives"][2]["name"])  

# print(test.get("relatives")[1].get("relationid"))  

# for relative in test["relatives"]:
#     print(relative["relationid"])

# JSON object
# for key, value in test.items():
#     print(key, value)
    
# print(test.get("_id"))

# print(test["relatives"])

# print(test["relatives"])

# for i in test["relatives"]:
#     if i["relationid"]=="321":
#         print (i)

# # dict inside of a list 
# for i in test ["relatives"]:
#     print (i)
