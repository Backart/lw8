"""
Module for legacy task management service.
Provides repository and service for task operations.
"""

import datetime
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Optional


class TaskStatus(IntEnum):
    """Enumeration of possible task statuses."""

    TODO = 0
    IN_PROGRESS = 1
    DONE = 2


@dataclass
class Task:
    """Data class representing a single Task entity."""

    title: str
    user: str
    priority: int = 3
    status: TaskStatus = TaskStatus.TODO
    task_id: int = field(default=0)
    created: datetime.datetime = field(default_factory=datetime.datetime.now)


class TaskRepository:
    """Repository for storing and retrieving tasks in memory."""

    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add(self, task: Task) -> None:
        """Adds a new task to the repository."""
        task.task_id = len(self._tasks) + 1
        self._tasks.append(task)

    def get_all(self) -> List[Task]:
        """Returns all tasks."""
        return self._tasks

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Finds a task by its unique ID."""
        return next((t for t in self._tasks if t.task_id == task_id), None)


class TaskService:
    """Service for high-level task operations."""

    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo

    def create_task(self, title: str, user_email: str) -> Optional[Task]:
        """Creates a new task."""
        if not title or len(title) > 100:
            return None
        task = Task(title=title, user=user_email)
        self.repo.add(task)
        return task

    def assign_task(self, task_id: int, user_email: str) -> Optional[Task]:
        """Assigns a task to a user."""
        task = self.repo.find_by_id(task_id)
        if task:
            task.user = user_email
            task.status = TaskStatus.IN_PROGRESS
            return task
        return None


x = 1
