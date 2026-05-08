from src.validators.task_validator import TaskValidator

def test_title_cannot_be_empty():
    validator = TaskValidator()
    assert validator.is_title_valid('') == False

def test_title_cannot_be_whitespace_only():
    validator = TaskValidator()
    assert validator.is_title_valid('   ') == False

def test_title_cannot_exceed_100_chars():
    validator = TaskValidator()
    # 101 символ має повертати False
    assert validator.is_title_valid('a' * 101) == False
from datetime import datetime, timedelta

def test_due_date_cannot_be_none():
    validator = TaskValidator()
    assert validator.is_due_date_valid(None) == False

def test_due_date_cannot_be_in_the_past():
    validator = TaskValidator()
    past_date = datetime.utcnow() - timedelta(days=1)
    assert validator.is_due_date_valid(past_date) == False

def test_due_date_cannot_be_more_than_2_years_ahead():
    validator = TaskValidator()
    # Ставимо дату на 3 роки (365 * 3 днів) вперед
    future_date = datetime.utcnow() + timedelta(days=1095)
    assert validator.is_due_date_valid(future_date) == False

def test_priority_cannot_be_none():
    validator = TaskValidator()
    assert validator.is_priority_valid(None) == False

def test_priority_must_be_integer_between_1_and_4():
    validator = TaskValidator()
    # Поза межами
    assert validator.is_priority_valid(0) == False
    assert validator.is_priority_valid(5) == False
    # Неціле число
    assert validator.is_priority_valid(2.5) == False
