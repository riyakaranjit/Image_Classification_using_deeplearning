import os
from flask import Flask, render_template,request, redirect, url_for,session,flash
from flask import send_from_directory
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import model_from_json
from tensorflow.keras.optimizers import SGD
from PIL import Image
import numpy as np


# opening, reading and storing the file in a variable
json_file = open("/home/riya/Desktop/Imageuploading/Cat Vs Dog Classifier/model/model.json", "r")
load_json_model = json_file.read()
json_file.close()

# loading the json model and it builds a fresh model from model.json json file
loaded_model = model_from_json(
    load_json_model)  # Parses a JSON moimage.filenamedel configuration string and returns a model instance(uncomplied).

# loading the weights into the new model
loaded_model.load_weights("/home/riya/Desktop/Imageuploading/Cat Vs Dog Classifier/model/model.h5")
print("Loaded weights from new model's disk")

# newly reconstructed model is uncomplied
opt = SGD(lr=0.001, momentum=0.9)
loaded_model.compile(optimizer=opt,
                     loss="binary_crossentropy",
                     metrics=["accuracy"]
                     )

def predict_image(img_file):
    model=loaded_model
    #preprocessing test image
    img = Image.open(img_file)  # img_file must be the full path to the sample image
    img = img.resize((200, 200))
    img = np.asarray(img)
    img = img.reshape((1, 200, 200, 3))  # input layers of the model created needs a 4 dimension tensor to work with
    #predict the test image
    result = model.predict(img)
    print(result[0])
    if result[0]==[1.]:
        return "Dog"
    else:
        return "Cat"

app = Flask(__name__)
app.secret_key="super secret key"
app.config["IMAGE_UPLOADS"]="/home/riya/Desktop/Imageuploading/uploads/"


@app.route("/")
def main():
    return ("Hi page welcome back to my guys!")

@app.route("/<name>")
def idk(name):
    return "Hi,%s! Bye." % name #we can use format{}
'''
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("idk",name=user))
    else:
        return render_template("login.html")
'''

@app.route("/img", methods=["GET","POST"])
def img_upload():
    if request.method=="POST":
        if request.files:
            image=request.files["image"]
            if image.filename == "":
                flash("NO IMAGE!")
                return redirect(request.url) #returning to the same page
            if image.filename != "":
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
                flash("IMAGE SAVED!")
                print("Image saved!")
                image_path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
                #if redirecting to predict route; the two commented lines are used
                #session["image_name"]=image.filename
            #return redirect(url_for("predict"))

            final_output = predict_image(image_path)
            return render_template("index.html", prediction=final_output, filename=image.filename)
    return render_template("index.html")

@app.route("/send_image/<filename>")
def send_image(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"],filename)

@app.route("/<name>")
def idk(name):
    return "Hi,%s! Bye." % name
"""
@app.route("/predict", methods =["GET","POST"])
def predict():
    image_name=session.get("image_name")
    image_path=os.path.join(app.config["IMAGE_UPLOADS"],image_name)

    final_output=predict_image(image_path)

    return render_template("predict_image.html",prediction=final_output)
"""

if __name__=="__main__":
    app.run(host="127.0.0.2",port=8080,debug=True)
