from flask import Flask, jsonify
import sys
sys.path.append('./Waffle Solver')
from waffleSolver import WaffleSolver

app = Flask(__name__)

@app.route('/get_hint')
def get_hint():
    # Implement logic to get hints based on the active game
    hint = waffleSolver()  # Replace with the appropriate game-solving function
    hint.solve()
    return jsonify({'hint': hint})

@app.route('/solve_puzzle')
def solve_puzzle():
    # Implement logic to solve the puzzle based on the active game
    solution = waffleSolver()  # Replace with the appropriate game-solving function
    solution.solve()
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)
