# -*- coding: utf-8 -*-
import os
import re
from nut import Print

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

    # ...

def auth(id, password, address):
    global connected_users, session_counts
    if id not in users:
        return None

    user = users[id]

    if user.requireAuth == 0 and address == user.remoteAddr:
        return user

    if user.remoteAddr and user.remoteAddr != address:
        return None

    if user.password != password:
        return None

    # Check if the user is already connected
    if id in connected_users:
        if session_counts.get(id, 0) >= 2:
            # User has reached the maximum number of sessions
            return None
    else:
        session_counts[id] = 0

    # Increment the session count for the user
    session_counts[id] += 1

    # User is not already connected, allow access and add to connected_users
    connected_users[id] = user
    return user

def disconnect(id):
    global connected_users, session_counts
    if id in connected_users:
        del connected_users[id]
        if id in session_counts:
            session_counts[id] -= 1
            if session_counts[id] <= 0:
                del session_counts[id]

# ...

def load(path='conf/users.conf'):
    global users

    if not os.path.isfile(path):
        id = 'guest'
        users[id] = User()
        users[id].setPassword('guest')
        users[id].setId('guest')
        return

    firstLine = True
    map = ['id', 'password', 'isAdmin', 'remoteAddr']  # Aggiungi 'remoteAddr' alla mappa
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

            Print.info('loaded user ' + str(t.id))

# ...

load()
