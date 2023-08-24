import os
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
from pyluach import dates
import requests
import json
import paypalrestsdk


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


def get_access_token(client_id, client_secret):
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    auth = (client_id, client_secret)
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, auth=auth, data=data)
    print(response.json().get("access_token", None))
    return response.json().get("access_token", None)


# get_access_token("AX_vZcLnrEtNrNc9wK-JoHk81p4ErlRAIC_CelJpNYaRgK2ICEDjwL2_ekUfkecDDxu8l3myRpmBaJBh",
#                  "EKLhvvxau-AOYFJ60SPfwUviLaIJe5KMac-ETQWcKxxK3-qDWjZAEUCMJI_EC86j4usi51LccvuoaE-7")


def create_order(access_token, amount, return_url, cancel_url):
    print("access:\n", access_token)
    url = "https://api.sandbox.paypal.com/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "value": f"{amount:.2f}",
                "currency_code": "USD"
            },
            "description": "Payment for your product"
        }],
        "application_context": {
            "return_url": return_url,
            "cancel_url": cancel_url
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(order_data))
    return response.json()


def main():
    # You'd typically get these values from your application's configuration or secrets management.
    CLIENT_ID = "AX_vZcLnrEtNrNc9wK-JoHk81p4ErlRAIC_CelJpNYaRgK2ICEDjwL2_ekUfkecDDxu8l3myRpmBaJBh"
    CLIENT_SECRET = "EKLhvvxau-AOYFJ60SPfwUviLaIJe5KMac-ETQWcKxxK3-qDWjZAEUCMJI_EC86j4usi51LccvuoaE-7"

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    print(access_token)
    if access_token:
        amount = 10.00  # or any desired amount
        return_url = "https://google.com"
        cancel_url = "https://youtube.com"

        order_response = create_order(
            access_token, amount, return_url, cancel_url)
        print(order_response)
    else:
        print("Failed to obtain access token.")

# CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
# CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')


@app.route('/create_payment', methods=['POST'])
def create_payment():
    payment_type = request.json.get('type')

    # Define the amount based on payment type. Adjust as necessary.
    if payment_type == 'kaddish':
        amount = 10.00
    elif payment_type == 'tehillim':
        amount = 5.00
    else:
        return jsonify({"error": "Invalid payment type"}), 400

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    order_response = create_order(
        access_token,
        amount,
        "https://google.com",
        "https://ynet.co.il"
    )

    # Extract the approval URL for the user to complete the payment
    approval_url = next(
        (link.get("href") for link in order_response.get(
            "links", []) if link.get("rel") == "approve"),
        None
    )

    if approval_url:
        return jsonify({"redirect_url": approval_url})
    else:
        return jsonify({"error": "Payment creation failed"}), 400


# @app.route('/execute_payment', methods=['GET'])
# def execute_payment():
#     payment_id = request.args.get('paymentId')
#     payer_id = request.args.get('PayerID')

#     payment = paypalrestsdk.Payment.find(payment_id)

#     if payment.execute({"payer_id": payer_id}):
#         print('Payment executed successfully')
#         return jsonify({"success": "Payment executed successfully"}), 200
#     else:
#         print(payment.error)
#         return jsonify({"error": "Payment execution failed"}), 400


@app.route('/create_images_collection', methods=['POST'])
def create_images_collection():
    mongo.create_images_collection()
    return jsonify({"message": "Images collection created"}), 200


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

    print(data["email"])
    a1 = MongoDB("users")
    b1 = Email(data["email"], "adelekeinan@gmail.com", "voacfoofzkdckeao")
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
        return redirect(redirect_url, code=302)

    else:
        return jsonify({"error": "Invalid token or email not verified."}), 400


@app.route('/deceased', methods=['POST'])
def save_deceased_details():
    useremail = request.form.get('token')
    a1 = MongoDB("users")
    b1 = MongoDB("deceased")

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
            'dateOfDeath': datetime.strptime(dateOfDeath, '%Y-%m-%d'),
            'photo_id': photo_id
        }

        res_deceasedId = b1.create(deceased_dict)
        print(res_deceasedId)

        querY = {"email": useremail}
        deceasedId = [res_deceasedId]

        a1.update_array(querY, deceasedId)

        return jsonify({"message": "Deceased details saved"}), 200
    return jsonify({"error": "No photo found"}), 400


