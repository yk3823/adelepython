from flask import Flask, request, jsonify
from databaseMain import MongoDB
from bson import json_util 
import json
from sendemail import Email
from message import Message




app = Flask(__name__)

# Storing data in a dictionary for simplicity. 
# In a real-world application, you would typically use a database.
data = {}

@app.route('/create', methods=['POST'])
def create():
    if not request.json:
        return jsonify({"error": "No data sent"}), 400

    data = request.get_json()
    # print(data["user_verified"])
    print(data["email"])
    a1 = MongoDB("users")
    b1 = Email(data["email"],"adelekeinan@gmail.com","ukwdpyraorxbqcsr")
    c1 = Message(data["email"],"hello").getMessage()
    b1.send_email("Hello welcome to adele website",c1["message"])
    a1.create(data)

    # b1 = mainEmail.Email(data["email"],"adelekeinan@gmail.com","ukwdpyraorxbqcsr")
    
        
    return jsonify({"ok":"document has been created!!"}), 200 
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)