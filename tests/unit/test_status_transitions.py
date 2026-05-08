import pytest
from src.models.task import TaskStatus
from src.validators.task_validator import TaskValidator

@pytest.mark.parametrize("from_status, to_status, expected", [
    # З TODO
    (TaskStatus.TODO, TaskStatus.TODO, False),
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS, True),
    (TaskStatus.TODO, TaskStatus.REVIEW, False),
    (TaskStatus.TODO, TaskStatus.DONE, False),
    (TaskStatus.TODO, TaskStatus.CANCELLED, True),
    # З IN_PROGRESS
    (TaskStatus.IN_PROGRESS, TaskStatus.TODO, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.REVIEW, True),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE, False),
    (TaskStatus.IN_PROGRESS, TaskStatus.CANCELLED, True),
    # З REVIEW
    (TaskStatus.REVIEW, TaskStatus.TODO, False),
    (TaskStatus.REVIEW, TaskStatus.IN_PROGRESS, True),
    (TaskStatus.REVIEW, TaskStatus.REVIEW, False),
    (TaskStatus.REVIEW, TaskStatus.DONE, True),
    (TaskStatus.REVIEW, TaskStatus.CANCELLED, False),
    # З DONE
    (TaskStatus.DONE, TaskStatus.TODO, True),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS, False),
    (TaskStatus.DONE, TaskStatus.REVIEW, False),
    (TaskStatus.DONE, TaskStatus.DONE, False),
    (TaskStatus.DONE, TaskStatus.CANCELLED, False),
    # З CANCELLED
    (TaskStatus.CANCELLED, TaskStatus.TODO, True),
    (TaskStatus.CANCELLED, TaskStatus.IN_PROGRESS, False),
    (TaskStatus.CANCELLED, TaskStatus.REVIEW, False),
    (TaskStatus.CANCELLED, TaskStatus.DONE, False),
    (TaskStatus.CANCELLED, TaskStatus.CANCELLED, False),
])
def test_status_transitions(from_status, to_status, expected):
    validator = TaskValidator()
    assert validator.is_valid_transition(from_status, to_status) == expected
