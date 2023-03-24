from flask import Flask, render_template, request
import json
from PIL import Image
import ActiveContour
import imghdr
import numpy as np
import Hough
from skimage.filters import gaussian

object_detection_app = Flask(__name__)

@object_detection_app.route("/")
def page1():
    return render_template("page1.html")

@object_detection_app.route("/page2")
def page2():
    return render_template("page2.html")


@object_detection_app.route("/index")
def index():
    return render_template("index.html")

@object_detection_app.route("/activeContour",methods =["POST","GET"])
def activeContour():
    image = request.files['image']
    imageShow = Image.open(image)
    imageShow.save(f"static/assets/image.png")
    s = np.linspace(0, 2*np.pi, 400)
    r = 100 + 100*np.sin(s)
    c = 220 + 100*np.cos(s)
    init = np.array([r, c]).T
    snake = ActiveContour.active_contour(gaussian(imghdr, 3),
                       init)
    return "Active Contour is Done"

@object_detection_app.route("/hough",methods =["POST","GET"])
def hough():
    image = request.files['image']
    imageShow = Image.open(image)
    imageShow.save(f"static/assets/image.png")
    return "Hough detection is Done"

@object_detection_app.route("/data",methods = ["POST","GET"])
def data():
    data =  request.form['cropperData'] 
    jsonData = json.loads(data)
    print(jsonData)
    return "Data is sent"


if __name__ == "__main__":
    object_detection_app.run()