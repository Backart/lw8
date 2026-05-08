from datetime import datetime, timedelta
from src.models.task import TaskStatus

class TaskValidator:
    def is_title_valid(self, title) -> bool:
        if title is None: return False
        title = title.strip()
        return bool(title) and len(title) <= 100

    def is_due_date_valid(self, due_date) -> bool:
        if due_date is None: return False
        if due_date < datetime.utcnow(): return False
        if due_date > datetime.utcnow() + timedelta(days=730): return False
        return True

    def is_priority_valid(self, priority) -> bool:
        if priority is None: return False
        if not isinstance(priority, int): return False
        if priority < 1 or priority > 4: return False
        return True

    def is_valid_transition(self, from_status: TaskStatus, to_status: TaskStatus) -> bool:
        valid_transitions = {
            TaskStatus.TODO: [TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED],
            TaskStatus.IN_PROGRESS: [TaskStatus.REVIEW, TaskStatus.CANCELLED],
            TaskStatus.REVIEW: [TaskStatus.DONE, TaskStatus.IN_PROGRESS],
            TaskStatus.DONE: [TaskStatus.TODO],
            TaskStatus.CANCELLED: [TaskStatus.TODO]
        }
        return to_status in valid_transitions.get(from_status, [])
