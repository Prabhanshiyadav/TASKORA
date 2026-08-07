from datetime import datetime

class Task:
    def __init__(self, task_id, title, priority="Medium", status="Pending", 
                 due_date="No Date", category="General", tags=None, 
                 notes="", estimated_time=1, comments=None, created_at=None):
        self.id = task_id
        self.title = title
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.category = category
        self.tags = tags or ["#General"]
        self.notes = notes
        self.estimated_time = estimated_time
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
            "tags": ", ".join(self.tags),
            "notes": self.notes,
            "estimated_time": f"{self.estimated_time} hrs",
            "comments_count": len(self.comments),
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        tags_raw = data.get("tags", "#General")
        tags = [t.strip() for t in tags_raw.split(",")] if isinstance(tags_raw, str) else tags_raw
        est = data.get("estimated_time", "1 hrs")
        if isinstance(est, str):
            est = int(''.join(filter(str.isdigit, est)) or 1)
        return cls(
            task_id=data["id"],
            title=data["title"],
            priority=data.get("priority", "Medium"),
            status=data.get("status", "Pending"),
            due_date=data.get("due_date", "No Date"),
            category=data.get("category", "General"),
            tags=tags,
            notes=data.get("notes", ""),
            estimated_time=est,
            comments=data.get("comments", []),
            created_at=data.get("created_at")
        )