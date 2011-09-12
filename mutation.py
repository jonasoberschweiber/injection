import pygame

class Mutation:
	def activated(self, fighter):
		pass

	def deactivated(self, fighter):
		pass

class FiftyPercentMoreSpeedMutation(Mutation):
	def activated(self, fighter):
		fighter.speed_multi = 1.5
	
	def deactived(self, fighter):
		fighter.speed_multi = 1