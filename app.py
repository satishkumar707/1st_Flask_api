import os
from uuid import uuid4

from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)  




APP_ROOT = os.path.dirname(os.path.abspath(__file__))

classes = ['cat','dog'] 

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    
        import numpy as np
        from keras_preprocessing import image

        from keras.models import load_model
        new_modell = load_model('cat_dog_classifierr.h5')
        # new_model.summary()
        test_image = image.load_img('images/' + filename, target_size=(128, 128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = new_modell.predict(test_image)
        ans = np.argmax(result, axis=1)
        if ans==1:
            prediction="dog"
        else:
            prediction = "cat"
        
    return render_template("template.html",image_name=filename, text=prediction)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(debug=False)

