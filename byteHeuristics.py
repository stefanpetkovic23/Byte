
def evaluate_central_control(board, player):
    player_token = 'O' if player == 0 else 'X'
    center_bonus = 2
    n = len(board)
    score = 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if board[i][j]['stek'] and board[i][j]['stek'][-1] == player_token:
                score += len(board[i][j]['stek']) * center_bonus
    return score


def evaluate_diagonal_neighbors(board, player):
    player_token = 'O' if player == 0 else 'X'
    score = 0
    for i in range(len(board) - 1):
        for j in range(len(board[i]) - 1):
            if board[i][j]['stek'] and board[i + 1][j + 1]['stek']:
                if board[i][j]['stek'][-1] == player_token and board[i + 1][j + 1]['stek'][-1] == player_token:
                    score += 1
    return score


def count_tokens_on_top_of_stacks(board, player):
    player_token = 'O' if player == 0 else 'X'
    score = 0
    for row in board:
        for cell in row:
            if cell['stek'] and cell['stek'][-1] == player_token:
                score += len(cell['stek']) ** 2
    return score



def count_tokens_on_board(board, player):
    player_token = 'O' if player == 0 else 'X'
    count = sum(cell['stek'].count(player_token) for row in board for cell in row)
    return count

def evaluate_full_stack_control(board, player, brojStekova, brojStekovaBelih, brojStekovaCrnih):
    player_token = 'O' if player == 0 else 'X'
    opponent_token = 'X' if player == 0 else 'O'

    player_stacks = brojStekovaBelih if player_token == 'O' else brojStekovaCrnih
    opponent_stacks = brojStekovaCrnih if player_token == 'O' else brojStekovaBelih
    positive_score = 1000 
    negative_score = -1000 

    victory_threshold = brojStekova / 2
    if player_stacks == victory_threshold - 1 or opponent_stacks == victory_threshold - 1:
        positive_score *= 10  
        negative_score *= 10  

    score = 0
    for row in board:
        for cell in row:
            if len(cell['stek']) == 8:
                if cell['stek'][-1] == player_token:
                    score += positive_score
                elif cell['stek'][-1] == opponent_token:
                    score += negative_score

    return score



