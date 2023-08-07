from flask import Flask, make_response, request, jsonify, redirect, Response
import pymongo
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
import base64

MONGODB_URI = "mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/"
DATABASE_NAME = "projectdb"
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db['deceased']
mongo = MongoDB(collection="users")
app = Flask(__name__)
cors = CORS(app)
fs = GridFS(db)
ITEMS_PER_PAGE = 6
data = {}


@app.route('/create_images_collection', methods=['POST'])
def create_images_collection():
    mongo.create_images_collection()
    return jsonify({"message": "Images collection created"}), 200


# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file found"}), 400
#     # client = MongoClient('localhost', 27017)
#     # db = client['memorial_site']
#     # fs = GridFS(db)

#     image_file = request.files['image']
#     image_id = fs.put(image_file)
#     image_id_str = str(image_id)

#     return jsonify({"message": "Image uploaded", "image_id": str(image_id_str)}), 200


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
    useremail = request.form.get('token')
    a1 = MongoDB("users")
    b1 = MongoDB("deceased")
    # result = b1.return_one_value({"email": useremail})

    name = request.form.get('name')
    dateOfDeath = request.form.get('dateOfDeath')

    if 'photo' in request.files:
        photo_file = request.files['photo']
        photo_data = photo_file.read()
        print(photo_data)
        # Save photo data to MongoDB GridFS
        photo_id = fs.put(photo_data)

        deceased_dict = {
            'name': name,
            'dateOfDeath': dateOfDeath,
            'photo_id': photo_id
        }
        res_deceasedId = b1.create(deceased_dict)
        print(res_deceasedId)

        querY = {"email": useremail}
        deceasedId = [res_deceasedId]

        a1.update_array(querY, deceasedId)

        return jsonify({"message": "Deceased details saved"}), 200
    return jsonify({"error": "No photo found"}), 400


def get_day_and_month(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.month, date_obj.day


@app.route('/get_deceased_details', methods=['GET'])
def get_deceased_details():
    page = int(request.args.get('page', 1))
    alldec = []
    a1 = MongoDB("deceased")
    skip_records = (page - 1) * ITEMS_PER_PAGE
    deceased_details = a1.read(
        skip=skip_records, limit=ITEMS_PER_PAGE, sort=[("dateOfDeath", 1)])
    fs = GridFS(db)
    current_month, current_day = get_day_and_month(
        datetime.now().strftime('%Y-%m-%d'))
    positive_differences = []
    negative_differences = []
    for result in deceased_details:
        if 'photo_id' in result:
            # print(result['name'])
            image = fs.get(result['photo_id'])
            encoded_image = base64.b64encode(image.read()).decode('ascii')
            deceased_month, deceased_day = get_day_and_month(
                result['dateOfDeath'])
            difference = ((datetime(2000, deceased_month, deceased_day) -
                           datetime(2000, current_month, current_day)).days)

            data = {
                'name': result['name'],
                'photo_id': encoded_image,
                'difference': difference,
                'dateOfDeath': result['dateOfDeath']

            }
            alldec.append(data)

            if difference > 0:
                positive_differences.append(difference)
            else:
                negative_differences.append(difference)
        positive_differences.sort()
        negative_differences.sort()
        sorted_differences = positive_differences + negative_differences

        alldec = sorted(
            alldec, key=lambda x: sorted_differences.index(x['difference']))

        total_items = a1.count()
        total_pages = -(-total_items // ITEMS_PER_PAGE)

    return jsonify({
        'current_page': page,
        'total_pages': total_pages,
        'items_per_page': ITEMS_PER_PAGE,
        'total_items': total_items,
        'deceased_details': alldec
    }), 200

    # print(sorted_differences)

    # return jsonify(alldec), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
