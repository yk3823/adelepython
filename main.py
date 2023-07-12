from flask import Flask, request, jsonify, redirect
from databaseMain import MongoDB
from bson import json_util
import json
from sendemail import Email
from message import Message
from handle_dates import userDate
from datetime import datetime
import uuid
from pymongo import MongoClient
from flask_cors import CORS
from bson.objectid import ObjectId
from pymongo import MongoClient
from gridfs import GridFS


client = MongoClient('localhost', 27017)
db = client['memorial_site']
collection = db['deceased']
mongo = MongoDB(collection="users")
app = Flask(__name__)
cors = CORS(app)
fs = GridFS(db)
# cors = CORS(app, origins='http://localhost:5173')

data = {}


@app.route('/create_images_collection', methods=['POST'])
def create_images_collection():
    mongo.create_images_collection()
    return jsonify({"message": "Images collection created"}), 200


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file found"}), 400
    # client = MongoClient('localhost', 27017)
    # db = client['memorial_site']
    # fs = GridFS(db)

    image_file = request.files['image']
    image_id = fs.put(image_file)
    image_id_str = str(image_id)

    return jsonify({"message": "Image uploaded", "image_id": str(image_id_str)}), 200


@app.route('/userdate', methods=['POST'])
def userdate():
    if not request.json:
        return jsonify({"error": "No data sent"}), 400

    data = request.get_json()
    a1 = userDate(data)

    print("Foreign date and Hebrew date:", a1.print_dates())
    next_date = a1.get_next_date()
    print("Next year and next Hebrew year:", next_date)

    date_valdiate = a1.validate_input()

    if 'error' in date_valdiate:
        return jsonify(date_valdiate), 400
    else:
        return jsonify(date_valdiate), 200


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    email = data.get("email")
    a1 = MongoDB("users")
    querytoemail = a1.read({"email": email})

    if querytoemail:
        error_message = "Email already exists in the system"
        print(error_message)
        return jsonify({"error": "Email already exists in the system"}), 400

    if not request.json:
        return jsonify({"error": "No data sent"}), 400

    # print(data["user_verified"])
    print(data["email"])
    a1 = MongoDB("users")
    b1 = Email(data["email"], "adelekeinan@gmail.com", "voacfoofzkdckeao")
    # d1 = userDate(datetime.strptime(data['date'], '%Y/%m/%d'))

    c1 = Message(data["email"], "hello").getMessage()
    b1.send_email(c1["subject"], c1["message"])
    if 'photo' in data:
        image_id = data['photo']
        data['photo'] = fs.get(ObjectId(image_id))

    a1.create(data)

    # b1 = mainEmail.Email(data["email"],"adelekeinan@gmail.com","voacfoofzkdckeao")
    created_message = "Email created"
    print(created_message)
    return jsonify({"ok": "document has been created!!"}), 200


@app.route('/emailverified/<token>', methods=['GET'])
def verify_email(token):
    email = token
    a1 = MongoDB("users")
    a1.update({"email": email}, {"user_verified": True})
    redirect_url = "http://localhost:5173/verify?token=" + token

    if a1.read({"email": email, "user_verified": True}):
        # return jsonify({"message": f"Email has been verified with token {token}! You can now add a deceased person on the site.", "redirect_url": redirect_url}), 200
        return redirect(redirect_url, code=302)

    else:
        return jsonify({"error": "Invalid token or email not verified."}), 400


@app.route('/deceased', methods=['POST'])
def save_deceased_details():
    data = request.get_json()
    a1 = MongoDB("deceased")
    a1.create(data)

    return jsonify({"message": "Deceased details saved"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
