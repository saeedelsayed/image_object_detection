from flask import Flask, render_template, request
import json
from PIL import Image

object_detection_app = Flask(__name__)

@object_detection_app.route("/")
def page1():
    return render_template("page1.html")

@object_detection_app.route("/page2")
def page2():
    return render_template("page2.html")


@object_detection_app.route("index")
def index():
    return render_template("index.html")

@object_detection_app.route("/activeContour",methods =["POST","GET"])
def activeContour():
    image = request.files['image']
    imageShow = Image.open(image)
    imageShow.save(f"static/assets/image.png")
    return "Active Contour is Done"

@object_detection_app.route("/data",methods = ["POST","GET"])
def data():
    data =  request.form['cropperData'] 
    jsonData = json.loads(data)
    print(jsonData)
    return "Data is sent"


if __name__ == "__main__":
    object_detection_app.run()