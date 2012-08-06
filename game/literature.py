import random
import collections

#Handle problems

class LiteratureError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

#Game as an object		
		
class Game(object):
	#Initialize card suits and values
	#Initialize sets and values
	
	def CARDS(self):
		return ['SA', 'DA', 'HA', 'CA', 'S2', 'D2', 'H2', 'C2', 'S3', 'D3', 'H3', 'C3', 'S4', 
			'D4', 'H4', 'C4', 'S5', 'D5', 'H5', 'C5', 'S6', 'D6', 'H6', 'C6', 'S7', 'D7',\
			'H7', 'C7', 'S8', 'D8', 'H8', 'C8', 'S9', 'D9', 'H9', 'C9', 'S10', 'D10', 'H10',\
			'C10', 'SJ', 'DJ', 'HJ', 'CJ', 'SQ', 'DQ', 'HQ', 'CQ', 'SK', 'DK', 'HK', 'CK']
			
	def SETS(self):
		return [['S10', 'S7', 'S8', 'S9', 'SJ', 'SK', 'SQ'], ['D10', 'D7', 'D8', 'D9', 'DJ', 'DK',\
			'DQ'], ['H10', 'H7', 'H8', 'H9', 'HJ', 'HK', 'HQ'], ['C10', 'C7', 'C8', 'C9', 'CJ',\
			'CK', 'CQ'], ['S2', 'S3', 'S4', 'S5', 'S6', 'SA'], ['D2', 'D3', 'D4', 'D5', 'D6',\
			'DA'], ['H2', 'H3', 'H4', 'H5', 'H6', 'HA'], ['C2', 'C3', 'C4', 'C5', 'C6', 'CA']]
	
	#Construct Game with new deck
	
	def __init__(self, limit):
		self.state = 'Created'
		self.deck = self.CARDS()
		self.parts = self.SETS()
		self.players = []
		self.captures = [[],[]]
		self.count = 6
		self.limit = limit
		
	#Add Player to Game	
		
	def add(self, player):
		if isinstance(player, Player) == False:
			raise LiteratureError('Only players may be added to a game.')
			
		if len(self.players) >= self.count:
			raise LiteratureError('The player count has been exceeded.')
		
		team = 'A' if len(self.players) % 2 == 0 else 'B'
		spot = len(self.players) + 1
		
		self.players.append(player)
		self.players[len(self.players)-1].sit(team, spot)
		self.players[len(self.players)-1].push(self)

		return True
	
	#Start game by dealing cards
	
	def deal(self):
		self.state = 'Dealing'
		while len(self.deck) > 0:
			for player in self.players:
				if len(self.deck) > 0:
					selection = random.randint(0, len(self.deck)-1)
					player.get(self.deck[selection])
					del self.deck[selection]
		return True
	
	#Get the base of a card
		
	def base(self, card):
		set = card[0]
		if card[1] == 'A' or (card[1] not in 'JQK' and int(card[1:]) < 7):
			return set + 'm'
		else:
			return set + 'M'	
		
	#Run the game in a loop
	
	def run(self):
		self.state = 'Running'
		self.deal()
		self.lastPlayer = random.randint(0,len(self.players)-1)
		self.turn = 1
		self.currentPlayer = 0
		
		while len(self.deck) < 52:
			if (len(self.players[self.currentPlayer].show()) > 0):
				#for i in self.players:
				#	print(i.show())
				#print('')
				
				#print(self.turn)
				self.turn = self.turn + 1
				
				if self.turn > self.limit:
					self.end()
					return True
				
				if self.number(1) + self.number(3) + self.number(5) == 0:
					last = self.players[1].show() + self.players[3].show() + self.players[5].show()
					types = []
					
					for card in last:
						if self.base(card) not in types:
							types.append(self.base(card))
							
					for type in types:
						for part in self.parts:
							if type == self.base(part[0]):
								if type not in self.captures[1]:
									self.captures[1].append(type)
								
					break
					
				elif self.number(2) + self.number(4) + self.number(6) == 0:
					last = self.players[0].show() + self.players[2].show() + self.players[4].show()
					types = []
					
					for card in last:
						if self.base(card) not in types:
							types.append(self.base(card))
							
					for type in types:
						for part in self.parts:
							if type == self.base(part[0]):
								if type not in self.captures[0]:
									self.captures[0].append(type)
									
					break
				
				self.played = False
				self.players[self.currentPlayer].move()
				#pause = input('')
			
		self.end()
		return True
	
	#Allow knowledge of the number of an opponent's cards
	
	def number(self, player):
		if 1 <= player <= 6:
			return len(self.players[int(player) - 1].show())
		return False
		
	#Allow players to get the game score as list of captures
	
	def score(self):
		return self.captures
	
	#Check if player has card
	
	def has(self, player, card):
		if card in self.players[player].show():
			return True
		return False

	#Check player basis for a card
	
	def basis(self, player, card):
		for item in self.SETS():
			if card in item:
				base = item
				break
		
		for item in self.players[player].show():
			if item in base:
				return True
		
		return False
		
	#Fetch cards after a call

	def fetch(self, set):
		for player in self.players:
			player.lose(set)
		return True
	
	#Allow players to ask for cards in turns
	
	def ask(self, asked, card):
		#print('Memory Before: ' + str(self.players[self.currentPlayer].memory) + '\n')
		if len(str(asked)) > 1 or str(asked) not in '123456':
			raise LiteratureError('A valid player must be asked.')
		
		asked = int(asked) - 1
			
		if self.currentPlayer % 2 == asked % 2:
			raise LiteratureError('A member of the same team as a player was asked for a card.')
		
		if card not in self.CARDS():
			raise LiteratureError('An illegitimate card was asked for.')
		
		if self.basis(self.currentPlayer, card) == False or self.has(self.currentPlayer, card) == True:
			raise LiteratureError('A deceptive move was made: player has no basis or has card.')
			
		if self.played == True:
			raise LiteratureError('Multiple asks were erroneously made in the same turn.')
			
		move = ['ask', self.currentPlayer + 1, asked + 1, card]
		#print(move)
		out = self.currentPlayer
		
		if self.number(asked + 1) == 0:
			raise LiteratureError('A player without cards was asked for a card.')
		
		if self.has(asked, card):
			self.players[asked].give(card)
			self.players[self.currentPlayer].get(card)
			move.append(True)
		
		else:
			self.lastPlayer = self.currentPlayer
			self.currentPlayer = asked
			move.append(False)
		
		for player in range(len(self.players)):
			if (self.number(player + 1) > 0):
				self.players[player].process(move)
		
		#print('Focus: ' + str(self.players[out].focus))
		#print('Action: ' + str(move) + '\n')
		#print('Memory After: ' + str(self.players[out].memory) + '\n\n')
		self.played = True
		
	#Allow players to call in their turns
	#First, second, and third should correspond to P1, P3, P5 or P2, P4, P6

	def call(self, first, second, third):
		#print('Memory Before: ' + str(self.players[self.currentPlayer].memory) + '\n')
		#print(first, second, third)
		
		if self.played == True:
			raise LiteratureError('Multiple calls were erroneously made in the same turn.')
			
		#print(self.currentPlayer)
		
		if (self.currentPlayer % 2 == 0):
			firstPlayer = 0
			secondPlayer = 2
			thirdPlayer = 4
		else:
			firstPlayer = 1
			secondPlayer = 3
			thirdPlayer = 5
		
		problem = False
		called = []
			
		for card in first:
			if card in self.CARDS():
				if self.has(firstPlayer, card) == False:
					problem = True
				called.append(card)
			else:
				raise LiteratureError('An illegitimate card was called for.')
				
		for card in second:
			if card in self.CARDS():
				if self.has(secondPlayer, card) == False:
					problem = True
				called.append(card)
			else:
				raise LiteratureError('An illegitimate card was called for.')
		
		for card in third:
			if card in self.CARDS():
				if self.has(thirdPlayer, card) == False:
					problem = True
				called.append(card)
			else:
				raise LiteratureError('An illegitimate card was called for.')
				
		called = sorted(called)
		out = self.currentPlayer
		
		if called not in self.parts:
			raise LiteratureError('An invalid set was called.')
		
		if problem == True:
			self.parts.remove(called)
			self.deck = self.deck + called
			
			if out % 2 == 0:
				self.captures[1].append(called)
			else:
				self.captures[0].append(called)

			if self.number(self.lastPlayer + 1) == 0:
				self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0])
				
			self.currentPlayer = self.lastPlayer
			next = [player for player in range(len(self.players)) if self.number(player + 1) != 0 if player != self.currentPlayer]
				
			if len(next) > 0:
				self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0 if player != self.currentPlayer])
			
			else:
				self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0])					
		
			self.fetch(called)

		else:
			self.parts.remove(called)
			self.deck = self.deck + called
			
			if out % 2 == 0:
				self.captures[0].append(called)
			else:
				self.captures[1].append(called)
			
			self.fetch(called)
			
			if self.number(self.lastPlayer + 1) == 0:
				self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0])
				
			if self.number(self.currentPlayer + 1) == 0:
				self.currentPlayer = self.lastPlayer
				next = [player for player in range(len(self.players)) if self.number(player + 1) != 0 if player != self.currentPlayer]
				
				if len(next) > 0:
					self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0 if player != self.currentPlayer])
				
				else:
					self.lastPlayer = random.choice([player for player in range(len(self.players)) if self.number(player + 1) != 0])					
		
		move = ['call', out + 1, first, second, third]

		for player in range(len(self.players)):
			if (self.number(player + 1) > 0):
				self.players[player].process(move)
		
		#print('Action: ' + str(move))
		#print('Score: ' + str(len(self.captures[0])) + ':' + str(len(self.captures[1])) + '\n')
		#input('')
		#print('Memory After: ' + str(self.players[out].memory) + '\n\n')
		self.played = True
	
	#Get game state
		
	def state(self):
		return self.state
	
	#End the game
	
	def end(self):
		self.state = 'Finished'
		if self.turn <= self.limit:
			self.score = str(len(self.captures[0])) + ':' + str(len(self.captures[1]))
			print('After ' + str(self.turn) + ' turns, the final score is: ' + str(len(self.captures[0])) + ':' + str(len(self.captures[1])) + '.')
		else:
			self.score = '0:0'
			print('Error after ' + str(self.limit) + ' turn limit was exceeded.')
		return True
	
