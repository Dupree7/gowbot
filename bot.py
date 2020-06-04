import pyautogui
import random
import numpy as np
import time

square_length = 119
padding_left = 485
padding_top = 80

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
			if(self.name == 's' or self.name == 'S' or self.name == 'g'):
				return True

		return self.extra_turn > obj.extra_turn

class Riky():
	def __init__(self):
		self.matrix = [['x' for x in range(8)] for y in range(8)]
		self.moves = []

	def moveTo(self, x, y):
		pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5)) 
	def click(self):
		pyautogui.click()
	def dragTo(self, x, y):
		pyautogui.dragTo(x, y, duration=random.uniform(0.2, 0.5))

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

	def CountColor(self, color, i, j):
		horizontal = 1
		vertical = 1

		temp_i = i - 1
		while(temp_i > - 1):
			if(self.matrix[temp_i][j] == self.matrix[i][j]):
				vertical = vertical + 1
				temp_i = temp_i - 1
			else:
				break
		temp_i = i + 1
		while(temp_i < 8):
			if(self.matrix[temp_i][j] == self.matrix[i][j]):
				vertical = vertical + 1
				temp_i = temp_i + 1
			else:
				break

		temp_j = j - 1
		while(temp_j > -1):
			if(self.matrix[i][temp_j] == self.matrix[i][j]):
				horizontal = horizontal + 1
				temp_j = temp_j - 1
			else:
				break
		temp_j = j + 1
		while(temp_j < 8):
			if(self.matrix[i][temp_j] == self.matrix[i][j]):
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

		move_a_count, move_a_extra_turn = self.CountColor(self.matrix[i][j], i, j) 
		move_a = move(self.matrix[i][j], move_a_count, i, j, i, j + 1, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.CountColor(self.matrix[i][j + 1], i, j + 1) 
		move_b = move(self.matrix[i][j + 1], move_b_count, i, j + 1, i, j, move_b_extra_turn)

		temp = self.matrix[i][j + 1]
		self.matrix[i][j + 1] = self.matrix[i][j]
		self.matrix[i][j] = temp

		return move_a, move_b

	def getMoveToBottom(self, i, j):
		temp = self.matrix[i][j]
		self.matrix[i][j] = self.matrix[i + 1][j]
		self.matrix[i + 1][j] = temp

		move_a_count, move_a_extra_turn = self.CountColor(self.matrix[i][j], i, j) 
		move_a = move(self.matrix[i][j], move_a_count, i, j, i + 1, j, move_a_extra_turn)

		move_b_count, move_b_extra_turn = self.CountColor(self.matrix[i + 1][j], i + 1, j) 
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
		#for move in self.moves:
		print(self.moves[0])
		self.moves.clear()

	def Play(self):
		time.sleep(2) # to alt-tab to the game

		while(1): #find end condition
			self.createMatrix()
			#print(self.matrix)
			#break;
			self.FindAllMoves()
			self.makeMove() #or use spell
			time.sleep(2)

if __name__ == '__main__':
	riky = Riky()
	riky.Play()