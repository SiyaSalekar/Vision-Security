from flask import Flask, render_template, session, redirect, abort, request, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import os
import bcrypt
import qrcode
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
from . import mydb


app = Flask(__name__)

# DB Connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Siya12345!@localhost/vision_security'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Gmail Login Connect
app.secret_key = "secret"
GOOGLE_CLIENT_ID = "32339361886-h68qo4kbddtfncgup3cqcstngeeav5l5.apps.googleusercontent.com"
clients_secret_file = os.path.join(pathlib.Path(__file__).parent,"client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=clients_secret_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"],
    redirect_uri="https://visionsecurity.tk/callback"
)

# ----Begin Ovidiu's Code
#this is path to images to  be used with flask and HTML.

IMAGES=os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMAGES

placeholder_image=os.path.join(app.config['UPLOAD_FOLDER'], 'placeholder_image.jpg')
# ----End Ovidiu's Code


# --------Begin Siya's Code
def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500) #states do not match, dont trust
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(id_token=credentials._id_token, request=token_request,audience=GOOGLE_CLIENT_ID)
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["google_token"] = credentials._id_token
    return redirect("/secure_area")


@app.route("/logout")
def logout():
    mydb.user_logout(session["google_id"])
    session.clear()
    return redirect("/")


@app.route("/secure_area")
@login_required
def secure_area():
    mydb.add_user_and_login(session['name'], session['google_id'])
    return render_template("index.html", student_id=session['google_id'])


@app.route("/")
def index():
    return render_template("google_login.html")


@app.route("/register",methods=["POST"])
def register():

    student_number = request.form.get("student_number")
    student_pass = request.form.get("password")
    if not student_number:
        return render_template("error.html", message="ID not entered")
    if not student_pass:
        return render_template("error.html", message="Password not entered")

    # convert passwd to bytes
    passwd = student_pass.encode()

    # hashing password
    password = bcrypt.hashpw(passwd, bcrypt.gensalt())
    # imp otherwise stores as bytes
    password_store = str(password)

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=4)
    qr.add_data(password_store)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(f"var/www/FlaskApp/FlaskApp/static/images/{student_number}.png")

    mydb.register_user(student_number, password_store)
    return render_template("index.html")

# -------End Siya's Code


if __name__ == '__main__':
    app.run()