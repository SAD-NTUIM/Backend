from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
# from flask_cors import cors_origin
from cr2tojpg import img_conv
from wb_module import whiteBalance
app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
@cross_origin("*") 
def index():
    if (request.method =='POST'):
        testing_info = request.get_json()
        print(testing_info)
        return jsonify({"You sent": testing_info}), 201
    else:
        return jsonify({"about": "Post fail"})

#Input : filename
#Output : base64 image
@app.route("/CR2toJpg", methods=['GET','POST'])
@cross_origin("*") 
def CR2toJpg():
    if (request.method =='POST'):
        process_info = request.get_json()
        location = process_info["location"]
        print(process_info)
        image = img_conv(location)
        return jsonify({"output location": image}), 201
    else:
        return jsonify({"about": "No process"})

#Input : filename, x, y
#Output : base64 image
@app.route("/whiteBalance", methods=['GET','POST'])
@cross_origin("*")
def wb():
    if (request.method =='POST'):
        process_info = request.get_json()

        location = process_info["location"]
        x = process_info["x"]
        y = process_info["y"]

        print(process_info)
        image = whiteBalance(location, x, y)
        return jsonify({"output location": image}), 201
    else:
        return jsonify({"about": "No process"})

if __name__ == '__main__':
    app.run(debug=True)