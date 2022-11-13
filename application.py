from flask import Flask, render_template
import qrcode
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    #app.run(host='192.168.43.136',port=9000)
    app.run(debug=True)