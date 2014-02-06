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
	def __init__(self, state_string = None, copy = None):
		if copy:
			self.entities = copy.entities
		else:
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

	def __iadd__(self, action):
		self.entities += action
		return self

	def __isub__(self, action):
		self.entities -= action
		return self

	def has_boat(self):
		return self.entities.has_boat()


class CandMState:
	def __init__(self, init_string = None, copy = None):
		if copy:
			self.left_bank = copy.left_bank
			self.right_bank = copy.right_bank
		else:
			(left, right) = init_string.strip().split('|')
			self.left_bank = BankState(left)
			self.right_bank = BankState(right)

	def __repr__(self):
		return "%s | %s" % (self.left_bank, self.right_bank)

	def __eq__(self, other):
		return self.left_bank == other.left_bank and self.right_bank == other.right_bank
	
	def __add__(self, action):
		result = CandMState(copy = self)
		(depart, arrive) = result.bank_roles()
		depart -= action
		arrive += action
		return result
	
	def bank_roles(self):
		if self.left_bank.has_boat():
			return (self.left_bank, self.right_bank)
		else:
			return (self.right_bank, self.left_bank)

	def get_successors(self):
		(depart, arrive) = self.bank_roles()
		return [(action, self+action) for action in Actions if arrive.arrival_action_valid(action) and depart.departure_action_valid(action)]

#def treeSearch(problem, strategy):
#	fringe = [ problem.initialState ]
#	while True:
#		if len(fringe) == 0:
#			return None
#		node = selectFrom(fringe, strategy)
#		if problem.goalTest(node):
#			return pathTo(node)
#		fringe.a

class SearchNode:
	known_states = []
	def __init__(self, parent, state, action):
		self.parent = parent
		self.state = state
		self.action = action
		SearchNode.known_states.append(state)

	def successors(self):
		successors = self.state.get_successors()
		viable_successors = [ s for s in successors if s[1] not in SearchNode.known_states ]
		return [SearchNode(self, state, action) for (action, state) in viable_successors ]

	def pathto(self):
		x = [self]
		next = self.parent
		while next:
			x.append(next)
			next = next.parent
		x.reverse()
		return x

class Problem:
	def __init__(self, initial_state, goal_state):
		self.initial = initial_state
		self.goal = goal_state
		self.known_states = [ initial_state ]
		self.fringe = [ SearchNode(parent = None, state = initial_state, action = None) ]

	def solve(self, strategy):
		while len(self.fringe) > 0:
			(node, fringe) = strategy(self.fringe)
			if node.state == self.goal:
				return node
			self.fringe = fringe + node.successors()
		return None

def breadth_first(fringe):
	return (fringe[0], fringe[1:])

def depth_first(fringe):
	return (fringe[-1], fringe[0:-1])

def main():
	problem = Problem(initial_state = CandMState('3M3CB|'),
					  goal_state = CandMState('|3M3CB'))
	
	node = problem.solve(breadth_first)
	if node:
		path = node.pathto()
		if len(path) == 1:
			print "Initial state is goal state"
		else:
			for p in path:
				print p.state
	else:
		print "No solution found"
	
if __name__ == "__main__":
	main()
