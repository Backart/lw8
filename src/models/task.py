from dataclasses import dataclass
from typing import Optional
from enum import Enum
from uuid import UUID, uuid4


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Task:
    title: str
    priority: int
    due_date: Optional[object] = None
    creator_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None
    status: TaskStatus = TaskStatus.TODO
    id: UUID = None

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
