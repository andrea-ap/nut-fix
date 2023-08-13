import os
import re

users = {}

class User:
    def __init__(self):
        self.id = None
        self.password = None
        self.isAdmin = False
        self.remoteAddr = None
        self.requireAuth = True
        self.switchHost = None
        self.switchPort = None

    # ... (resto del codice per la classe User) ...

def find_user_by_credentials(username, password):
    for user in users.values():
        if user.id == username and user.password == password:
            return user
    return None

def auth(id, password, address):
    if id in users:
        user = users[id]

        if user.requireAuth == 0 and address == user.remoteAddr:
            return user

        if user.remoteAddr and user.remoteAddr != address:
            return None

        authenticated_user = find_user_by_credentials(id, password)
        if authenticated_user and authenticated_user != user:
            return None

        return authenticated_user

def load(path='conf/users.conf'):
    global users

    if not os.path.isfile(path):
        id = 'guest'
        users[id] = User()
        users[id].setPassword('guest')
        users[id].setId('guest')
        return

    firstLine = True
    map = ['id', 'password', 'isAdmin']
    with open(path, encoding="utf-8-sig") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            if firstLine:
                firstLine = False
                if re.match(r'[A-Za-z\|\s]+', line, re.I):
                    map = line.split('|')
                    continue

            t = User()
            t.loadCsv(line, map)

            users[t.id] = t

def export(fileName='conf/users.conf', map=['id', 'password', 'isAdmin']):
    os.makedirs(os.path.dirname(fileName), exist_ok=True)
    global users
    buffer = ''

    buffer += '|'.join(map) + '\n'
    for k, t in users.items():
        buffer += t.serialize(map) + '\n'

    with open(fileName, 'w', encoding='utf-8-sig') as csv:
        csv.write(buffer)

load()
