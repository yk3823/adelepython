# from flask import Flask, request ,jsonify
# from pymongo import MongoClient

# app = Flask(__name__)
# data = {} 
# mongo_uri = "mongodb+srv://adelekeinan:J0seph123%21@clusteradele.thiqpjx.mongodb.net/"
# client = MongoClient(mongo_uri)
# db = client['projectdb']

# @app.route('/', methods=['POST'])
# def receive_json():
#     data = request.get_json()

#     if not data:
#         return jsonify({"message": "No JSON received"}), 400
#     #     print(data)  # Print the data to the server console for debugging
#     return jsonify(data)  # Echo back the received JSON data

# @app.route('/emailverified/token', methods=['GET'])
# def verify_email(token):
    
#     return jsonify({"message": f"Email has been verified with token {token}!"}), 200

# # @app.route('/emailverified', methods=['POST'])
# # def mail():        
# #     return jsonify({"ok":"document has been created!!"}), 200 
# #     # if (request.json):
# #     #     user_data = request.json

   
# #     #     db.users.update_one(
# #     #         {"email": user_data['email']},  # Query
# #     #         {"$set": user_data},  # Update
# #     #         upsert=True  # If not exists, insert
# #     #     )

# #     #     return {'message': 'User data updated'}, 200
# #     # else:
# #     #     return {"error":"error"},404

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5020)
