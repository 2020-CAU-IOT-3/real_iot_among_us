from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import vote
import socket
missionGage = 0
alive_list = ['red', 'blue', 'white', 'black']
app = Flask(__name__, static_url_path='/static')

room_mission = {'0':'-1', '1':'-1', '2':'-1'}
@app.route("/whoMission", methods=['GET', 'POST'])
def whoMission():
    if request.method == 'POST':
        returnjson = request.get_json(silent=True, cache=False, force=True)
        if returnjson['room'] == '0':
            return "<h1>"+ str(room_mission[0]) + "</h1>"
        elif returnjson['code'] == '1':
            return "<h1>"+ str(room_mission[1]) + "</h1>"
        elif returnjson['code'] == '2':
            return "<h1>"+ str(room_mission[2]) + "</h1>"
        return str(returnjson)
    if request.method == 'GET':
        return 'test'

@app.route('/')
def hello_world():
    return '<h1>among_us_server</h1>'
"""
@app.route('/missionStart')
def missionStart():
    if request.method == 'POST':
        f = request.files['file']
        f.save("imposterImage/" + secure_filename(f.filename))
        if isImposter(f) :
            session['job'] = 'imposter'
        else :
            session['job'] = 'crew'
        return '<h1>success upload</h1>'
    else :
        return render_template("mission_start.html")
"""
@app.route('/missionCompleteSend')
def missionComplete():
    global missionGage
    if request.method == 'POST':
            missionGage += 10
    return '<h1>among_us_server</h1>'

@app.route('/missionCompleteShow')
def missionCompleteShow():
    return '<h1>'+str(missionGage)+'</h1>'

@app.route('/missionCrewUpdate')
def missionCrewUpdate():
    return '<h1>'+str(missionGage)+'</h1>'

@app.route('/vote')
def vote_page():
    global alive_list
    killed_people = 1
    vote.vote(alive_list)
    return '<h1>' + str(killed_people) + '</h1>'

if __name__ == '__main__':
    IP = str(socket.gethostbyname(socket.gethostname()))
    app.run(host="165.194.44.20", port=5000, debug=False)
    app.run()
