from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import os

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def tie(board):
    # Returns false if board contains None values and True if all squares on board is full
    
    for row in board:
        if None in row:
            return False
    return True

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    if "moves" not in session:
        session["moves"] = []

    return render_template("game.html", game=session["board"], turn=session["turn"], moves=session["moves"])


@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    turn = session["turn"]

    if turn == "X":
        #Play X
        session["board"][row][col] = "X"
        session["turn"] = "O"

        #Save to history
        session["moves"].append([row,col, turn])
    else:
        #Play O
        session["board"][row][col] = "O"
        session["turn"] = "X"

        #Save to history
        session["moves"].append([row,col, turn])

    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():

    if session["board"]:
        session.pop("board")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.context_processor
def winner():
        
    # Columns
    left = [ session["board"][0][0], session["board"][1][0], session["board"][2][0] ]
    middle = [ session["board"][0][1], session["board"][1][1], session["board"][2][1] ]
    right = [ session["board"][0][2], session["board"][1][2], session["board"][2][2] ]
    
    # Rows
    top_row = [ session["board"][0][0], session["board"][0][1], session["board"][0][2] ]
    middle_row = [ session["board"][1][0], session["board"][1][1], session["board"][1][2] ]
    bottom_row = [ session["board"][2][0], session["board"][2][1], session["board"][2][2] ]
    
    # Horizontal  = \ and /
    horizontal1 = [ session["board"][0][0], session["board"][1][1], session["board"][2][2] ]
    horizontal2 = [ session["board"][0][2], session["board"][1][1], session["board"][2][0] ]
    
    check = left, middle, right, horizontal1, horizontal2, top_row, middle_row, bottom_row

    for i in check:
        if i == ["X", "X", "X"]:
            return dict(winner="X")
        
        if i == ["O", "O", "O"]:
            return dict(winner="O")
                
    full_board = tie(session["board"])
    
    # Returns empty string if board is not full
    if not full_board:
        return dict(winner="")

    # If all squares have values and nobody has won, it is a tie
    return dict(winner="Tie!")
    

# Undo move
@app.route("/undo", methods = ["POST"])
def undo():
    
    if "moves" in session:
        try:
                # Coordinates
                move = session["moves"][-1]

                x = move[0]
                y = move[1]
                turn = move[2]
            
                # Remove from board at specified position
                session["board"][x][y] = None 
                session["turn"] = turn

                # Remove last move from history
                session["moves"].pop(-1)
            
        
        except IndexError:
            return redirect(url_for("index"))        
    
    return redirect(url_for("index"))    