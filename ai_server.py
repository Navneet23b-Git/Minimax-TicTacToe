import math
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


# -----------------------
# Game Logic
# -----------------------

def check_winner(board):

    for i in range(3):

        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]

        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None


def is_draw(board):

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False

    return True


# -----------------------
# Minimax AI
# -----------------------

def minimax(board, depth, is_maximizing):

    winner = check_winner(board)

    if winner == "X":
        return 10 - depth

    if winner == "O":
        return depth - 10

    if is_draw(board):
        return 0

    if is_maximizing:

        best_score = -math.inf

        for i in range(3):
            for j in range(3):

                if board[i][j] == " ":

                    board[i][j] = "X"

                    score = minimax(board, depth + 1, False)

                    board[i][j] = " "

                    best_score = max(best_score, score)

        return best_score

    else:

        best_score = math.inf

        for i in range(3):
            for j in range(3):

                if board[i][j] == " ":

                    board[i][j] = "O"

                    score = minimax(board, depth + 1, True)

                    board[i][j] = " "

                    best_score = min(best_score, score)

        return best_score


def best_move(board):

    best_score = -math.inf
    move = [0, 0]

    for i in range(3):
        for j in range(3):

            if board[i][j] == " ":

                board[i][j] = "X"

                score = minimax(board, 0, False)

                board[i][j] = " "

                if score > best_score:

                    best_score = score
                    move = [i, j]

    return move


# -----------------------
# Probability Calculation
# -----------------------

def simulate_outcomes(board, player):

    winner = check_winner(board)

    if winner == "X":
        return (1, 0, 0)

    if winner == "O":
        return (0, 1, 0)

    if is_draw(board):
        return (0, 0, 1)

    x_wins = 0
    o_wins = 0
    draws = 0

    for i in range(3):
        for j in range(3):

            if board[i][j] == " ":

                board[i][j] = player

                next_player = "O" if player == "X" else "X"

                x, o, d = simulate_outcomes(board, next_player)

                x_wins += x
                o_wins += o
                draws += d

                board[i][j] = " "

    return (x_wins, o_wins, draws)


def calculate_probabilities(board):

    x, o, d = simulate_outcomes(board, "X")

    total = x + o + d

    if total == 0:
        return 0, 0, 0

    x_prob = round((x / total) * 100, 2)
    o_prob = round((o / total) * 100, 2)
    draw_prob = round((d / total) * 100, 2)

    return x_prob, o_prob, draw_prob


# -----------------------
# HTTP Server
# -----------------------

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":

            with open("index.html") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(content.encode())


        elif self.path == "/style.css":

            with open("style.css") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()

            self.wfile.write(content.encode())


        elif self.path == "/script.js":

            with open("script.js") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()

            self.wfile.write(content.encode())


    def do_POST(self):

        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)

        data = json.loads(body)

        board = data["board"]

        move = best_move(board)

        board[move[0]][move[1]] = "X"

        x_prob, o_prob, draw_prob = calculate_probabilities(board)

        response = {
            "row": move[0],
            "col": move[1],
            "x_prob": x_prob,
            "o_prob": o_prob,
            "draw_prob": draw_prob
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


# -----------------------
# Start Server
# -----------------------

PORT = 8000

server = HTTPServer(("localhost", PORT), Handler)

print(f"Server running at http://localhost:{PORT}")

webbrowser.open(f"http://localhost:{PORT}")

server.serve_forever()