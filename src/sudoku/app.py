from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import logging
import sys
import os
from .generator import SudokuGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

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
    
    logger.info(f"Received generation request: Difficulty={difficulty}, Count={count}")
    
    def generate_stream():
        for i in range(count):
            try:
                board, grade, solution = generator.generate(difficulty)
                # Yield progress and the puzzle data
                response_data = {
                    'progress': i + 1,
                    'total': count,
                    'puzzle': {
                        'board': board,
                        'grade': grade,
                        'solution': solution
                    }
                }
                yield json.dumps(response_data) + '\n'
            except Exception as e:
                logger.error(f"Error generating puzzle {i+1}/{count}: {str(e)}", exc_info=True)
                yield json.dumps({'error': str(e)}) + '\n'

    return Response(stream_with_context(generate_stream()), mimetype='application/x-ndjson')

def run():
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Sudoku Generator on port {port}, debug={debug}")
    app.run(debug=debug, host='0.0.0.0', port=port)

if __name__ == "__main__":
    run()
