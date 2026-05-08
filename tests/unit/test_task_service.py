import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from src.services.task_service import TaskService
from src.models.task import Task

class TestTaskServiceCreateTask:
    def test_create_task_happy_path(self):
        # ARRANGE
        mock_repo = MagicMock()
        mock_notifier = MagicMock()
        service = TaskService(task_repo=mock_repo, notifier=mock_notifier)
        
        # ACT
        task = service.create_task('Test Task', 1, None, uuid4())
        
        # ASSERT
        assert task.title == 'Test Task'
        assert task.priority == 1

    def test_create_task_edge_case_empty_title(self):
        mock_repo = MagicMock()
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        
        with pytest.raises(ValueError, match="Title cannot be empty"):
            service.create_task('', 1, None, uuid4())

    def test_create_task_mock_verification(self):
        mock_repo = MagicMock()
        mock_notifier = MagicMock()
        service = TaskService(task_repo=mock_repo, notifier=mock_notifier)
        
        task = service.create_task('Test Task', 1, None, uuid4())
        
        # Перевіряємо, що репозиторій викликав метод save [cite: 177]
        mock_repo.save.assert_called_once_with(task)
        # При створенні сповіщення не надсилається [cite: 178]
        mock_notifier.send.assert_not_called()

    def test_assign_task_happy_path(self):
        mock_repo = MagicMock()
        task_id = uuid4()
        assignee_id = uuid4()
        
        # Налаштовуємо Stub: повертаємо фейкову задачу при пошуку [cite: 151, 152]
        fake_task = Task(title='To Assign', priority=1, id=task_id)
        mock_repo.find_by_id.return_value = fake_task
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        updated_task = service.assign_task(task_id, assignee_id)
        
        assert updated_task.assignee_id == assignee_id

    def test_assign_task_edge_case_not_found(self):
        mock_repo = MagicMock()
        # Задача не знайдена [cite: 162, 163]
        mock_repo.find_by_id.return_value = None 
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        
        with pytest.raises(ValueError, match="Task not found"):
            service.assign_task(uuid4(), uuid4())

    def test_assign_task_mock_verification(self):
        mock_repo = MagicMock()
        mock_notifier = MagicMock()
        task_id = uuid4()
        assignee_id = uuid4()
        
        fake_task = Task(title='To Assign', priority=1, id=task_id)
        mock_repo.find_by_id.return_value = fake_task
        
        service = TaskService(task_repo=mock_repo, notifier=mock_notifier)
        service.assign_task(task_id, assignee_id)
        
        # Перевіряємо виклик збереження і сповіщення [cite: 156, 157, 395]
        mock_repo.save.assert_called_once_with(fake_task)
        mock_notifier.send.assert_called_once()

    def test_get_tasks_by_assignee_happy_path(self):
        mock_repo = MagicMock()
        assignee_id = uuid4()
        fake_tasks = [Task(title='T1', priority=1), Task(title='T2', priority=2)]
        mock_repo.find_by_assignee.return_value = fake_tasks
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        tasks = service.get_tasks_by_assignee(assignee_id)
        
        assert len(tasks) == 2
        assert tasks == fake_tasks

    def test_get_tasks_by_assignee_edge_case_empty(self):
        mock_repo = MagicMock()
        mock_repo.find_by_assignee.return_value = []
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        tasks = service.get_tasks_by_assignee(uuid4())
        
        assert tasks == []

    def test_get_tasks_by_assignee_mock_verification(self):
        mock_repo = MagicMock()
        assignee_id = uuid4()
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        service.get_tasks_by_assignee(assignee_id)
        
        mock_repo.find_by_assignee.assert_called_once_with(assignee_id)

    def test_change_status_happy_path(self):
        from src.models.task import TaskStatus
        mock_repo = MagicMock()
        task_id = uuid4()
        fake_task = Task(title='T1', priority=1, id=task_id)
        mock_repo.find_by_id.return_value = fake_task
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        updated_task = service.change_status(task_id, TaskStatus.DONE)
        
        assert updated_task.status == TaskStatus.DONE

    def test_change_status_edge_case_not_found(self):
        from src.models.task import TaskStatus
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = None
        
        service = TaskService(task_repo=mock_repo, notifier=MagicMock())
        
        with pytest.raises(ValueError, match="Task not found"):
            service.change_status(uuid4(), TaskStatus.DONE)

    def test_change_status_mock_verification(self):
        from src.models.task import TaskStatus
        mock_repo = MagicMock()
        mock_notifier = MagicMock()
        task_id = uuid4()
        fake_task = Task(title='T1', priority=1, id=task_id)
        mock_repo.find_by_id.return_value = fake_task
        
        service = TaskService(task_repo=mock_repo, notifier=mock_notifier)
        service.change_status(task_id, TaskStatus.DONE)
        
        mock_repo.save.assert_called_once_with(fake_task)
        mock_notifier.send.assert_called_once()
