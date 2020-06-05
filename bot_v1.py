import pyautogui
import random
import numpy as np
import time

square_length = 119
padding_left = 485
padding_top = 80
cast_location = (968, 955) #x y
spell_check_pixel = [19, 227, 246]

def around(x, c):
	if(c - 0.3 <= x and x <= c + 0.3):
		return 1
	return 0

def rgbToChar(r, g, b):
	if(around(r, 0.16) and around(g, 0.88) and around(b, 1.045)): #blue
		return 'b'
	elif(around(r, 1.225) and around(g, 0.98) and around(b, 0.5)): #yellow
		return 'y' 
	elif(around(r, 1.13) and around(g, 0.22) and around(b, 0.37)): #red
		return 'r'
	elif(around(r, 0.79) and around(g, 0.16) and around(b, 1.06)): #purple
		return 'p'
	elif(around(r, 0.87) and around(g, 0.66) and around(b, 0.6)): #Brown
		return 'B' 
	elif(around(r, 0.64) and around(g, 1.02) and around(b, 0.25)): #green
		return 'g'
	elif(around(r, 1.25) and around(g, 1.15) and around(b, 1.21)): #small skull 
		return 's' 
	else:
		return 'S' #bigg skull

class move():
	def __init__(self, name, color_count, from_x, from_y, to_x, to_y, extra_turn):
		self.name = name
		self.color_count = color_count
		self.from_x = from_x
		self.from_y = from_y
		self.to_x = to_x
		self.to_y = to_y
		self.extra_turn = extra_turn
	def __str__(self):
		return "{0} of {1} ({2}, {3}) -> ({4}, {5})".format(self.color_count, self.name, self.from_x + 1, self.from_y + 1, self.to_x + 1, self.to_y + 1)
	def __lt__(self, obj):
		if(self.extra_turn == obj.extra_turn):
			if(self.name == 's' or self.name == 'S'):
				return True; 
			if(self.name == 'g' or self.name == 'b'):
				return True
			if(self.name == 'B'):
				return True
		return self.extra_turn > obj.extra_turn

