from src.models.task import Task, TaskStatus
from uuid import UUID
from typing import Optional


class TaskService:
    def __init__(self, task_repo, notifier):
        self.task_repo = task_repo
        self.notifier = notifier

    def create_task(
        self, title: str, priority: int, due_date: Optional[object], creator_id: UUID
    ) -> Task:
        if not title:
            raise ValueError("Title cannot be empty")

        task = Task(title=title, priority=priority, due_date=due_date, creator_id=creator_id)
        self.task_repo.save(task)
        return task

    def assign_task(self, task_id: UUID, assignee_id: UUID) -> Task:
        task = self.task_repo.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.assignee_id = assignee_id
        self.task_repo.save(task)
        self.notifier.send(recipient_id=assignee_id, message="Task assigned")
        return task

    def get_tasks_by_assignee(self, assignee_id: UUID) -> list[Task]:
        return self.task_repo.find_by_assignee(assignee_id)

    def change_status(self, task_id: UUID, new_status: TaskStatus) -> Task:
        task = self.task_repo.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.status = new_status
        self.task_repo.save(task)
        self.notifier.send(recipient_id="system", message=f"Status changed to {new_status}")
        return task
