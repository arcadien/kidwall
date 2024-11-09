from flask import Flask, render_template

from Model import Application, Registration

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/registrations', methods=['GET'])
def registrations():
    fortnite = Application("Fortnite")
    youtube = Application("Youtube")
    ecoleDirecte = Application("Ecole_Directe")
    rf = Registration(fortnite, False)
    ry= Registration(youtube, False)
    re = Registration(ecoleDirecte, True)
    registrations = [rf, ry, re]
    return render_template('registrations.html',registrations=registrations)