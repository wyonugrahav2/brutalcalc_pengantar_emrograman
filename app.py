# -*- coding: utf-8 -*-
import os
import sys

# Memastikan Vercel bisa membaca folder 'utils' di server mereka
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from utils.arithmetic import calculate_arithmetic
from utils.logic import calculate_logic
from utils.transform import calculate_transform
from utils.history import get_history, add_history, clear_history

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Ekspos 'app' sebagai 'application' untuk kebutuhan Vercel Serverless
application = app

# ─── PAGE ROUTES ───────────────────────────────────────────────
@app.route('/')
@app.route('/arithmetic')
def arithmetic():
    return render_template('arithmetic.html')

@app.route('/logic')
def logic():
    return render_template('logic.html')

@app.route('/transform')
def transform():
    return render_template('transform.html')

@app.route('/history')
def history():
    return render_template('history.html')

# ─── API ROUTES ────────────────────────────────────────────────
@app.route('/api/arithmetic', methods=['POST'])
def api_arithmetic():
    data = request.get_json()
    result = calculate_arithmetic(data)
    if result.get('success'):
        add_history({
            'category': 'ARITHMETIC',
            'operation': data.get('operation', '').upper(),
            'formula': result.get('formula', ''),
            'result': str(result.get('result', ''))
        })
    return jsonify(result)

@app.route('/api/logic', methods=['POST'])
def api_logic():
    data = request.get_json()
    result = calculate_logic(data)
    if result.get('success'):
        add_history({
            'category': 'LOGIC',
            'operation': data.get('operation', '').upper(),
            'formula': result.get('formula', ''),
            'result': str(result.get('result', ''))
        })
    return jsonify(result)

@app.route('/api/transform', methods=['POST'])
def api_transform():
    data = request.get_json()
    result = calculate_transform(data)
    if result.get('success'):
        add_history({
            'category': 'TRANSFORM',
            'operation': data.get('type', '').upper(),
            'formula': result.get('formula', ''),
            'result': str(result.get('result', ''))
        })
    return jsonify(result)

@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(get_history())

@app.route('/api/history/clear', methods=['POST'])
def api_history_clear():
    clear_history()
    return jsonify({'success': True, 'message': 'HISTORY CLEARED'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)