#Abstract player as an object		
		
class Player(object):
	#Construct player object
	#Unknown hand, team, and number
	
	def __init__(self, max):
		self.hand = []
		self.memory = []
		self.team = ''
		self.limit = max
		self.free = max
		self.number = 0
	
	#Process function to be implemented
	
	def process(self, move):
		raise LiteratureError('The process subroutine has not been implemented for a player.')
	
	#Move function to be implemented
	#Format: P1 ? P2 S6
	#Format: P1 ! P1 S5 P3 SA,S2,S3 P5 S4,S6
	
	def move(self):
		raise LiteratureError('The move subroutine has not been implemented for a player.')
	
	#Sit down for a particular team
	#Be assigned a player number
	
	def sit(self, side, position):
		self.team = side
		self.number = position
		return True
	
	#Receive dealt cards
		
	def get(self, card):
		self.hand.append(card)
		return True
		
	#Give cards when asked
	#Actually just delete it
	
	def give(self, card):
		self.hand.remove(card)
		return True
		
	#Lose multiple cards from set
	#Occurs after a call
	
	def lose(self, set):
		for card in set:
			if card in self.hand:
				self.hand.remove(card)
		return True

	#Get pushed on to a particular game
	
	def push(self, game):
		self.game = game
		return True
		
	#Allow game to access hand
	
	def show(self):
		return self.hand
	