@app.route('/get_deceased_details', methods=['GET'])
def get_deceased_details():

    page = int(request.args.get('page', 1))
    skip_records = (page - 1) * ITEMS_PER_PAGE

    current_date = datetime.now()
    pipeline = [
        {
            "$addFields": {
                "differenceInDays": {
                    "$subtract": [
                        {"$dayOfYear": "$dateOfDeath"},
                        {"$dayOfYear": current_date}
                    ]
                }
            }
        },
        {
            "$addFields": {
                "isFuture": {
                    "$cond": [
                        {"$gte": ["$differenceInDays", 0]},
                        1,
                        0
                    ]
                }
            }
        },
        {
            "$sort": {
                "isFuture": -1,  # prioritize future dates
                "differenceInDays": 1
            }
        },
        {
            "$skip": skip_records
        },
        {
            "$limit": ITEMS_PER_PAGE
        },

    ]

    deceased_details = list(collection.aggregate(pipeline))
    fs = GridFS(db)

    alldec = []
    for result in deceased_details:
        if 'photo_id' in result:
            image = fs.get(result['photo_id'])
            encoded_image = base64.b64encode(image.read()).decode('ascii')

            date_of_death = result.get('dateOfDeath')
            hebrew_date_calculated = dates.HebrewDate.from_pydate(
                date_of_death)
            hebrew_date_string = hebrew_date_calculated.hebrew_date_string()

            data = {
                'name': result['name'],
                'photo_id': encoded_image,
                'difference': result['differenceInDays'],
                'dateOfDeath': datetime.strftime(result['dateOfDeath'], '%Y-%m-%d'),
                'hebrew_date': hebrew_date_string

            }
            alldec.append(data)

    total_items = collection.count_documents({})
    total_pages = -(-total_items // ITEMS_PER_PAGE)

    return jsonify({
        'current_page': page,
        'total_pages': total_pages,
        'items_per_page': ITEMS_PER_PAGE,
        'total_items': total_items,
        'deceased_details': alldec
    }), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = mongo.read({'email': email, 'password': password})

    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)


# def get_day_and_month(date_str):
#     if isinstance(date_str, str):
#         date_obj = datetime.strptime(date_str, '%Y-%m-%d')
#     elif isinstance(date_str, datetime):
#         date_obj = date_str
#     else:
#         raise TypeError(
#             "Input should be either string in '%Y-%m-%d' format or a datetime object.")
#     return date_obj.month, date_obj.day

# @app.route('/get_deceased_details', methods=['GET'])
# def get_deceased_details():
#     page = int(request.args.get('page', 1))
#     alldec = []
#     a1 = MongoDB("deceased")
#     skip_records = (page - 1) * ITEMS_PER_PAGE
#     deceased_details = a1.read(
#         skip=skip_records, limit=ITEMS_PER_PAGE, sort=[("dateOfDeath", 1)])
#     fs = GridFS(db)
#     current_month, current_day = get_day_and_month(
#         datetime.now().strftime('%Y-%m-%d'))
#     positive_differences = []
#     negative_differences = []
#     for result in deceased_details:
#         if 'photo_id' in result:
#             image = fs.get(result['photo_id'])
#             encoded_image = base64.b64encode(image.read()).decode('ascii')
#             deceased_month, deceased_day = get_day_and_month(
#                 result['dateOfDeath'])
#             difference = ((datetime(2000, deceased_month, deceased_day) -
#                            datetime(2000, current_month, current_day)).days)

#             data = {
#                 'name': result['name'],
#                 'photo_id': encoded_image,
#                 'difference': difference,
#                 'dateOfDeath': datetime.strftime(result['dateOfDeath'], '%Y-%m-%d')

#             }
#             alldec.append(data)

#             if difference > 0:
#                 positive_differences.append(difference)
#             else:
#                 negative_differences.append(difference)
#         positive_differences.sort()
#         negative_differences.sort()
#         sorted_differences = positive_differences + negative_differences

#         alldec = sorted(
#             alldec, key=lambda x: sorted_differences.index(x['difference']))

#     total_items = a1.count()
#     total_pages = -(-total_items // ITEMS_PER_PAGE)

#     return jsonify({
#         'current_page': page,
#         'total_pages': total_pages,
#         'items_per_page': ITEMS_PER_PAGE,
#         'total_items': total_items,
#         'deceased_details': alldec
#     }), 200

    # print(sorted_differences)

    # return jsonify(alldec), 200
