import random

from fighter import Fighter

class FightingAi:
    MOVE_TOWARDS_OPPONENT = 0
    MOVING_LEFT = 2
    MOVING_RIGHT = 3
    EVADE = 4
    ATTACK_OPPONENT = 1

    REACTION_TIME = 30 
    EVASION_TIME = 20

    PROB_KICK = .5
    PROB_EVADE = .2
    PROB_SWITCH_NO_REASON = .05

    PROB_FIREBALL = .1
    PROB_FIREBALL_SUCCESS = .05

    PROB_SWIFT_FEET = .1

    PROB_BLOCK = .25

    def __init__(self, game, fighter):
        self.fighter = fighter
        self.game = game
        self.opponent = self.game.opponent(self.fighter)
        self.state = self.MOVE_TOWARDS_OPPONENT
        self.reaction_time = -1
        self.evasion_frames = -1
        self.last_evade = 'left'
        self.opponent.injection_callbacks.append(self.opponent_changed_injection)
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
        self.mutation_counters = {
            'magicalaffinity': 'tranquility',
            'strength': 'hardenedskin',
            'toxic': 'tranquility',
            'swiftfeet': 'swiftfeet',
            'wings': 'swiftfeet',
        }
    
    def reset(self):
        self.reaction_time = -1
        self.evasion_frames = -1
    
    def opponent_changed_injection(self, old_injection, new_injection):
        if self.fighter.current_injection >= 2:
            return
        wanted = []
        for mut in self.opponent.injections[new_injection]:
            if mut == None:
                continue
            if self.mutation_counters.has_key(mut.name):
                wanted.append(self.mutation_counters[mut.name])
        wanted = [w for w in wanted if w not in self.fighter.injections[self.fighter.current_injection]]
        if any([w in self.fighter.injections[self.fighter.current_injection + 1] for w in wanted]):
            self.fighter.switch_to_injection(self.fighter.current_injection + 1)

    def distance_to_opponent(self):
        return self.opponent.rect.x - self.fighter.rect.x
    
    def update(self):
        #print self.state_names[self.state], self.distance_to_opponent()
        self.state_handlers[self.state]()
        self.evade_fireball()

        r = random.randint(0, 100)
        if r <= self.PROB_FIREBALL * 100 and 'magicalaffinity' in self.fighter.injection_names():
            r = random.randint(0, 100)
            if r <= self.PROB_FIREBALL_SUCCESS * 100:
                self.fighter.fireball()
            return

    def move_towards_opponent(self):
        dist = self.distance_to_opponent()
        r = random.randint(0, 100)
        if r <= self.PROB_SWITCH_NO_REASON * 100 and self.fighter.current_injection < 2:
            self.fighter.switch_to_injection(self.fighter.current_injection + 1)
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
    
    def apply_swift_feet(self):
    	if self.fighter.speed_multi <= 1 and 'swiftfeet' in self.fighter.mutation_names():
    		r = random.randint(0, 100)
    		if r <= self.PROB_SWIFT_FEET * 100:
    			self.fighter.simulate_key_sequence(['left', 'left'])
    
    def evade_fireball(self):
    	if not 'wings' in self.fighter.mutation_names():
    		return
    	if self.fighter.jump_count > 0 and self.fighter.jump_frame >= 4:
    		self.fighter.jump()
    	for f in self.game.fireballs:
    		if abs(f.pos[0] - self.fighter.rect.x) < 40:
    			self.fighter.jump()

    def moving_left(self):
        dist = self.distance_to_opponent()
        if abs(dist) < 20:
            print 'stop left (3)'
            self.fighter.stop_left()
            self.state = self.ATTACK_OPPONENT
            return
        self.apply_swift_feet()
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
        self.apply_swift_feet()
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
            if self.reaction_time == 0:
                self.state = self.MOVE_TOWARDS_OPPONENT
                self.reaction_time = -1
            elif self.reaction_time == -1:
                self.reaction_time = self.REACTION_TIME
            else:
                self.reaction_time -= 1
            return
        if self.opponent.kicking or self.opponent.punching:
        	r = random.randint(0, 100)
        	if r <= self.PROB_BLOCK * 100:
        		self.fighter.block()
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
        self.apply_swift_feet()
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
