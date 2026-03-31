import sqlite3

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            due_date TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending'
        )
    ''')
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN notified INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column already exists
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN notes TEXT")
        conn.execute("ALTER TABLE tasks ADD COLUMN image_path TEXT")
        conn.execute("ALTER TABLE tasks ADD COLUMN audio_path TEXT")
    except sqlite3.OperationalError:
        pass # Columns exist
    try:
        conn.execute("ALTER TABLE tasks ADD COLUMN completion_remark TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def add_task(description, due_date=None, priority='Medium', notes=None, image_path=None, audio_path=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (description, due_date, priority, status, notes, image_path, audio_path)
        VALUES (?, ?, ?, 'Pending', ?, ?, ?)
    ''', (description, due_date, priority, notes, image_path, audio_path))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks(status=None):
    conn = get_db_connection()
    if status is None:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    else:
        tasks = conn.execute('SELECT * FROM tasks WHERE status = ?', (status,)).fetchall()
    conn.close()
    return [dict(row) for row in tasks]

def mark_notified(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET notified = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def complete_task(task_id, remark=None):
    conn = get_db_connection()
    if remark:
        conn.execute('UPDATE tasks SET status = ?, completion_remark = ? WHERE id = ?', ('Completed', remark, task_id))
    else:
        conn.execute('UPDATE tasks SET status = ? WHERE id = ?', ('Completed', task_id))
    conn.commit()
    conn.close()

def edit_completion_remark(task_id, remark):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET completion_remark = ? WHERE id = ?', (remark, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def search_tasks(keyword):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE description LIKE ?', ('%' + keyword + '%',)).fetchall()
    conn.close()
    return [dict(row) for row in tasks]

def edit_task_media(task_id, notes=None, image_path=None, audio_path=None):
    conn = get_db_connection()
    fields = []
    values = []
    if notes is not None:
        fields.append("notes = ?")
        values.append(notes)
    if image_path is not None:
        fields.append("image_path = ?")
        values.append(image_path)
    if audio_path is not None:
        fields.append("audio_path = ?")
        values.append(audio_path)
        
    if not fields:
        return
        
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
    conn.execute(query, tuple(values))
    conn.commit()
    conn.close()

def edit_task(task_id, description=None, due_date=None, priority=None):
    conn = get_db_connection()
    fields = []
    values = []
    if description:
        fields.append("description = ?")
        values.append(description)
    if due_date:
        fields.append("due_date = ?")
        values.append(due_date)
    if priority:
        fields.append("priority = ?")
        values.append(priority)
        
    if not fields:
        return
        
    values.append(task_id)
    query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
    conn.execute(query, tuple(values))
    conn.commit()
    conn.close()

# Initialize the database file and schema when the module is imported
init_db()