class Riky():
	def __init__(self):
		self.matrix = [['x' for x in range(8)] for y in range(8)]
		self.moves = []
		self.used_spell = False

	def moveTo(self, x, y, max_duration = 0.5):
		pyautogui.moveTo(x, y, duration=random.uniform(0.2, max_duration)) 

	def click(self):
		pyautogui.click()

	def dragTo(self, x, y):
		pyautogui.dragTo(x, y, duration=random.uniform(0.2, 0.5))

	def pressKey(self, key):
		time.sleep(random.uniform(0.5, 0.615))
		pyautogui.press('esc')

	def castSpell(self):
		pyautogui.moveTo(cast_location[0], cast_location[1], 0.3)
		pyautogui.click()

	def getColorFromSquare(self, pixels, i, j):
		r, g, b = 0, 0, 0

		for l in range(padding_top + 20 + i * square_length, padding_top + 20 + i * square_length + 1):
			for c in range(padding_left + 35 + j * square_length, padding_left + 35 + j * square_length + 40):
				r = r + pixels[l][c][0]
				g = g + pixels[l][c][1]
				b = b + pixels[l][c][2]

		r = r / (89 * 89)
		g = g / (89 * 89)
		b = b / (89 * 89)
		#print("r = ",r, ", green = ", g, ", blue = ", b)
		#if(j == 7):
			#print("")
		return rgbToChar(r, g, b)

	def createMatrix(self):
		ss = pyautogui.screenshot()
		pixels = np.array(ss)

		for i in range(0, 8):
			for j in range(0, 8):
				self.matrix[i][j] = self.getColorFromSquare(pixels, i, j)

	def interchange(self, from_i, from_j, to_i, to_j):
		x,y = self.getPixelsAt(from_i, from_j)
		to_x, to_y = self.getPixelsAt(to_i, to_j)
		self.moveTo(x, y)
		self.dragTo(to_x, to_y)

	def getPixelsAt(self, i, j):
		x = padding_left + j * square_length + square_length / 2 + random.randint(-40, 40)
		y = padding_top + i * square_length + square_length / 2 + random.randint(-40, 40)
		return x,y

	def CountColor(self, i, j):
		horizontal = 1
		vertical = 1

		ok = self.matrix[i][j] == 's' or self.matrix[i][j] == 'S'
		temp_i = i - 1
		while(temp_i > - 1):
			if(self.matrix[temp_i][j] == self.matrix[i][j] or (ok and (self.matrix[temp_i][j] == 's' and self.matrix[temp_i][j] ==' S'))):
				vertical = vertical + 1
				temp_i = temp_i - 1
			else:
				break
		temp_i = i + 1
		while(temp_i < 8):
			if(self.matrix[temp_i][j] == self.matrix[i][j] or (ok and (self.matrix[temp_i][j] == 's' and self.matrix[temp_i][j] ==' S'))):
				vertical = vertical + 1
				temp_i = temp_i + 1
			else:
				break

		temp_j = j - 1
		while(temp_j > -1):
			if(self.matrix[i][temp_j] == self.matrix[i][j] or (ok and (self.matrix[i][temp_j] == 's' and self.matrix[i][temp_j] ==' S'))):
				horizontal = horizontal + 1
				temp_j = temp_j - 1
			else:
				break
		temp_j = j + 1
		while(temp_j < 8):
			if(self.matrix[i][temp_j] == self.matrix[i][j] or (ok and (self.matrix[i][temp_j] == 's' and self.matrix[i][temp_j] ==' S'))):
				horizontal = horizontal + 1
				temp_j = temp_j + 1
			else:
				break

		if(horizontal > 3):
			return horizontal, 1
		if(vertical > 3):
			return vertical, 1
		return max(horizontal, vertical), 0

	def getMoveToRight(self, i, j):
		temp = self.matrix[i][j + 1]
		self.matrix[i][j + 1] = self.matrix[i][j]
		self.matrix[i][j] = temp

		move_a_count, move_a_extra_turn = self.CountColor( i, j) 
		move_a = move(self.matrix[i][j], move_a_count, i, j, i, j + 1, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.CountColor(i, j + 1) 
		move_b = move(self.matrix[i][j + 1], move_b_count, i, j + 1, i, j, move_b_extra_turn)

		temp = self.matrix[i][j + 1]
		self.matrix[i][j + 1] = self.matrix[i][j]
		self.matrix[i][j] = temp

		return move_a, move_b

	def getMoveToBottom(self, i, j):
		temp = self.matrix[i][j]
		self.matrix[i][j] = self.matrix[i + 1][j]
		self.matrix[i + 1][j] = temp

		move_a_count, move_a_extra_turn = self.CountColor(i, j) 
		move_a = move(self.matrix[i][j], move_a_count, i, j, i + 1, j, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.CountColor(i + 1, j) 
		move_b = move(self.matrix[i + 1][j], move_b_count, i + 1, j, i, j, move_b_extra_turn)

		temp = self.matrix[i][j]
		self.matrix[i][j] = self.matrix[i + 1][j]
		self.matrix[i + 1][j] = temp

		return move_a, move_b

	def FindAllMoves(self):
		for i in range(8):
			for j in range(7): #left to right
				move_a, move_b = self.getMoveToRight(i, j)
				if move_a.color_count > 2:
					self.moves.append(move_a)
				if move_b.color_count > 2:
					self.moves.append(move_b)

		for i in range(7):
			for j in range(8):
				move_a, move_b = self.getMoveToBottom(i, j)
				if move_a.color_count > 2:
					self.moves.append(move_a)
				if move_b.color_count > 2:
					self.moves.append(move_b)

		self.moves.sort()

	def makeMove(self):
		self.interchange(self.moves[0].from_x, self.moves[0].from_y, self.moves[0].to_x, self.moves[0].to_y)
		self.moves.clear()

	def getSpellsStatus(self):
		ss = pyautogui.screenshot()
		pixels = np.array(ss)

		ok1 = (pixels[75][169][0] == spell_check_pixel[0] and pixels[75][169][1] == spell_check_pixel[1] and pixels[75][169][2] == spell_check_pixel[2])
		ok2 = (pixels[330][169][0] == spell_check_pixel[0] and pixels[330][169][1] == spell_check_pixel[1] and pixels[330][169][2] == spell_check_pixel[2])
		ok3 = (pixels[585][169][0] == spell_check_pixel[0] and pixels[585][169][1] == spell_check_pixel[1] and pixels[585][169][2] == spell_check_pixel[2])
		ok4 = (pixels[840][169][0] == spell_check_pixel[0] and pixels[840][169][1] == spell_check_pixel[1] and pixels[840][169][2] == spell_check_pixel[2])

		return ok1, ok2, ok3, ok4

	def doomedClubExtraTurn(self):
		for line in range(8):
			count = 0
			for column in range(8):
				if(self.matrix[line][column] == 'g' or self.matrix[line][column] == 's' or self.matrix[line][column] == 'S'):
					count = count + 1
				else:
					count = 0
				if(count > 3):
					return True

		for column in range(8):
			count = 0
			for line in range(8):
				if(self.matrix[line][column] == 'g' or self.matrix[line][column] == 's' or self.matrix[line][column] == 'S'):
					count = count + 1
				else:
					count = 0
				if(count > 3):
					return True
		return False

	def useSpell(self, index):
		has_target = False
		if(index == 1):
			first_spell_location = (190, 320)
			self.moveTo(first_spell_location[1] + random.randint(-120, 120), first_spell_location[0] + random.randint(-80, 80), 0.3)
			self.click()
		elif(index == 2):
			second_spell_location = (450, 320)
			self.moveTo(second_spell_location[1] + random.randint(-120, 120), second_spell_location[0] + random.randint(-80, 80), 0.3)
			self.click()
		elif(index == 3):
			has_target = True
			third_spell_location = (700, 320)
			self.moveTo(third_spell_location[1] + random.randint(-120, 120), third_spell_location[0] + random.randint(-80, 80), 0.3); #has target
			self.click();
		else:
			has_target = True
			forth_spell_location = (940, 320)
			self.moveTo(forth_spell_location[1] + random.randint(-120, 120), forth_spell_location[0] + random.randint(-80, 80), 0.3); #has target
			self.click();

		self.moveTo(cast_location[1] + random.randint(-150, 150), cast_location[0] + random.randint(-40, 40), 0.3)
		self.click()

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
			self.click()
			time.sleep(0.1)

	def checkSpells(self):
		ok1, ok2, ok3, ok4 = self.getSpellsStatus()

		if(ok1 and self.doomedClubExtraTurn()):
			self.useSpell(1)
			time.sleep(random.uniform(1, 1.5))
			return
		if(self.moves[0].extra_turn == True or (self.moves[0].name == 's' or self.moves[0].name == 'S')):
			return
		if(ok3):
			self.useSpell(3)
			time.sleep(random.uniform(0.6, 0.80))
			return
		if(ok2):
			self.useSpell(2)
			time.sleep(random.uniform(0.6, 0.80))
			return
		if(ok4):
			self.useSpell(4)
			time.sleep(random.uniform(0.15, 0.3))
			return
		if(ok1):
			self.useSpell(1)
			time.sleep(random.uniform(0.4, 0.6))

	def enterBattle(self):
		middle_enemy = (960, 550)
		self.moveTo(middle_enemy[0] + random.randint(-130, 130), middle_enemy[1] + random.randint(-200, 200))
		self.click()
		time.sleep(0.15)

		start_fight = (980, 1015)
		self.moveTo(start_fight[0] + random.randint(-500, 500), start_fight[1] + random.randint(-25, 25))
		self.click()
		time.sleep(7)

	def isMyTurn(self, check_end_game = False):
		time.sleep(0.5)
		ss = pyautogui.screenshot()
		pixels = np.array(ss)
		my_arrow_x = 317
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
				return True
			return False
		if(my_count > 7):
			return True
		elif(enemy_count > 7):
			return False

		return True

	def gameEnded(self):
		ok = self.isMyTurn(check_end_game = True)
		time.sleep(0.5)
		ok = ok | self.isMyTurn(check_end_game = True)
		return ok

	def doubleClick(self):
		pyautogui.doubleClick(interval = random.uniform(0.1, 0.15))

	def enterPvpScreen(self):
		skip_and_continue = (980, 1015)
		self.moveTo(skip_and_continue[0] + random.randint(-500, 500), skip_and_continue[1] + random.randint(-25, 25), 0.3)
		self.click()
		time.sleep(random.uniform(3, 3.5)) 
		self.moveTo(cast_location[1] + random.randint(-150, 150), cast_location[0] + random.randint(-40, 40), 0.3)
		self.click()
		time.sleep(random.uniform(2, 2.5))
		self.moveTo(cast_location[1] + random.randint(240, 270), cast_location[0] + random.randint(-15, 15), 0.3) # for the kingdom rewards
		self.doubleClick()

	def Play(self):
		time.sleep(2) # to alt-tab to the game
		
		count = 0
		while(1):
			self.enterBattle()
			while(not self.gameEnded()):
				self.createMatrix() 
				self.FindAllMoves()
				self.checkSpells()
				if(not self.isMyTurn()):
					continue
				self.makeMove()
				while(not self.isMyTurn()):
					time.sleep(2)
			self.enterPvpScreen()
			count = count + 1
			print(count)

if __name__ == '__main__':
	riky = Riky()
	riky.Play()
