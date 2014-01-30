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

class BankState:
	def __init__(self, state_string):
		self.entities = {}
		for entity in Entities.keys():
			self.entities[entity] = 0

		muliplier = 1
		parse_state = Multiplier_None()
		for char in state_string.upper():
			if char.isdigit():
				(multiplier, parse_state) = parse_state.add_digit(int(char))
			elif char in self.entities.keys():
				self.entities[char] = multiplier
				multiplier = 1
				parse_state = Multiplier_None()
			else:
				raise Exception("undefined state %s -> %s" % (state_string, char))

	def __repr__(self):
		string = ""
		for entity in self.entities:
			if self.entities[entity] > 0:
				string += "%d%s" % (self.entities[entity], entity)
		return string


class CandMState:
	def __init__(self, init_string):
		(left, right) = init_string.strip().split('|')
		self.left_bank = BankState(left)
		self.right_bank = BankState(right)

	def __repr__(self):
		return "%s|%s" % (self.left_bank, self.right_bank)

initial_state = CandMState('3M3CB|')
print initial_state

goal_state = CandMState('|3M3CB')
print goal_state
