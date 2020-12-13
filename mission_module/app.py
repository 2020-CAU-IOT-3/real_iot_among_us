import serial
import time
import threading
import os
import requests,json
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
)

def startCommand(command):
    global who_mission
    global mission_thread
    global mission_thread_timeout
    global mission_thread_count
    if command == 's':
        print("command:" + "s")
        mission_thread_count = 1
        who_mission = [0,0,0,0,0]
        mission_thread =  threading.Thread(target=missionstarter)
        mission_thread.start()
        mission_thread_timeout =  threading.Thread(target=timeoutThread)
        mission_thread_timeout.start()
    elif command == 'e':
        print("command:" + "e")
        if mission_thread_count == 1:
            mission_thread_count = 0
            max_index = who_mission.index(max(who_mission))
            if max_index != 0 and max_index != 1:
                server_command = "missionCompleteSend"
                r = requests.post(serverAddress+server_command, headers=headers)

def timeoutThread():
    global mission_thread_count
    global timeout_count
    print("start_timeout")
    while True:
        if(timeout_count > 0)
            timeout_count -= 1
        print(timeout_count)
        if(timeout_count <= 0):
            break;
        time.sleep(1)
    mission_thread_count = 0
    output_str = "$t\n"
    print(output_str)
    ser.write(output_str.encode())

def missionstarter():
    global who_mission
    global mission_thread_count
    print("mission_start")
    while mission_thread_count:
        server_command = 'whoMission'
        data = {'room': str(room_number)}
        r = requests.post(serverAddress+server_command, headers=headers, data=json.dumps(data))
        print(r.text)
        who_mission[int(r.text)] += 1
        time.sleep(1)

serverAddress = 'http://192.168.0.17:5000/'
headers = {'Content-Type': 'application/json'}
room_number = 1

who_mission = [0,0,0,0,0] #None, imposter, crew1, crew2, crew3
mission_thread = None
mission_thread_timeout = None
mission_thread_count = 0
timeout_count = 30

while True:
    if ser.readable():
        buffer_str = []
        res = ser.read()
        print('res:"' + str(res)+'"')
        if res == '$':
            print('reset_buffer')
            buffer_str = []
            mission_thread_count = 0
            timeout_count = 30
            if mission_thread_timeout != None:
                print("kill timeout")
                mission_thread_timeout.stop()
            while True:
                res = ser.read()
                #print('res:"' + str(res)+'"')
                if res == '\n':
                    break;
                else :
                    buffer_str.append(res)
            print(buffer_str)
            command = buffer_str[0]
            startCommand(command)





# Serial.write()
"""
ser.write(output_str.encode())
"""

# Serial.read()
"""
if ser.readable():
    res = ser.readline()
    print(res.decode()[:len(res)-1])
"""
