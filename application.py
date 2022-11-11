from flask import Flask, render_template
import qrcode
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/qrgenerate/<studentID>')
def generateCode(studentID):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10,border=4)
    qr.add_data(studentID)
    qr.make(fit=True)
    img = qr.make_image(fill_color='green', back_color = 'white')
    img.save(f"templates/images/{studentID}.png")
    return render_template("qrgenerator.html")

if __name__ == '__main__':
    #app.run(host='192.168.43.136',port=9000)
    app.run(debug=True)