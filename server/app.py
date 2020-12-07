from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import vote
import socket
missionGage = 10
alive_list = ['red', 'blue', 'white', 'black']
app = Flask(__name__, static_url_path='/static')

room_mission = {'0':'-1', '1':'-1', '2':'-1'}
@app.route("/whoMission", methods=['GET', 'POST'])
def whoMission():
    if request.method == 'POST':
        returnjson = request.get_json(silent=True, cache=False, force=True)
        if returnjson['room'] == '0':
            return str(room_mission[0])
        elif returnjson['code'] == '1':
            return str(room_mission[1])
        elif returnjson['code'] == '2':
            return str(room_mission[2])
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
@app.route('/missionCompleteSend', methods=['GET', 'POST'])
def missionComplete():
    global missionGage
    if request.method == 'POST':
        missionGage += 10
        print(str(missionGage))
        return str(missionGage)
    else:
        return render_template('mission_test.html')
@app.route('/missionCompleteShow',  methods=['GET', 'POST'])
def missionCompleteShow():
    global room_mission
    max = 100
    mission_bar = '['+ str('█')*missionGage
    for x in range(missionGage,100):
        mission_bar += '. '
    mission_bar += ']'
    if missionGage == 100:
        return redirect(url_for('crewWin'))
    return render_template('mission_now.html', progress = mission_bar)
    #return '<h1>'+'room_0:'+ room_mission['0']+'</h1>'+ '<h1>'+'room_1:'+ room_mission['1']+'</h1>'+ '<h1>'+'mission_gage'+ mission_bar+'</h1>'

@app.route('/crewWin',  methods=['GET', 'POST'])
def crewWin():
    return 'CrewWin'

@app.route('/missionCrewUpdate',  methods=['GET', 'POST'])
def missionCrewUpdate():
    global room_mission
    if request.method == 'POST':
        returnjson = request.get_json(silent=True, cache=False, force=True)
        room_mission[returnjson['room']] = returnjson['type']
        return 'complete:'+ str(room_mission[returnjson['room']])
    else:
        return '<h1>get</h1>'

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
