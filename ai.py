import random

from fighter import Fighter

class FightingAi:
	# TODO: 
	# * When injections are implemented: the AI needs to know about them.

	MOVE_TOWARDS_OPPONENT = 0
	MOVING_LEFT = 2
	MOVING_RIGHT = 3
	EVADE = 4
	ATTACK_OPPONENT = 1

	REACTION_TIME = 15 
	EVASION_TIME = 20

	PROB_KICK = .5
	PROB_EVADE = .2

	def __init__(self, game, fighter):
		self.fighter = fighter
		self.game = game
		self.opponent = self.game.opponent(self.fighter)
		self.state = self.MOVE_TOWARDS_OPPONENT
		self.reaction_time = -1
		self.evasion_frames = -1
		self.last_evade = 'left'
		self.state_handlers = {
			self.MOVE_TOWARDS_OPPONENT: self.move_towards_opponent,
			self.ATTACK_OPPONENT: self.attack_opponent,
			self.MOVING_LEFT: self.moving_left,
			self.MOVING_RIGHT: self.moving_right,
			self.EVADE: self.evade
		}
		self.state_names = {
			self.MOVE_TOWARDS_OPPONENT: 'MOVE_TOWARDS_OPPONENT',
			self.ATTACK_OPPONENT: 'ATTACK_OPPONENT',
			self.MOVING_LEFT: 'MOVING_LEFT',
			self.MOVING_RIGHT: 'MOVING_RIGHT',
			self.EVADE: 'EVADE'
		}
	
	def reset(self):
		print 'reset'
		self.reaction_time = -1
		self.evasion_frames = -1

	def distance_to_opponent(self):
		return self.opponent.rect.x - self.fighter.rect.x
	
	def update(self):
		#print self.state_names[self.state], self.distance_to_opponent()
		self.state_handlers[self.state]()

	def move_towards_opponent(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			self.state = self.ATTACK_OPPONENT
			return
		if dist < 0:
			self.state = self.MOVING_LEFT
			print 'moving left (1)'
			self.fighter.left()
		else:
			self.state = self.MOVING_RIGHT
			print 'moving right (2)'
			self.fighter.right()
		if self.opponent.rect.y - self.fighter.rect.y < 20:
			self.fighter.jump()

	def moving_left(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			print 'stop left (3)'
			self.fighter.stop_left()
			self.state = self.ATTACK_OPPONENT
			return
		if dist > 0:
			if self.reaction_time == 0:
				print 'stop left (4)'
				self.fighter.stop_left()
				print 'move right (5)'
				self.fighter.right()
				self.state = self.MOVING_RIGHT
				self.reaction_time = -1
			elif self.reaction_time == -1:
				self.reaction_time = self.REACTION_TIME
			else:
				self.reaction_time -= 1

	def moving_right(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			print 'stop right (6)'
			self.fighter.stop_right()
			self.state = self.ATTACK_OPPONENT
			return
		if dist < 0:
			if self.reaction_time == 0:
				print 'stop right (7)'
				self.fighter.stop_right()
				print 'move left (8)'
				self.fighter.left()
				self.state = self.MOVING_LEFT
				self.reaction_time = -1
			elif self.reaction_time == -1:
				self.reaction_time = self.REACTION_TIME
			else:
				self.reaction_time -= 1
	
	def attack_opponent(self):
		dist = self.distance_to_opponent()
		if self.fighter.kicking or self.fighter.punching:
			return
		if abs(dist) > 20:
			self.state = self.MOVE_TOWARDS_OPPONENT
			return
		r = random.randint(0, 100)
		if r <= self.PROB_EVADE * 100:
			self.state = self.EVADE
			return
		r = random.randint(0, 100)
		if r <= self.PROB_KICK * 100:
			self.fighter.kick()
		else:
			self.fighter.punch()
	
	def evade(self):
		dist = self.distance_to_opponent()
		if self.evasion_frames == -1:
			if dist < 0:
				print 'move left (9)'
				self.fighter.left()
				self.last_evade = 'left'
			else:
				print 'move right (10)'
				self.fighter.right()
				self.last_evade = 'right'
			self.evasion_frames = 0
		elif self.evasion_frames == self.EVASION_TIME:
			self.state = self.MOVE_TOWARDS_OPPONENT
			self.evasion_frames = -1
			if self.last_evade == 'left':
				print 'stop left (11)'
				self.fighter.stop_left()
			else:
				print 'stop right (12)'
				self.fighter.stop_right()
		else:
			self.evasion_frames += 1