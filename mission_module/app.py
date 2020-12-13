import serial


ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
)

def startCommand(command):
    global who_mission
    global mission_thread
    global mission_thread_count
    if command == 's':
        mission_thread_count = 1
        who_mission = [0,0,0,0,0]
        mission_thread = Thread(target=missionstarter)
        mission_timeout_thread = Thread(target=timeoutThread)
    elif command == 'e':
        if mission_thread_count == 1
            mission_thread_count = 0
            max_index = who_mission.index(max(who_mission))
            if max_index != 0 and max_index != 1:
                server_command = "missionCompleteSend"
                r = requests.post(serverAddress+server_command, headers=headers)

def timeoutThread():
    sleep(15)
    mission_thread_count = 0
    output_str = "$t"
    ser.write(output_str.encode())

def missionstarter():
    global who_mission
    global mission_thread_count
    while mission_thread_count:
        server_command = 'whoMission'
        data = {'room': str(room_number)}
        r = requests.post(serverAddress+server_command, headers=headers, data=json.dumps(data))
        who_mission[int(r)] += 1
        sleep(1/2)

serverAddress = 'http://192.168.0.17:5000/'
headers = {'Content-Type': 'application/json'}
room_number = 1

who_mission = [0,0,0,0,0] #None, imposter, crew1, crew2, crew3
mission_thread = None
mission_thread_count = 0
buffer = ''
while True:
    if ser.readable():
        res = ser.read()
        while True:
            if res == '$':
                buffer = ''
                break;
            while True:
                res = ser.read()
                if res == '\n':
                    break;
                else :
                    buffer += res
            command = buffer[0]
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
