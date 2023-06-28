from pymongo import MongoClient

client = MongoClient('mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net')
db = client['projectdb']
collection = db['images']

with open('/Users/josephkeinan/Downloads/testtestpic.jpg', 'rb') as f:
  
    image_data = f.read()
    stored_image = collection.insert_one({'image': image_data})
    

print(stored_image.inserted_id)
