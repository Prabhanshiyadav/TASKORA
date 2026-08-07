import sqlite3
import os
from datetime import datetime

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "taskora.db")

class Task:
    def __init__(self, task_id, title, priority="Medium", status="Pending", 
                 due_date="No Date", category="General", tags=None, 
                 notes="", estimated_time=1, subtasks=None, comments=None, created_at=None):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.category = category
        self.tags = tags or ["#General"]
        self.notes = notes
        self.estimated_time = estimated_time
        self.subtasks = subtasks or []
        self.comments = comments or []
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "category": self.category,
            "tags": ", ".join(self.tags) if isinstance(self.tags, list) else self.tags,
            "notes": self.notes,
            "estimated_time": f"{self.estimated_time} hrs",
            "created_at": self.created_at
        }

class TaskManager:
    def __init__(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(DB_FILE)

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority TEXT,
                    status TEXT,
                    due_date TEXT,
                    category TEXT,
                    tags TEXT,
                    notes TEXT,
                    estimated_time INTEGER,
                    created_at TEXT
                )
            """)
            conn.commit()

    @property
    def tasks(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, priority, status, due_date, category, tags, notes, estimated_time, created_at FROM tasks")
            rows = cursor.fetchall()
            result = []
            for r in rows:
                tags_list = r[6].split(",") if r[6] else ["#General"]
                result.append(Task(
                    task_id=r[0], title=r[1], priority=r[2], status=r[3],
                    due_date=r[4], category=r[5], tags=tags_list, notes=r[7],
                    estimated_time=r[8], created_at=r[9]
                ))
            return result

    def add_task(self, title, priority, due_date, category, tags, notes, estimated_time):
        tags_str = ",".join(tags) if isinstance(tags, list) else tags
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO tasks (title, priority, status, due_date, category, tags, notes, estimated_time, created_at)
                VALUES (?, ?, 'Pending', ?, ?, ?, ?, ?, ?)
            """, (title, priority, str(due_date), category, tags_str, notes, estimated_time, created_at))
            conn.commit()

    def update_task(self, task_id, new_title, new_priority, new_status, new_category, new_notes):
        with self.get_connection() as conn:
            if new_title:
                conn.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
            if new_priority:
                conn.execute("UPDATE tasks SET priority = ? WHERE id = ?", (new_priority, task_id))
            if new_status:
                conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
            if new_category:
                conn.execute("UPDATE tasks SET category = ? WHERE id = ?", (new_category, task_id))
            if new_notes:
                conn.execute("UPDATE tasks SET notes = ? WHERE id = ?", (new_notes, task_id))
            conn.commit()

    def delete_task(self, task_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

    def get_stats(self):
        all_tasks = self.tasks
        total = len(all_tasks)
        completed = sum(1 for t in all_tasks if t.status == "Done")
        pending = total - completed
        high_priority = sum(1 for t in all_tasks if t.priority == "High")
        score = int((completed / total) * 100) if total > 0 else 0
        return total, completed, pending, high_priority, score