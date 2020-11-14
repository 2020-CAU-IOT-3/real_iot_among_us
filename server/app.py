from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def hello_world():
    return '<h1>among_us_server</h1>'

@app.route('/missionStart')
def missionComplete():
    global mission_up
    if request.method == 'POST':
        f = request.files['file']
        f.save("imposterImage/" + secure_filename(f.filename))
        if isImposter(f) :
            session['job'] = 'imposter'
        else :
            session['job'] = 'crew'
        return '<h1>success upload</h1>'
    return '<h1>among_us_server</h1>'

@app.route('/missionCompleteSend')
def missionComplete():
    return '<h1>among_us_server</h1>'

@app.route('/missionCompleteShow')
def missionCompleteShow():
    return '<h1>among_us_server</h1>'


def isImposter(img):
    return False
