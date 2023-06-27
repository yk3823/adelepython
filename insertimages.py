from pymongo import MongoClient
import gridfs


client = MongoClient('mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net', 27017)
db = client['projectdb']
fs = gridfs.GridFS(db)

with open('/Users/josephkeinan/Downloads/testtestpic.jpg', 'rb') as f:
    # Insert the file into GridFS
    thedata = f.read()
    stored = fs.put(thedata, filename="testtestpic.jpg")
print(stored)

file = fs.get(stored)
data = file.read()
with open('output.jpg', 'wb') as f:
    f.write(data)
