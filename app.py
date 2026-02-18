from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static')
DB_PATH = '/data/notes.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs('/data', exist_ok=True)
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/notes', methods=['GET', 'POST', 'DELETE'])
def notes():
    conn = get_db()
    
    if request.method == 'GET':
        rows = conn.execute('SELECT * FROM notes ORDER BY created_at DESC').fetchall()
        return jsonify([dict(r) for r in rows])
    
    elif request.method == 'POST':
        data = request.json
        content = data.get('content', '').strip()
        if not content:
            return jsonify({'error': 'Content required'}), 400
        cursor = conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        row = conn.execute('SELECT * FROM notes WHERE id = ?', (cursor.lastrowid,)).fetchone()
        return jsonify(dict(row)), 201
    
    elif request.method == 'DELETE':
        note_id = request.args.get('id')
        if not note_id:
            return jsonify({'error': 'ID required'}), 400
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
