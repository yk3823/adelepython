
from gridfs import GridFS
from pymongo import MongoClient
from PIL import Image

client = MongoClient('localhost', 27017)
db = client['memorial_site']
collection = db['deceased']

fs = GridFS(db)


image_path = '/Users/josephkeinan/Downloads/testtestpic.jpg'
with open(image_path, 'rb') as f:
    image_bytes = f.read()


image_id = fs.put(image_bytes, filename="testtestpic.jpg")

print(image_id)
# image = Image.open(image_path)
# image_bytes = image.tobytes()


# with fs.new_file(filename='testtestpic.jpg') as grid_file:
#     grid_file.write(image_bytes)

# image.close()

# retrieved_file = fs.find_one({"filename": "testtestpic.jpg"})
# retrieved_image_bytes = retrieved_file.read()

# retrieved_image_path = '/Users/josephkeinan/Downloads/retrieved_image.jpg'
# with open(retrieved_image_path, 'wb') as retrieved_image_file:
#     retrieved_image_file.write(retrieved_image_bytes)
