from flask import Flask, request, jsonify
from databaseMain import MongoDB
from bson import json_util
import json
from sendemail import Email
from message import Message
from date import userDate
from datetime import datetime
import uuid
from pymongo import MongoClient
from flask_cors import CORS



client = MongoClient('localhost', 27017)
db = client['memorial_site']
collection = db['deceased']
app = Flask(__name__)
CORS(app)
data = {}


@app.route('/userdate', methods=['POST'])
def userdate():
    if not request.json:
        return jsonify({"error": "No data sent"}), 400
    data = request.get_json()
    fullname = data.get('fullname')
    date_of_death = data.get('date_of_death')
    date_next = data.get('date_next')
    date_reminder = data.get('date_reminder')
    user_id = data.get('user_id')
    if None in [fullname, date_of_death, date_next, date_reminder, user_id]:
        return jsonify({"error": "Missing data fields"}), 400
    try:
        date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
        date_next = datetime.strptime(date_next, '%Y-%m-%d')
        date_reminder = datetime.strptime(date_reminder, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    deceased_id = uuid.uuid4().hex
    doc = {
        'deceased_id': deceased_id,
        'fullname': fullname,
        'date_of_death': date_of_death,
        'date_next': date_next,
        'date_reminder': date_reminder,
        'user_id': user_id,
        'created_at': datetime.utcnow()
    }
    collection.insert_one(doc)

  

    return jsonify({"message": "deceased date processed"}), 200


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    email = data.get("email")
    a1 = MongoDB("users")
    existing_user = a1.read({"email": email})
    if existing_user:
        error_message = "Email already exists in the system"
        print(error_message) 
        return jsonify({"error": "Email already exists in the system"}), 400
       

    if not request.json:
        return jsonify({"error": "No data sent"}), 400

   
    # print(data["user_verified"])
    print(data["email"])
    a1 = MongoDB("users")
    b1 = Email(data["email"], "adelekeinan@gmail.com", "ukwdpyraorxbqcsr")
    d1 = userDate(datetime.strptime(data['date'], '%Y/%m/%d'))

    c1 = Message(data["email"], "hello").getMessage()
    b1.send_email(c1["subject"], c1["message"])
    a1.create(data)

    # b1 = mainEmail.Email(data["email"],"adelekeinan@gmail.com","ukwdpyraorxbqcsr")
    created_message = "Email created"
    print(created_message) 
    return jsonify({"ok": "document has been created!!"}), 200


@app.route('/emailverified/<token>', methods=['GET'])
def verify_email(token):
    email = token
    a1 = MongoDB("users")
    a1.update({"email": email}, {"user_verified": True})
    if a1.read({"email": email, "user_verified": True}):
        return jsonify({"message": f"Email has been verified with token {token}! You can now add a deceased person on the site."}), 200
    else:
        return jsonify({"error": "Invalid token or email not verified."}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
    # def main():
#     d = userDate(2010, 6, 2)
#     d.print_dates()
#     next_date = d.get_next_date()
#     d.print_reminder(next_date)


# if __name__ == "__main__":
#     main()
    # if not request.json:
    #     return jsonify({"error": "No data sent"}), 400

    # key = request.json.get('key')
    # value = request.json.get('value')

    # if key in data:
    #     return jsonify({"error": "Key already exists"}), 400

    # data[key] = value
    # return jsonify({"message": f"{key} has been created."}), 201
# @app.route('/emailverified', methods=['GET'])
# def mail():


#     return jsonify({"ok":"document has been created!!"}), 200
# @app.route('/read', methods=['GET'])
# def read():
#     # key = request.args.get('key')

#     query = {"phone":"5555555"}

#     data = a1.read(query)
#     # Use json_util.dumps to convert ObjectId to string
#     # json.loads takes string and makes it a python object
#     data_json = json.loads(json_util.dumps(data))
#     #jsonify - python and converts it to json
#     return jsonify(data_json)


# @app.route('/update', methods=['PATCH'])
# def update():
#     if not request.json:
#         return jsonify({"error": "No data sent"}), 400

#     key = request.json.get('key')
#     value = request.json.get('value')

#     if key not in data:
#         return jsonify({"error": "Key not found"}), 404

#     data[key] = value
#     return jsonify({"message": f"{key} has been updated."}), 200

# @app.route('/delete', methods=['DELETE'])
# def delete():
#     key = request.args.get('key')

#     if key not in data:
#         return jsonify({"error": "Key not found"}), 404
#     del data[key]
#     return jsonify({"message": f"{key} has been deleted."}), 200
  # datetime_str = data.get('datetime1')
    # print(datetime_str)

    # if datetime_str is None or datetime_str == "":
    #     return jsonify({"error": "Invalid datetime format"}), 400

    # try:
    #     datetime_obj = datetime.strptime(str(datetime_str), '%Y-%m-%d')
    # except ValueError:
    #     return jsonify({"error": "Invalid datetime format"}), 400

    # d = userDate(datetime_obj.year, datetime_obj.month, datetime_obj.day)
    # d.print_dates()
    # next_date = d.get_next_date()
    # d.print_reminder(next_date)
