from flask import Flask, render_template, request, redirect, json
import os
from flask_mysqldb import MySQL
import bcrypt
import qrcode

app = Flask(__name__)


# ----Begin Ovidiu's Code
#this is path to images to  be used with flask and HTML.

IMAGES=os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = IMAGES

placeholder_image=os.path.join(app.config['UPLOAD_FOLDER'], 'placeholder_image.jpg')
# ----End Ovidiu's Code

# --------Begin Siya's Code
# database connect
app.config['MYSQL'] = 'localhost'
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = 'vision_security'

mysql = MySQL(app)

# database connect endRegion

@app.route("/", methods = ["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return render_template("greet.html")


@app.route("/register",methods=["POST"])
def register():

    student_number = request.form.get("student_id")
    email = request.form.get("student_email")
    end_date = request.form.get("end_date")
    if not student_number:
        return render_template("error.html", message="Invalid ID")
    if not email:
        return render_template("error.html", message="Invalid Email")
    if not end_date:
        return render_template("error.html", message="Invalid End Date")

    # convert passwd to bytes
    passwd = request.form.get("password").encode()

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
    img.save(f"static/images/{student_number}.png")

    cursor = mysql.connection.cursor()
    cursor.execute("insert into student(student_number, student_email, student_password, course_end_date) values (%s, %s, %s, %s) ", (student_number, email, password_store, end_date))
    mysql.connection.commit()
    cursor.close()
    return redirect("/")


# -------End Siya's Code

if __name__ == '__main__':
    app.run()