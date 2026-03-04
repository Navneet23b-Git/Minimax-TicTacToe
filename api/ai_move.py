import math
import json

def check_winner(board):

    for i in range(3):

        if board[i][0]==board[i][1]==board[i][2]!=" ":
            return board[i][0]

        if board[0][i]==board[1][i]==board[2][i]!=" ":
            return board[0][i]

    if board[0][0]==board[1][1]==board[2][2]!=" ":
        return board[0][0]

    if board[0][2]==board[1][1]==board[2][0]!=" ":
        return board[0][2]

    return None


def is_draw(board):

    for i in range(3):
        for j in range(3):
            if board[i][j]==" ":
                return False

    return True


def minimax(board,depth,is_max):

    winner = check_winner(board)

    if winner=="X":
        return 10-depth

    if winner=="O":
        return depth-10

    if is_draw(board):
        return 0


    if is_max:

        best=-math.inf

        for i in range(3):
            for j in range(3):

                if board[i][j]==" ":

                    board[i][j]="X"

                    score=minimax(board,depth+1,False)

                    board[i][j]=" "

                    best=max(best,score)

        return best


    else:

        best=math.inf

        for i in range(3):
            for j in range(3):

                if board[i][j]==" ":

                    board[i][j]="O"

                    score=minimax(board,depth+1,True)

                    board[i][j]=" "

                    best=min(best,score)

        return best


def best_move(board):

    best_score=-math.inf
    move=[0,0]

    for i in range(3):
        for j in range(3):

            if board[i][j]==" ":

                board[i][j]="X"

                score=minimax(board,0,False)

                board[i][j]=" "

                if score>best_score:

                    best_score=score
                    move=[i,j]

    return move


def handler(request):

    data = request.json()

    board = data["board"]

    move = best_move(board)

    return {
        "row":move[0],
        "col":move[1]
    }