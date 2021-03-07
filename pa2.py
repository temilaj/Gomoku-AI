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
		next_move, minimax_score = self.minimax(board.slots, 2, -math.inf, math.inf, True)

		print('next_move', next_move)

		return next_move

	def drop_piece(self, temp_slots, row, col, piece):
		temp_slots[row][col] = piece
	
	def get_valid_locations(self, board):
		valid_locations = []
		for row in range(self.ROW_COUNT):
			for col in range(self.COLUMN_COUNT):
				if board[row][col] == EMPTY:
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
			if not is_not_blank(entry):
				return r

	def evaluate_window(self, window, piece):
		score = 0
		opponent_piece = self.checker
		if piece == self.checker:
			opponent_piece = self.opponent_checker
		if window.count(piece) == 5:
			score += 100
		elif window.count(piece) == 4 and window.count(EMPTY) == 1:
			score += 10
		elif window.count(piece) == 3 and window.count(EMPTY) == 2:
			score += 5
		elif window.count(piece) == 2 and window.count(EMPTY) == 3:
			score += 2
		elif window.count(piece) == 1 and window.count(EMPTY) == 4:
			score += 1

		if window.count(opponent_piece) == 4 and window.count(EMPTY) == 1:
			score -= 8
		elif window.count(opponent_piece) == 3 and window.count(EMPTY) == 2:
			score -= 6
		return score

	def score_position(self, temp_board, piece):
		score = 0

		# Score Horizontal
		for row in range(self.ROW_COUNT):
			row_array = temp_board[row]
			for column in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				window = row_array[column: column + WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)
		# # Score Vertical
		for column in range(self.COLUMN_COUNT):
			# col_array = [int(i) for i in list(board[:,c])]
			col_array = list(sub[column] for sub in temp_board) 
			for row in range(self.ROW_COUNT - WINDOW_LENGTH + 1):
				window = col_array[row: row + WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		# Score positive sloped diagonal
		for r in range(self.ROW_COUNT - WINDOW_LENGTH + 1):
			for c in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				window = [temp_board[r + i][ c + i ] for i in range(WINDOW_LENGTH)]
				# print('window', window)
				score += self.evaluate_window(window, piece)


		# negative positive sloped diagonal
		for r in range(self.ROW_COUNT - WINDOW_LENGTH + 1):
			for c in range(self.COLUMN_COUNT - WINDOW_LENGTH + 1):
				window = [temp_board[r + WINDOW_LENGTH - 1 - i][c + i] for i in range(WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		return score;

	def pick_best_move(self, board, piece):
		valid_locations = self.get_valid_locations(board.slots)
		best_score = -10000
		best_move = random.choice(valid_locations)
		for location in valid_locations:
			row = location[0]
			column = location[1]
			temp_slots = copy.deepcopy(board.slots)
			self.drop_piece(temp_slots, row, column, piece)
			score = self.score_position(temp_slots, piece)
			if score > best_score:
				best_score = score
				best_move = (row, column)


		return best_move;

	def is_terminal_node(self, board, valid_locations):
		# return heuristic value of node if it's a terminal node
		return self.winning_move(board, self.checker, valid_locations) or self.winning_move(board, self.opponent_checker, valid_locations) or len(valid_locations) == 0

	def minimax(self, board, depth, alpha, beta, maximizingPlayer):

		valid_locations = self.get_valid_locations(board)
		is_terminal = self.is_terminal_node(board, valid_locations)
		if depth == 0 or is_terminal:
			if is_terminal:
				if self.winning_move(board, self.opponent_checker, valid_locations):
					return (valid_locations[0], 100000000000000)
				elif self.winning_move(board, self.checker, valid_locations):
					return (valid_locations[0], -10000000000000)
				else: # Game is over, no more valid moves
					return (valid_locations[0], 0)
			else: # Depth is zero
				# if depth is zero, find the heuristic value of the board
				return (valid_locations[0], self.score_position(board, self.opponent_checker))
		#else recursively check tree for best score
		if maximizingPlayer:
			value = -math.inf
			best_move = random.choice(valid_locations)
			for location in valid_locations:
				row = location[0]
				col = location[1]
				# row = self.get_next_open_row(board, col)
				temp_slots = copy.deepcopy(board)
				self.drop_piece(temp_slots, row, col, self.opponent_checker)
				new_score = self.minimax(temp_slots, depth-1, alpha, beta, False)[1]
				# print('max -new_score', new_score)
				if new_score > value:
					value = new_score
					best_move = location
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return best_move, value

		else: # Minimizing player
			value = math.inf
			best_move = random.choice(valid_locations)
			for location in valid_locations:
				row = location[0]
				col = location[1]
				# row = self.get_next_open_row(board, col)
				temp_slots = copy.deepcopy(board)
				self.drop_piece(temp_slots, row, col, self.checker)
				new_score = self.minimax(temp_slots, depth-1, alpha, beta, True)[1]
				# print('min -new_score', new_score)
				if new_score < value:
					value = new_score
					best_move = location
				beta = min(beta, value)
				if alpha >= beta:
					break
			return best_move, value

	def winning_move(self, board, checker, valid_locations):
		""" Checks for if the specified checker added to position x, y will 
			lead to a win
		"""
		for location in valid_locations:
			r = location[0]
			c = location[1]
			return self.is_horizontal_win(board, checker,r,c) \
				or self.is_vertical_win(board, checker,r,c) \
				or self.is_diagonal1_win(board, checker,r,c) \
				or self.is_diagonal2_win(board, checker,r,c)

	def is_horizontal_win(self, board, checker, r, c):
		cnt = 0
		
		for i in range(5):
			# Check if the next four columns in this row
			# contain the specified checker.
			if c+i < self.COLUMN_COUNT and board[r][c+i] == checker:
				cnt += 1
			else:
				break
		
		if cnt == 5:
			return True
		else:
			# check towards left           
			for i in range(1, 6-cnt):
				if c-i >= 0 and board[r][c-i] == checker:
					cnt += 1
				else:
					break
			   
			if cnt == 5:
				return True  
			
		return False
						
	def is_vertical_win(self, board, checker, r, c):
		cnt = 0
		for i in range(5):
			# Check if the next four rows in this col
			# contain the specified checker.            
			if r+i < self.COLUMN_COUNT and board[r+i][c] == checker:
				cnt += 1
			else:
				break
		
		if cnt == 5:
			return True
		else:
			# check upwards
			for i in range(1, 6-cnt):
				if r-i >= 0 and board[r-i][c] == checker:
					cnt += 1
				else:
					break
			
			if cnt == 5:
				return True  
			
		return False

	def is_diagonal1_win(self, board, checker, r, c):
		cnt = 0
		for i in range(5):
			if r+i < self.ROW_COUNT and c+i < self.COLUMN_COUNT and \
				board[r+i][c+i] == checker:                    
				cnt += 1
			else:
				break
		if cnt == 5:
			return True
		else:
			for i in range(1, 6-cnt):
				if r-i >= 0 and c-i >= 0 and \
					board[r-i][c-i] == checker:
						cnt += 1
				else:
					break
				
			if cnt == 5:
				return True  
		
		return False    

	def is_diagonal2_win(self, board, checker, r, c):
		cnt = 0
		for i in range(5):
			if r-i >= 0 and c+i < self.COLUMN_COUNT and \
				board[r-i][c+i] == checker:
				cnt += 1
			else:
				break
			
		if cnt == 5:
			return True
		else:
			for i in range(1, 6-cnt):
				if r+i < self.ROW_COUNT and c-i >= 0 and \
					board[r+i][c-i] == checker:
					cnt += 1
				else:
					break
				
			if cnt == 5:
				return True  
		
		return False 