#Sample player using a simple "active" strategy
	
class ActivePlayer(Player):
	def SETS(self):
		return {'SM': ['S10', 'S7', 'S8', 'S9', 'SJ', 'SK', 'SQ'], 'DM': ['D10', 'D7', 'D8', 'D9', 'DJ', 'DK',\
			'DQ'], 'HM': ['H10', 'H7', 'H8', 'H9', 'HJ', 'HK', 'HQ'], 'CM': ['C10', 'C7', 'C8', 'C9', 'CJ',\
			'CK', 'CQ'], 'Sm': ['S2', 'S3', 'S4', 'S5', 'S6', 'SA'], 'Dm': ['D2', 'D3', 'D4', 'D5', 'D6',\
			'DA'], 'Hm': ['H2', 'H3', 'H4', 'H5', 'H6', 'HA'], 'Cm': ['C2', 'C3', 'C4', 'C5', 'C6', 'CA']}
	
	def __init__(self, max):
		super().__init__(max)
		self.focus = ''
		self.memory = []
		
	def base(self, card):
		set = card[0]
		if card[1] == 'A' or (card[1] not in 'JQK' and int(card[1:]) < 7):
			return set + 'm'
		else:
			return set + 'M'
	
	def spotlight(self, second = False):
		bases = []
		
		for card in self.hand:
			bases.append(self.base(card))
			bases.append(self.base(card))
		
		for item in self.memory:
			if item[0] == 'Card' or item[0] == '~Card':
				if self.base(item[2]) in bases:
					bases.append(self.base(item[2]))
					bases.append(self.base(item[2]))
			
			elif item[0] == 'Base' or item[0] == '~Base':
				if item[2] in bases:
					bases.append(item[2])
		
		self.focus = max(set(bases), key = bases.count)
		return True
	
	def move(self):
		help = random.randint(0,9)
	
		if help <= 2:
			bases = []
			
			for card in self.hand:
				if self.base(card) not in bases:
					bases.append(self.base(card))
					
			self.focus = max(set(bases), key = bases.count)
			found = False
			
			while found == False:
				base = random.choice(bases)
				need = []
			
				for card in self.SETS()[base]:
					if card not in self.hand:
						need.append(card)
				
				if len(need) > 0:
					found = True
				
				else:
					for card in self.SETS()[base]:
						if card in self.hand:
							need.append(card)
						
					if self.number == 1 or self.number == 2:
						self.game.call(need, [], [])
						return True
					
					elif self.number == 3 or self.number == 4:
						self.game.call([], need, [])
						return True
					
					else:
						self.game.call([], [], need)
						return True
					
			opponents = [2,4,6] if self.team == 'A' else [1,3,5]
			opponents = [person for person in opponents if self.game.number(person) > 0]
			
			self.game.ask(random.choice(opponents), random.choice(need))
			return True
	
		self.spotlight()
		locations = {}
		
		for card in self.SETS()[self.focus]:
			if card in self.hand:
				locations[card] = self.number
			else:
				locations[card] = False
		
		for item in self.memory:
			if item[0] == 'Card' and item[1] % 2 == self.number % 2 and self.base(item[2]) == self.focus:
				locations[item[2]] = item[1] 
		
		for item in self.memory:
			if item[0] == 'Card' and self.base(item[2]) == self.focus and item[1] % 2 != self.number % 2:
				self.game.ask(item[1], item[2])
				if item in self.memory:
					self.memory.remove(item)
				return True
				
		for item in self.memory:
			if item[0] == 'Card' and item[1] % 2 != self.number % 2:
				self.game.ask(item[1], item[2])
				if item in self.memory:
					self.memory.remove(item)
				return True
		
		permutations = []
		#print(locations)
		
		for key, value in locations.items():
			if value == False:
				opponents = [2,4,6] if self.team == 'A' else [1,3,5]
				for opponent in opponents:
					if ['~Card', opponent, key] not in self.memory and ['~Base', opponent, key] not in self.memory:
						permutations.append([opponent, key])
		
		if len(permutations) > 0:
			selection = random.choice(permutations)
			checks = len(permutations)
			
			while self.game.number(selection[0]) == 0 and checks > 0:
				selection = random.choice(permutations)
				checks = checks - 1
			
			if checks > 0:
				self.game.ask(selection[0], selection[1])
			
			else:
				permutations = []

				for key, value in locations.items():
					if value == False:
						opponents = [2,4,6] if self.team == 'A' else [1,3,5]
						for opponent in opponents:
							if self.game.number(opponent) > 0:
								permutations.append([opponent, key])	

				selection = random.choice(permutations)
				self.game.ask(selection[0], selection[1])
			
			return True
			
		else:
			consist = locations
			team = [1,3,5] if self.team == 'A' else [2,4,6]
			team.remove(self.number)
			
			for person in team:
				if self.game.number(person) == 0:
					for key, value in consist.items():
						if value == False and self.base(key) == self.focus:
							consist[key] = '~' + str(person)
							
			for item in self.memory:
				if item[0] == '~Card' and item[1] in team and self.base(item[2]) == self.focus:
					if consist[item[2]] == False:
						consist[item[2]] = '~' + str(item[1])
				if item[0] == '~Base' and item[1] in team and item[2] == self.focus:
					for key, value in consist.items():
						if value == False and self.base(key) == item[2] and item[2] == self.focus:
							consist[key] = '~' + item[1]
			
			for key, value in consist.items():
				if value == False:
					consist[key] = random.choice(team)
				elif str(value)[0] == '~':
					if int(value[1:]) == team[0]:
						consist[key] = team[1]
					else:
						consist[key] = team[0]
		
			first = []
			second = []
			third = []
			
			if self.team == 'A':
				for key, value in consist.items():
					if value == 1: first.append(key)
					elif value == 3: second.append(key)
					elif value == 5: third.append(key)
					
			elif self.team == 'B':
				for key, value in consist.items():
					if value == 2: first.append(key)
					elif value == 4: second.append(key)
					elif value == 6: third.append(key)
				
			self.game.call(first, second, third)
			return True
						
		return True
		
	def process(self, move):
		self.spotlight()
		type = move[0]
		
		if type == 'call':
			return True
		
		elif type == 'ask':
			info = []

			player = move[1]
			askee = move[2]
			card = move[3]
			success = move[4]

			if player != self.number:
				info.append(['Basis', player, self.base(card)])

			if success == True:
				if player != self.number:
					info.append(['Card', player, card])
				if player != self.number and askee != self.number:
					info.append(['~Card', askee, card])
	
			else:
				if player != self.number and card not in self.hand:
					info.append(['~Card', player, card])
				if askee != self.number and card not in self.hand:
					info.append(['~Card', askee, card])
					
			total = []
			order = [[],[],[],[]]
			bases = []
			
			for item in info:
				total.append(item)
			
			for item in self.memory:
				go = False
				for thing in total:
					if (thing[0] == '~' + item[0] or '~' + thing[0] == item[0]) and item[1] == thing[1] and item[2] == thing[2]:
						go = True
						break
				
				if item[0] == 'Card' and item[2] in self.hand:
					go = True
				
				if go == False:
					total.append(item)		
			
			total = [list(i) for i in set(tuple(i) for i in total)]
			
			for thing in self.hand:
				if self.base(thing) not in bases:
					bases.append(self.base(thing))
			
			for item in total:
				if item[0] == 'Card' and self.base(item[2]) in bases:
					if self.base(item[2]) == self.focus:
						order[0].insert(0, item)
					else:
						order[1].append(item)
				
				if item[0] == 'Base' and item[2] in bases:
					if item[2] == self.focus:
						order[0].append(item)
					else:
						order[2].insert(0, item)
						
				
				if item[0] == '~Card' and self.base(item[2]) in bases:
					if self.base(item[2]) == self.focus:
						order[1].insert(0, item)
					else:
						order[2].append(item)
				
				if item[0] == '~Base' and item[2] in bases:
					if item[2] == self.focus:
						order[3].insert(0, item)
					else:
						order[3].append(item)

			order = order[0] + order[1] + order[2] + order[3]
			order.reverse()
			
			self.memory = []
			self.free = self.limit
			
			while self.free > 0 and len(order) > 0:
				if order[len(order)-1][0] == 'Card' or order[len(order)-1][0] == '~Card' and self.free > 1:
					self.free = self.free - 2
					self.memory.append(order[len(order)-1])
					del order[len(order)-1]
					continue
					
				elif order[len(order)-1][0] == 'Base' or order[len(order)-1][0] == '~Base':
					self.free = self.free - 1
					self.memory.append(order[len(order)-1])
					del order[len(order)-1]
					continue
					
				self.free = self.free - 1
					
			return True
	
