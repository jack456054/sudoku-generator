from flask import Flask, render_template, request, jsonify
from .generator import SudokuGenerator

app = Flask(__name__)
generator = SudokuGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    difficulty = data.get('difficulty', 'Simple')
    count = int(data.get('count', 1))
    
    puzzles = []
    for _ in range(count):
        board, grade, solution = generator.generate(difficulty)
        puzzles.append({
            'board': board,
            'grade': grade,
            'solution': solution
        })
        
    return jsonify({'puzzles': puzzles})

def run():
    app.run(debug=True, port=5001)

if __name__ == "__main__":
    run()
