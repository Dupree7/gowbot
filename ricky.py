import time, pyautogui, numpy, random

cast_location = (968, 955) # add it to spells

class move():
	def __init__(self, name, color, color_count, from_x, from_y, to_x, to_y, extra_turn):
		self.name = name
		self.color = color
		self.color_count = color_count
		self.from_x = from_x
		self.from_y = from_y
		self.to_x = to_x
		self.to_y = to_y
		self.extra_turn = extra_turn
	def __str__(self):
		return "{0} of {1} ({2}, {3}) -> ({4}, {5}) with extra_turn = {6}".format(self.color_count, self.name, self.from_x + 1, self.from_y + 1, self.to_x + 1, self.to_y + 1, self.extra_turn)
	def __eq__(self, obj):
		return self.extra_turn == obj.extra_turn
	def __lt__(self, obj):
		if(self.extra_turn == obj.extra_turn): # TODO: better logic
			if(self.color == (2 << 6) or self.color == (2 << 2) or self.color == (2 << 1)):
				return True
		return self.extra_turn > obj.extra_turn

class tableManager():
	def __init__(self):
		self.matrix = [[0 for line in range(8)] for j in range(8)]
		self.moves = []
		self.lines_height = [93, 212, 331, 450, 569, 688, 807, 926]
		self.column_width = [543, 662, 781, 900, 1019, 1138, 1257, 1376]
		self.blue = [35, 189, 214]
		self.brown = [184, 147, 132]
		self.green = [136, 211, 53]
		self.purple = [165, 35, 214]
		self.red = [234, 51, 84]
		self.yellow = [250, 224, 115]
		self.visited = [[False for line in range(8)] for j in range(8)]
		self.padding_left = 485 #TODO: two arrays with (x, y) of squares center
		self.padding_top = 80
		self.square_length = 119
		
	def __str__(self):
		strMatrix = ""
		for line in range(0, 8):
			for column in range(0, 8):
				strMatrix = strMatrix + self.colorToString(self.matrix[line][column]) + " "
			strMatrix = strMatrix + "\n"
		return strMatrix
				
	def around(self, color, rgb):
		return ((color[0] - 5 <= rgb[0] and rgb[0] <= color[0] + 5) and
			(color[1] - 5 <= rgb[1] and rgb[1] <= color[1] + 5) and
				(color[2] - 5 <= rgb[2] and rgb[2] <= color[2] + 5)) 

	def bfs(self, line, column, color_1, color_2):
		if(line < 0 or line > 7 or column < 0 or column > 7):
			return 0
		if(not (self.matrix[line][column] & color_1 & color_2)):
			return 0
		if(self.visited[line][column]):
			return 0

		ans = 1
		self.visited[line][column] = True
		ans = ans + self.bfs(line + 1, column, color_1, color_2)
		ans = ans + self.bfs(line - 1, column, color_1, color_2)
		ans = ans + self.bfs(line, column + 1, color_1, color_2)
		ans = ans + self/bfs(line, column - 1, color_1, color_2)
		self.visited[line][column] = False
		return ans

	def createMatrix(self):
		ss = pyautogui.screenshot()
		pixels = numpy.array(ss)

		for line in range(0, 8):
			for column in range(0, 8):
				self.matrix[line][column] = self.getPixelColor(pixels[self.lines_height[line]][self.column_width[column]])
	
	def colorToString(self, color):
		if(color & (2 << 0)):
			return "blue"
		elif(color & (2 << 1)):
			return "brown"
		elif(color & (2 << 2)):
			return "green"
		elif(color & (2 << 3)):
			return "purple"
		elif(color & (2 << 4)):
			return "red"
		elif(color & (2 << 5)):
			return "yellow"
		return "skull"

	def countColor(self, line, column):
		horizontal = 1
		vertical = 1

		x = self.matrix[line][column]
		temp_l = line - 1
		while(temp_l > - 1):
			if(self.matrix[temp_l][column] == x):
				vertical = vertical + 1
				temp_l = temp_l - 1
			else:
				break
		temp_l = line + 1
		while(temp_l < 8):
			if(self.matrix[temp_l][column] == x):
				vertical = vertical + 1
				temp_l = temp_l + 1
			else:
				break

		temp_c = column - 1
		while(temp_c > -1):
			if(self.matrix[line][temp_c] == x):
				horizontal = horizontal + 1
				temp_c = temp_c - 1
			else:
				break
		temp_c = column + 1
		while(temp_c < 8):
			if(self.matrix[line][temp_c] == x):
				horizontal = horizontal + 1
				temp_c = temp_c + 1
			else:
				break
		if(horizontal == 3 and vertical == 3): #in convert/create gems a + form will not give extra turn
			return horizontal + vertical - 1, 1
		if(horizontal > 3):
			return horizontal, 1
		if(vertical > 3):
			return vertical, 1
		return max(horizontal, vertical), 0

	def dragTo(self, x, y):
		pyautogui.dragTo(x, y, duration=random.uniform(0.2, 0.5))

	def findAllMoves(self):
		for line in range(8):
			for column in range(7): #left to right
				move_a, move_b = self.getMoveToRight(line, column)
				if move_a.color_count > 2:
					self.moves.append(move_a)
				if move_b.color_count > 2:
					self.moves.append(move_b)

		for line in range(7):
			for column in range(8):
				move_a, move_b = self.getMoveToBottom(line, column)
				if move_a.color_count > 2:
					self.moves.append(move_a)
				if move_b.color_count > 2:
					self.moves.append(move_b)

		self.moves.sort()
		#for move in self.moves:
			#print(move)

	def getMoveToBottom(self, line, column):
		assert (line >= 0 and line < 8 and column >= 0 and column < 8)
		temp = self.matrix[line][column]
		self.matrix[line][column] = self.matrix[line + 1][column]
		self.matrix[line + 1][column] = temp

		move_a_count, move_a_extra_turn = self.countColor(line, column) 
		move_a = move(self.colorToString(self.matrix[line][column]), self.matrix[line][column], move_a_count, line, column, line + 1, column, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.countColor(line + 1, column) 
		move_b = move(self.colorToString(self.matrix[line + 1][column]), self.matrix[line][column], move_b_count, line + 1, column, line, column, move_b_extra_turn)

		temp = self.matrix[line][column]
		self.matrix[line][column] = self.matrix[line + 1][column]
		self.matrix[line + 1][column] = temp

		return move_a, move_b

	def getMoveToRight(self, line, column):
		assert (line >= 0 and line < 8 and column >= 0 and column < 8)
		temp = self.matrix[line][column + 1]
		self.matrix[line][column + 1] = self.matrix[line][column]
		self.matrix[line][column] = temp

		move_a_count, move_a_extra_turn = self.countColor(line, column) 
		move_a = move(self.colorToString(self.matrix[line][column]), self.matrix[line][column], move_a_count, line, column, line, column + 1, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.countColor(line, column + 1) 
		move_b = move(self.colorToString(self.matrix[line][column + 1]), self.matrix[line][column], move_b_count, line, column + 1, line, column, move_b_extra_turn)

		temp = self.matrix[line][column + 1]
		self.matrix[line][column + 1] = self.matrix[line][column]
		self.matrix[line][column] = temp

		return move_a, move_b

	def getPixelColor(self, pixel):
		if(self.around(self.blue, pixel)):
			return 2 << 0 # blue
		if(self.around(self.brown, pixel)):
			return 2 << 1 # brown
		if(self.around(self.green, pixel)):
			return 2 << 2 # green
		if(self.around(self.purple, pixel)):
			return 2 << 3 # purple
		if(self.around(self.red, pixel)):
			return 2 << 4 # red
		if(self.around(self.yellow, pixel)):
			return 2 << 5 # yellow
		return 2 << 6 # skulls
	
	def getPixelsAt(self, line, column):
		x = self.padding_left + column * self.square_length + self.square_length / 2 + random.randint(-40, 40)
		y = self.padding_top + line * self.square_length + self.square_length / 2 + random.randint(-40, 40)
		return x, y

	def interchange(self, from_l, from_c, to_l, to_c):
		x,y = self.getPixelsAt(from_l, from_c)
		to_x, to_y = self.getPixelsAt(to_l, to_c)
		self.moveTo(x, y)
		self.dragTo(to_x, to_y)

	def moveTo(self, x, y, max_duration = 0.5):
		pyautogui.moveTo(x, y, duration=random.uniform(0.2, max_duration))

	def twoColorsExtraTurn(self, color_1, color_2):
		for line in range(8):
			for column in range(8):
				if(self.bfs(line, column, color_1, color_2) > 4):
					return True
		return False
	def makeMove(self):
		self.interchange(self.moves[0].from_x, self.moves[0].from_y, self.moves[0].to_x, self.moves[0].to_y)
		self.moves.clear()
		time.sleep(random.uniform(0.1, 0.2))

class spellManager():
	def __init__(self):
		self.spell_check_pixel = [19, 227, 246]

	def getSpellsStatus(self):
		ss = pyautogui.screenshot()
		pixels = numpy.array(ss)

		ok1 = (pixels[75][169][0] == self.spell_check_pixel[0] and pixels[75][169][1] == self.spell_check_pixel[1] and pixels[75][169][2] == self.spell_check_pixel[2])
		ok2 = (pixels[330][169][0] == self.spell_check_pixel[0] and pixels[330][169][1] == self.spell_check_pixel[1] and pixels[330][169][2] == self.spell_check_pixel[2])
		ok3 = (pixels[585][169][0] == self.spell_check_pixel[0] and pixels[585][169][1] == self.spell_check_pixel[1] and pixels[585][169][2] == self.spell_check_pixel[2])
		ok4 = (pixels[840][169][0] == self.spell_check_pixel[0] and pixels[840][169][1] == self.spell_check_pixel[1] and pixels[840][169][2] == self.spell_check_pixel[2])

		return ok1, ok2, ok3, ok4

	def moveTo(self, x, y, max_duration = 0.5):
		pyautogui.moveTo(x, y, duration=random.uniform(0.2, max_duration))

	def useSpell(self, index):
		has_target = False
		if(index == 1):
			first_spell_location = (190, 320)
			self.moveTo(first_spell_location[1] + random.randint(-120, 120), first_spell_location[0] + random.randint(-80, 80), 0.3)
			pyautogui.click()
		elif(index == 2):
			second_spell_location = (450, 320)
			self.moveTo(second_spell_location[1] + random.randint(-120, 120), second_spell_location[0] + random.randint(-80, 80), 0.3)
			pyautogui.click()
		elif(index == 3):
			has_target = True
			third_spell_location = (700, 320)
			self.moveTo(third_spell_location[1] + random.randint(-120, 120), third_spell_location[0] + random.randint(-80, 80), 0.3); #has target
			pyautogui.click();
		else:
			has_target = True
			forth_spell_location = (940, 320)
			self.moveTo(forth_spell_location[1] + random.randint(-120, 120), forth_spell_location[0] + random.randint(-80, 80), 0.3); #has target
			pyautogui.click();

		self.moveTo(cast_location[1] + random.randint(-150, 150), cast_location[0] + random.randint(-40, 40), 0.3)
		pyautogui.click()

		if(has_target == True): 
			first_enemy_location = (190, 1600)
			self.moveTo(first_enemy_location[1] + random.randint(-100, 100), first_enemy_location[0] + random.randint(-70, 70), 0.25)
			pyautogui.doubleClick(interval = random.uniform(0.05, 0.1))
			second_enemy_location = (450, 1600)
			self.moveTo(second_enemy_location[1] + random.randint(-100, 100), second_enemy_location[0] + random.randint(-70, 70), 0.25)
			pyautogui.doubleClick(interval = random.uniform(0.05, 0.1))
			third_enemy_location = (700, 1600)
			self.moveTo(third_enemy_location[1] + random.randint(-100, 100), third_enemy_location[0] + random.randint(-70, 70), 0.25)
			pyautogui.doubleClick(interval = random.uniform(0.05, 0.1))
			forth_enemy_location = (950, 1600)
			self.moveTo(forth_enemy_location[1] + random.randint(-100, 100), forth_enemy_location[0] + random.randint(-70, 70), 0.25)
			pyautogui.doubleClick(interval = random.uniform(0.05, 0.1))
			pyautogui.click()
			time.sleep(0.1)

class envManager():
	def __init__(self):
		self.middle_enemy = (960, 550)
		self.start_fight = (980, 1015)
		self.hero_mvp = (948, 973)

	def battleGoing(self):
		ok = self.isMyTurn(True)
		if(ok):
			time.sleep(1)
			ok = ok | self.isMyTurn(True)
		return ok

	def enterBattle(self):
		self.moveTo(self.middle_enemy[0] + random.randint(-130, 130), self.middle_enemy[1] + random.randint(-200, 200))
		pyautogui.click()
		time.sleep(0.15)

		self.moveTo(self.start_fight[0] + random.randint(-500, 500), self.start_fight[1] + random.randint(-25, 25))
		pyautogui.click()
		time.sleep(8)

	def enterPvpScreen(self):
		time.sleep(5) # changeable
		skip_and_continue = (980, 1015)
		self.moveTo(skip_and_continue[0] + random.randint(-500, 500), skip_and_continue[1] + random.randint(-13, 13), 0.3)
		pyautogui.click()
		time.sleep(random.uniform(2.5, 3.2)) 
		self.moveTo(self.hero_mvp[1] + random.randint(-150, 150), self.hero_mvp[0] + random.randint(-40, 40), 0.3)
		pyautogui.click()
		time.sleep(random.uniform(2, 2.5))
		self.moveTo(cast_location[1] + random.randint(250, 270), cast_location[0] + random.randint(-11, 11), 0.3) # for the kingdom rewards
		self.doubleClick()

	def doubleClick(self):
		pyautogui.doubleClick(interval = random.uniform(0.1, 0.15))

	def isMyTurn(self, check_end_game = False):
		time.sleep(0.5)
		ss = pyautogui.screenshot()
		pixels = numpy.array(ss)
		my_arrow_x = 317 #TODO: make my_array and enemy_arrow as member
		my_count = 0
		for l in range(26):
			if(pixels[l][my_arrow_x][0] == 255 and pixels[l][my_arrow_x][1] == 255 and pixels[l][my_arrow_x][2] == 255):
				my_count = my_count + 1

		enemy_arrow_x = 1601
		enemy_count = 0
		for l in range(26):
			if(pixels[l][enemy_arrow_x][0] == 255 and pixels[l][enemy_arrow_x][1] == 255 and pixels[l][enemy_arrow_x][2] == 255):
				enemy_count = enemy_count + 1
		if(check_end_game):
			if(my_count == 0 and enemy_count == 0):
				return False
			return True
		if(my_count > 7):
			return True
		elif(enemy_count > 7):
			return False

		return True

	def moveTo(self, x, y, max_duration = 0.5):
		pyautogui.moveTo(x, y, duration=random.uniform(0.2, max_duration))

class Ricky():
	def __init__(self):
		self.table = tableManager()
		self.spells = spellManager()
		self.env = envManager()

	def makeMove(self):
			self.table.createMatrix()
			self.table.findAllMoves()
			ok1, ok2, ok3, ok4 = self.spells.getSpellsStatus()

			if(ok1 and self.table.twoColorsExtraTurn(2 << 2, 2 << 6)): #green w/ skull
				self.spells.useSpell(1)
				time.sleep(random.uniform(0.8, 1))
			elif(self.table.moves[0].extra_turn):
				self.table.makeMove()
			elif(ok2):
				self.spells.useSpell(2)
				time.sleep(random.uniform(0.5, 0.7))
			elif(ok3):
				self.spells.useSpell(3)
				time.sleep(random.uniform(0.8, 1))
			elif(ok4):
				self.spells.useSpell(4)
				time.sleep(random.uniform(0.2, 0.35))
			else:
				self.table.makeMove()

	def play(self):
		time.sleep(2)
		count = 0
		while(1):
			self.env.enterBattle()
			while(self.env.battleGoing()):
				self.makeMove()
				while(not self.env.isMyTurn()):
					time.sleep(2)
			self.env.enterPvpScreen()
			count = count + 1
			if(count % 15 == 0):
				time.sleep(random.randint(60 * 15, 60 * 20))

if __name__ == '__main__':
	if(8):
		print('da')
	riky = Ricky()
	riky.play()