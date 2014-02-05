#!/usr/bin/python

Entities = {	'M' : "Missionaries",
				'C' : "Cannibals", 
				'B' : "Boats"}

class Multiplier_None:
	def add_digit(self, digit):
		return (digit, Multiplier_Exists(digit))

class Multiplier_Exists:
	def __init__(self, digit):
		self.multiplier = digit
		
	def add_digit(self, digit):
		self.multiplier = self.multiplier * 10 + digit
		return (self.multiplier, this)

class EntityDictionary:
	def __init__(self):
		self.entities = {}
		for entity in Entities.keys():
			self.entities[entity] = 0
	
	def __repr__(self):
		return repr(self.entities)

	def __eq__(self, other):
		return self.entities == other.entities

	def __getitem__(self, key):
		return self.entities[key]

	def __setitem__(self, key, value):
		self.entities[key] = value

	def __iadd__(self, other):
		for entity in self.entities:
			self.entities[entity] += other.entities[entity]
		return self

	def __add__(self, other):
		result = EntityDictionary()
		result += self
		result += other
		return result

	def __isub__(self, other):
		for entity in self.entities:
			self.entities[entity] -= other.entities[entity]
		return self

	def __sub__(self, other):
		result = EntityDictionary()
		result += self
		result -= other
		return result

	def has_all_positive_values(self):
		for entity in self.entities:
			if self.entities[entity] < 0:
				return False
		return True

	def has_enough_missionaries(self):
		return self.entities['M'] >= self.entities['C'] or self.entities['M'] == 0

	def has_boat(self):
		return self.entities['B'] > 0

	def entityList(self):
		return self.entities.keys()


def ParseStateString(state_string):
	entities = EntityDictionary()
	multiplier = 1
	parse_state = Multiplier_None()
	for char in state_string.upper():
		if char.isdigit():
			(multiplier, parse_state) = parse_state.add_digit(int(char))
		elif char in entities.entityList():
			entities[char] = multiplier
			multiplier = 1
			parse_state = Multiplier_None()
		else:
			raise Exception("undefined state %s -> %s" % (state_string, char))

	return entities

Actions = [ ParseStateString(x) for x in "M C 2M 2C MC".split() ]

class BankState:
	def __init__(self, state_string):
		self.entities = ParseStateString(state_string)

	def __repr__(self):
		string = ""
		for entity in self.entities.entityList():
			if self.entities[entity] > 0:
				string += "%d%s" % (self.entities[entity], entity)
		return string

	def __str__(self):
		string = ""
		spacer = ""
		for entity in self.entities.entityList():
			if self.entities[entity] > 0:
				string += spacer + "%d%s" % (self.entities[entity], entity)
				spacer = " "
		return string
		
	def __eq__(self, other):
		return self.entities == other.entities

	def departure_action_valid(self, action):
		result = self.entities - action
		return result.has_enough_missionaries() and result.has_all_positive_values()
		
	def arrival_action_valid(self, action):
		result = self.entities + action
		return result.has_enough_missionaries()

	def has_boat(self):
		return self.entities.has_boat()


class CandMState:
	def __init__(self, init_string):
		(left, right) = init_string.strip().split('|')
		self.left_bank = BankState(left)
		self.right_bank = BankState(right)

	def __repr__(self):
		return "%s | %s" % (self.left_bank, self.right_bank)

	def __eq__(self, other):
		return self.left == other.left and self.right == other.right

	def get_successors(self):
		if self.left_bank.has_boat():
			depart = self.left_bank
			arrive = self.right_bank
		else:
			arrive = self.left_bank
			depart = self.right_bank
		return [action for action in Actions if arrive.arrival_action_valid(action) and depart.departure_action_valid(action)]

initial_state = CandMState('3M3CB|')
goal_state = CandMState('|3M3CB')


