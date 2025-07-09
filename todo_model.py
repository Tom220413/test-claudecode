import sqlite3
import os


class TodoModel:
    def __init__(self, db_path='todo.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_item(self, text):
        if text is None or not text or not text.strip():
            raise ValueError("Todo text cannot be empty")
        if len(text) > 200:
            raise ValueError("Todo text cannot exceed 200 characters")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (text) VALUES (?)', (text,))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def get_all_items(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, text, completed FROM todos ORDER BY id')
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            items.append({
                'id': row[0],
                'text': row[1],
                'completed': bool(row[2])
            })
        return items
    
    def toggle_completion(self, item_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET completed = NOT completed WHERE id = ?', (item_id,))
        if cursor.rowcount == 0:
            conn.close()
            raise ValueError(f"Todo item with ID {item_id} not found")
        conn.commit()
        conn.close()