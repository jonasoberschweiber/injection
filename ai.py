from fighter import Fighter

class FightingAi:
	# TODO: 
	# * The AI is a little fast, give the player some space.
	# * Punching would be nice.
	# * When injections are implemented: the AI needs to know about them.

	MOVE_TOWARDS_OPPONENT = 0
	MOVING_LEFT = 2
	MOVING_RIGHT = 3
	ATTACK_OPPONENT = 1

	def __init__(self, game, fighter):
		self.fighter = fighter
		self.game = game
		self.opponent = self.game.opponent(self.fighter)
		self.state = self.MOVE_TOWARDS_OPPONENT
		self.state_handlers = {
			self.MOVE_TOWARDS_OPPONENT: self.move_towards_opponent,
			self.ATTACK_OPPONENT: self.attack_opponent,
			self.MOVING_LEFT: self.moving_left,
			self.MOVING_RIGHT: self.moving_right
		}
		self.state_names = {
			self.MOVE_TOWARDS_OPPONENT: 'MOVE_TOWARDS_OPPONENT',
			self.ATTACK_OPPONENT: 'ATTACK_OPPONENT',
			self.MOVING_LEFT: 'MOVING_LEFT',
			self.MOVING_RIGHT: 'MOVING_RIGHT'
		}

	def distance_to_opponent(self):
		return self.opponent.rect.x - self.fighter.rect.x
	
	def update(self):
		print self.state_names[self.state], self.distance_to_opponent()
		self.state_handlers[self.state]()

	def move_towards_opponent(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			self.state = self.ATTACK_OPPONENT
			return
		if dist < 0:
			self.state = self.MOVING_LEFT
			self.fighter.left()
		else:
			self.state = self.MOVING_RIGHT
			self.fighter.right()
		if self.opponent.rect.y - self.fighter.rect.y < 20:
			self.fighter.jump()

	def moving_left(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			self.fighter.stop_left()
			self.state = self.ATTACK_OPPONENT
		if dist > 0:
			self.fighter.stop_left()
			self.fighter.right()
			self.state = self.MOVING_RIGHT

	def moving_right(self):
		dist = self.distance_to_opponent()
		if abs(dist) < 20:
			self.fighter.stop_right()
			self.state = self.ATTACK_OPPONENT
		if dist < 0:
			self.fighter.stop_right()
			self.fighter.left()
			self.state = self.MOVING_LEFT
	
	def attack_opponent(self):
		dist = self.distance_to_opponent()
		if abs(dist) > 20:
			self.state = self.MOVE_TOWARDS_OPPONENT
			return
		if self.fighter.kicking or self.fighter.punching:
			return
		self.fighter.kick()
