from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sys
import pathlib

# Add solver paths
sys.path.append('./Waffle Solver')
sys.path.append('./Squaredle Solver')

from waffleSolver import WaffleSolver
from squaredleSolver import SquaredleSolver


print("app.py loaded!")

solver = None

app = Flask(__name__)

# ✅ Wide open CORS for testing (your extension will work)
CORS(app, supports_credentials=True)

# 🔒 If you want to lock down later to only your extension, use:
# CORS(app, resources={r"/*": {"origins": "chrome-extension://pbonfggjbpljbkjdnkljglooaihoeikc"}})


def getBoardFromHTML(tags, size):
    boardInfo = {}
    for tag in tags:
        tag = tag.split('"')
        letterInfo = tag[1][21:]
        position = tag[3]
        position = (int(position[15]), int(position[31]))

        if "green" in letterInfo:
            letterInfo = (letterInfo[0], 2)
        elif "yellow" in letterInfo:
            letterInfo = (letterInfo[0], 1)
        else:
            letterInfo = (letterInfo[0], 0)
        
        boardInfo[position] = letterInfo

    board = []

    if size == "daily":
        board.append([boardInfo[(x, 0)] for x in range(5)])
        board.append([boardInfo[(0, 1)], (" ", 3), boardInfo[(2, 1)], (" ", 3), boardInfo[(4, 1)]])
        board.append([boardInfo[(x, 2)] for x in range(5)])
        board.append([boardInfo[(0, 3)], (" ", 3), boardInfo[(2, 3)], (" ", 3), boardInfo[(4, 3)]])
        board.append([boardInfo[(x, 4)] for x in range(5)])

    elif size == "deluxe":
        board.append([boardInfo[(x, 0)] for x in range(7)])
        board.append([boardInfo[(0, 1)], (" ", 3), boardInfo[(2, 1)], (" ", 3), boardInfo[(4, 1)], (" ", 3), boardInfo[(6, 1)]])
        board.append([boardInfo[(x, 2)] for x in range(7)])
        board.append([boardInfo[(0, 3)], (" ", 3), boardInfo[(2, 3)], (" ", 3), boardInfo[(4, 3)], (" ", 3), boardInfo[(6, 3)]])
        board.append([boardInfo[(x, 4)] for x in range(7)])
        board.append([boardInfo[(0, 5)], (" ", 3), boardInfo[(2, 5)], (" ", 3), boardInfo[(4, 5)], (" ", 3), boardInfo[(6, 5)]])
        board.append([boardInfo[(x, 6)] for x in range(7)])

    return board


def getSimpleGrid(board):
    # returns a grid of just characters, no info about color
    simpleGrid = []
    for row in board:
        simpleGrid.append(tuple([letterInfo[0] for letterInfo in row]))
    return tuple(simpleGrid)


@app.route('/solveWaffle', methods=['POST'])
@cross_origin()  # ✅ Explicit CORS for this route
def solveWaffle():
    print("Answering Waffle Request")

    boardInfo = request.json.get('gameBoardHTML')
    divInfoList, swapsLeft = boardInfo
    swapsLeft = int(swapsLeft)
    print(f"{swapsLeft} swaps left")

    print(f"amount of tiles found: {len(divInfoList)}")
    if len(divInfoList) == 21:
        boardSize = "daily"
    elif len(divInfoList) == 40:
        boardSize = "deluxe"
    else:
        return jsonify({"error": "Invalid board size"}), 400

    board = getBoardFromHTML(divInfoList, boardSize)
    simpleGrid = getSimpleGrid(board)

    print(board)

    global solver
    if solver:
        if simpleGrid not in solver.nextSwaps:
            # regenerate swaps if puzzle changed
            solver = WaffleSolver(board, boardSize)
            solver.solve(True, swapsLeft)
    else:
        for row in board:
            print(row)
        print(boardSize)
        solver = WaffleSolver(board, boardSize)
        solver.solve(True, swapsLeft)

    if solver.failed:
        print("Solver failed")
        return jsonify({"failed": True})

    if simpleGrid == solver.simpleSolution:
        print("Finished, no need to get the next swap")
        return jsonify({"finished": True})
    
    nextSwap = solver.nextSwaps[simpleGrid]
    print(nextSwap)

    return jsonify({"nextSwap": nextSwap})


@app.route('/solveSquaredle', methods=['POST'])
@cross_origin()  # ✅ Explicit CORS for this route
def solveSquaredle():
    print("Answering Squaredle Request")

    board = request.json.get('gameBoard')
    print(board)

    solver = SquaredleSolver(board, debugMode=True)
    solver.findAllWords()

    formattedWords = [(wordStrand.word, wordStrand.indexes) for wordStrand in solver.wordStrands]
    print(formattedWords)

    return jsonify({"wordsList": formattedWords})


if __name__ == '__main__':
    app.run()
