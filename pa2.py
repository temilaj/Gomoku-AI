# 
# Programming Assignment 2, CS640
#
# A Gomoku (Gobang) Game
#
# Adapted from CS111
# By Yiwen Gu
#
# You need to implement an AI Player for Gomoku
# A Random Player is provided for you
# 
#
import random
from pa2_gomoku import Player
import copy
import math

WINDOW_LENGTH = 5
EMPTY = ' '

def is_not_blank(s):
    return bool(s and s.strip())

class AIPlayer(Player):
	""" a subclass of Player that looks ahead some number of moves and 
	strategically determines its best next move.
	"""

	def __init__(self, checker):
		self.ROW_COUNT = 0
		self.COLUMN_COUNT = 0
		self.checker = checker
		if checker == 'X':
			self.opponent_checker = 'O'
		else:
			self.opponent_checker = 'X'

	def drop_piece(self, temp_slots, row, col, piece):
		temp_slots[row][col] = piece

	def get_valid_locations(self, board):
		valid_locations = []
		for row in range(self.ROW_COUNT):
			for col in range(self.COLUMN_COUNT):
				if board.can_add_to(row, col):
					valid_locations.append((row, col))
		return valid_locations
	
	def valid_locations_exist(self, board):
		for row in range(self.ROW_COUNT):
			for col in range(self.COLUMN_COUNT):
				if board.can_add_to(row, col):
					return True
		return False

	def get_next_open_row(self, board, row, col):
		for r in range(self.ROW_COUNT):
			entry = board.slots[r][col]
			# print('entry', entry)
			if not is_not_blank(entry):
				return r

	def evaluate_window(self, window, piece):
		score = 0
		opponent_piece = self.checker
		if piece == self.checker:
			opponent_piece = self.opponent_checker
		# print('window', window)
		if window.count(piece) == 5:
			print('count 5')
			score += 100
		elif window.count(piece) == 4 and window.count(EMPTY) == 1:
			# print('count 4')
			score += 10
		elif window.count(piece) == 3 and window.count(EMPTY) == 2:
			# print('count 3')
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 3:
			# print('count 2')
			score += 2
		elif window.count(piece) == 1 and window.count(EMPTY) == 4:
			# print('count 1')
			score += 1

		if window.count(opponent_piece) == 4 and window.count(EMPTY) == 1:
			# print(window)
			print(' ====== = fa-ol ----')
			score -= 800
		elif window.count(opponent_piece) == 3 and window.count(EMPTY) == 2:
			score -= 2
		# print('score', score)
		return score

	def score_position(self, temp_board, piece):
		score = 0

		# Score center column
		# center_array = [int(i) for i in list(temp_board[:, self.COLUMN_COUNT//2])]
		# center_array = temp_board[self.COLUMN_COUNT//2]
		# # print('center_array')
		# # print(center_array)
		# center_count = center_array.count(piece)
		# # print('center_count', center_count)
		# score += center_count * 3

		# Score Horizontal
		for row in range(self.ROW_COUNT):
			row_array = temp_board[row]
			# row_array = [int(i) for i in list(temp_board[row,:])]
			for column in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				# if self.COLUMN_COUNT - column >= WINDOW_LENGTH:
				# 	window = row_array[column: column + WINDOW_LENGTH]
				# else:
				# 	print('reverse')
				# 	# window = row_array[-WINDOW_LENGTH :]
				# 	window = row_array[-WINDOW_LENGTH :]
				window = row_array[column: column + WINDOW_LENGTH]
				# print('window', window)
				score += self.evaluate_window(window, piece)
		# # Score Vertical
		for column in range(self.COLUMN_COUNT):
			# col_array = [int(i) for i in list(board[:,c])]
			# row_array = temp_board[row]
			# col_array = temp_board[column]
			col_array = list(sub[column] for sub in temp_board) 
			for row in range(self.ROW_COUNT - WINDOW_LENGTH + 1):
				window = col_array[row: row + WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		# # Score posiive sloped diagonal
		for r in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
			for c in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				window = [temp_board[r + i][ c + i ] for i in range(WINDOW_LENGTH)]
				# print('window', window)
				score += self.evaluate_window(window, piece)


		for r in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
			for c in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				window = [temp_board[r + WINDOW_LENGTH - 1 - i][c + i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		return score;


	# def generate_matrix(original_list):
	# 	return [list(ele) for ele in test_list]

	def pick_best_move(self, board, piece):
		valid_locations = self.get_valid_locations(board)
		best_score = -10000
		best_move = random.choice(valid_locations)
		for location in valid_locations:
			row = location[0]
			column = location[1]
			# next_row = self.get_next_open_row(board, row, column)
			# print('row, column', row, column)
			# print('next_row, column', next_row, column)
			temp_slots = copy.deepcopy(board.slots)
			self.drop_piece(temp_slots, row, column, piece)
			score = self.score_position(temp_slots, piece)
			print('score', score)
			print('best_score', best_score)
			if score > best_score:
				best_score = score
				# best_move = (row, column)
				# print('best move', next_row, column)
				best_move = (row, column)


		return best_move;


	def next_move(self, board):
		""" returns the called AIPlayer's next move for a game on
			the specified Board object. 
			input: board is a Board object for the game that the called
					 Player is playing.
			return: row, col are the coordinated of a vacant location on the board 
		"""
		self.num_moves += 1
		self.ROW_COUNT = board.height
		self.COLUMN_COUNT = board.width
		# open_pos = []
		# for row in range(board.height):
		# 	for col in range(board.width):
		# 		if board.can_add_to(row, col):
		# 			open_pos.append((row, col))
		
		# return random.choice(open_pos)
		next_move = self.pick_best_move(board, self.checker)
		# next_move, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)

		print('next_move', next_move)

		return next_move
		
		
		################### TODO: ######################################
		# Implement your strategy here. 
		# Feel free to call as many as helper functions as you want.
		# We only cares the return of this function
		################################################################
		
	def is_terminal_node(self, board):
		# return heuristic value of node if it's a terminal node
		return winning_move(board, self.checker) or winning_move(board, self.opponent_checker) or len(self.get_valid_locations(board)) == 0

	def minimax(self, board, depth, alpha, beta, maximizingPlayer):
		## else recursively check tree for best score

		valid_locations = self.get_valid_locations(board)
		is_terminal = self.is_terminal_node(board)
		if depth == 0 or is_terminal:
			if is_terminal:
				if winning_move(board, self.opponent_checker):
					return (None, 100000000000000)
				elif winning_move(board, self.checker):
					return (None, -10000000000000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				# if depth is zero, find the heuristic value of the board
				return (None, self.score_position(board, self.opponent_checker))
		if maximizingPlayer:
			value = -math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.get_next_open_row(board, col)
				b_copy = self.deepcopy(board.slots)
				self.drop_piece(b_copy, row, col, self.opponent_checker)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
				if new_score > value:
					value = new_score
					column = col
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return column, value

		else: # Minimizing player
			value = math.inf
			column = random.choice(valid_locations)
			for col in valid_locations:
				row = self.get_next_open_row(board, col)
				b_copy = self.deepcopy(board.slots)
				self.drop_piece(b_copy, row, col, self.checker)
				new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
				if new_score < value:
					value = new_score
					column = col
				beta = min(beta, value)
				if alpha >= beta:
					break
			return column, value
