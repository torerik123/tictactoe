from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    if session["turn"] == "X":
        session["board"][row][col] = "X"
        session["turn"] = "O"    
    
    else:
        session["board"][row][col] = "O"
        session["turn"] = "X"

    return redirect(url_for("index"))


@app.route("/reset", methods=["POST"])
def reset():

    if session["board"]:
        session.pop("board")
    
        return redirect(url_for("index"))


@app.context_processor
def winner():
        
    # Columns
    left = [ session["board"][0][0], session["board"][1][0], session["board"][2][0] ]
    middle = [ session["board"][0][1], session["board"][1][1], session["board"][2][1] ]
    right = [ session["board"][0][2], session["board"][1][2], session["board"][2][2] ]
    
    columns = left, middle, right
    
    for i in columns:
        if i == ["X", "X", "X"]:
            return dict(winner="X is the winner")
        
        if i == ["O", "O", "O"]:
            return dict(winner="O is the winner")
    
    # Rows
    for row in session["board"]:
        
        if row == ["X", "X", "X"]:
            return dict(winner='X is the winner')

        if row == ["O", "O", "O"]:
            return dict(winner='O is the winner')
                
    # TODO: Horizontal wins and tie 

    return dict(winner=str(columns))