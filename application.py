from flask import Flask, render_template
import qrcode
import os

#this is path to images to  be used with flask and HTML.

app = Flask(__name__)
IMAGES=os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMAGES

placeholder_image=os.path.join(app.config['UPLOAD_FOLDER'], 'placeholder_image.jpg')

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
    app.run(debug=True)

