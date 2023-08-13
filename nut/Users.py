# -*- coding: utf-8 -*-
import os
import re
from nut import Print

users = {}
active_sessions = {}  # Dictionary to track active user sessions

class User:
    # ... (rest of the class remains the same)
    
    def __init__(self):
		self.id = None
		self.password = None
		self.isAdmin = False
		self.remoteAddr = None
		self.requireAuth = True
		self.switchHost = None
		self.switchPort = None

	def loadCsv(self, line, map=[]):
		split = line.split('|')
		for i, value in enumerate(split):
			if i >= len(map):
				Print.info('invalid map index: ' + str(i) + ', ' + str(len(map)))
				continue

			i = str(map[i])
			methodName = 'set' + i[0].capitalize() + i[1:]
			method = getattr(self, methodName, lambda x: None)
			method(value.strip())

	def serialize(self, map=['id', 'password']):
		r = []
		for i in map:

			methodName = 'get' + i[0].capitalize() + i[1:]
			method = getattr(self, methodName, lambda: methodName)
			r.append(str(method()))
		return '|'.join(r)

	def setId(self, id):
		self.id = id

	def getId(self):
		return str(self.id)

	def setPassword(self, password):
		self.password = password

	def getPassword(self):
		return self.password

	def setIsAdmin(self, isAdmin):
		try:
			self.isAdmin = False if int(isAdmin) == 0 else True
		except BaseException:
			pass

	def getIsAdmin(self):
		return 1 if self.isAdmin else 0

	def setRequireAuth(self, requireAuth):
		try:
			self.requireAuth = False if int(requireAuth) == 0 else True
		except BaseException:
			pass

	def getRequireAuth(self):
		return str(self.requireAuth)

	def setSwitchHost(self, host):
		self.switchHost = host

	def getSwitchHost(self):
		return self.switchHost

	def setSwitchPort(self, port):
		try:
			self.switchPort = int(port)
		except BaseException:
			pass

	def getSwitchPort(self):
		return self.switchPort

def first():
	global users
	for id, user in users.items():
		return user
	return None

def auth(id, password, address):
    global active_sessions

    if id not in users:
        return None

    user = users[id]

    if id in active_sessions:
        return None  # User already has an active session

    if user.requireAuth == 0 and address == user.remoteAddr:
        active_sessions[id] = True  # Mark the user as having an active session
        return user

    if user.remoteAddr and user.remoteAddr != address:
        return None

    # TODO: save password hash in config
    if user.password != password:
        return None

    active_sessions[id] = True  # Mark the user as having an active session
    return user

def end_session(user_id):
    global active_sessions
    if user_id in active_sessions:
        del active_sessions[user_id]  # Remove the user's active session

# ... (rest of the code remains the same)




	