if __name__ == '__main__':
	scores = []
	turns = []
	botched = []
	
	#Change the following parameters for settings
	#They include runs, bound, start, and end
	
	runs = 100 #Number of Iterations Per Memory Level
	bound = 600 #Cut-off Number of Turns (When a Botch is Declared)
	start = 30 #Start At This Memory Level
	end = 31 #End BEFORE This Memory Level
	
	#Instantiate six players with thirty memory slots
	#Add them to the example game
	#Run fifty instances for testing
	
	#Thirty seems to be a good number for this to work
	#Too few memory slots otherwise, and the game stalls
	#Hopefully I can make this probabilistic though
	
	for memory in range(start,end):
		print('Memory level ' + str(memory) + ' is beginning.')
		
		scores.append([])
		turns.append([])
		botched.append(0)
		
		for run in range(runs):	
			testGame = Game(bound)
			people = []
			
			for i in range(6):
				people.append(ActivePlayer(memory))
				testGame.add(people[len(people)-1])
				
			testGame.run()
			
			if testGame.score != '0:0':
				scores[memory-start].append(testGame.score)
				turns[memory-start].append(testGame.turn)
			
			else:
				botched[memory-start] = botched[memory-start] + 1
	
		histogram = {x: scores[memory-start].count(x) for x in set(scores[memory-start])}
		display = ''
		
		for key in ['4:4','3:5','5:3','2:6','6:2','1:7','7:1','0:8','8:0']:
			if key in histogram:
				display = display + str(key) + ' - ' + str(histogram[key]) + ', '
				
		print('\nFinal: ' + display[:-2])
		
		if len(scores[memory-start]) > 0:
			print('Botched Trials: ' + str(botched[memory-start]) + '. Botched Percentage: ' + str(int(100*botched[memory-start]/runs)) + '%. Average Count: ' + str(int(sum(turns[memory-start])/len(turns[memory-start]))) + '.')
		
		else:
			print('Botched Trials: ' + str(botched[memory-start]) + '. Botched Percentage: ' + str(int(100*botched[memory-start]/runs)) + '%. Average Count: ' + str(bound) + '.\n')
		
	pause = input('')