from flask import Flask, render_template

object_detection_app = Flask(__name__)

@object_detection_app.route("/")
def page1():
    return render_template("page1.html")

@object_detection_app.route("/page2")
def page2():
    return render_template("page2.html")

if __name__ == "__main__":
    object_detection_app.run()