import copy
import random
from math import inf
from threading import Thread


class Solution:
    def __init__(self, board):
        self.bo = board
        self.evaluation = outer_board_estimation(self.bo)

    def random_choice(self, color):
        all_pieces = []
        all_moves = []
        was_checked = self.bo.is_checked(color)
        self.bo.update_moves()
        new_board = copy.deepcopy(self.bo)
        for row in range(0, 8):
            for col in range(0, 8):
                if new_board.board[row][col] != 0:
                    if new_board.board[row][col].color == color:
                        if len(new_board.board[row][col].move_list) > 0:
                            all_pieces.append(new_board.board[row][col])
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        return (piece.row, piece.col), (move[0], move[1])
                else:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        all_moves.append(((piece.row, piece.col), (move[0], move[1])))
        if was_checked:
            return -1
        else:
            if len(all_moves) <= 0:
                return -1
            return random.choice(all_moves)

    def tier3_choice(self, color):
        all_pieces = []
        best_value = -inf
        was_checked = self.bo.is_checked(color)
        self.bo.update_moves()
        new_board = copy.deepcopy(self.bo)
        best_move = -1
        for row in range(0, 8):
            for col in range(0, 8):
                if new_board.board[row][col] != 0:
                    if new_board.board[row][col].color == color:
                        if len(new_board.board[row][col].move_list) > 0:
                            all_pieces.append(new_board.board[row][col])
        for piece in all_pieces:
            for move in piece.move_list:
                if was_checked:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if best_move == -1:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board)
                        elif outer_board_estimation(new_board) > best_value:
                            best_move = (piece.row, piece.col), (move[0], move[1])
                            best_value = outer_board_estimation(new_board)
                else:
                    new_board = copy.deepcopy(self.bo)
                    new_board.simple_move((piece.row, piece.col), (move[1], move[0]), color)
                    if not new_board.is_checked(color):
                        if outer_board_estimation(new_board) > best_value:
                            best_value = outer_board_estimation(new_board)
                            best_move = (piece.row, piece.col), (move[0], move[1])
        if best_value == self.evaluation and not was_checked:
            return self.random_choice(color)
        return best_move

    def tier2_choice(self, color):

        return self.random_choice(color)


def get_all_moves(board, color):
    all_moves = []
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0 and board.board[row][col].color == color:
                for move in board.board[row][col].move_list:
                    all_moves.append(((row, col), (move[1], move[0])))
    return all_moves


def outer_board_estimation(board):
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 900
    return black_score - white_score


def outer_board_advanced_estimation(board):
    white_score = 0
    black_score = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if board.board[row][col] != 0:
                if board.board[row][col].color == "w":
                    if board.board[row][col].__class__.__name__ == "Rook":
                        white_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        white_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        white_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        white_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        white_score += 900
                else:
                    if board.board[row][col].__class__.__name__ == "Rook":
                        black_score += 50
                    elif board.board[row][col].__class__.__name__ == "Pawn":
                        black_score += 10
                    elif board.board[row][col].__class__.__name__ == "Bishop":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Knight":
                        black_score += 30
                    elif board.board[row][col].__class__.__name__ == "Queen":
                        black_score += 90
                    elif board.board[row][col].__class__.__name__ == "King":
                        black_score += 900
    return black_score - white_score
