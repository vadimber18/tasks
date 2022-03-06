import pytest

from app.models import Task


def test_task():
    assert Task(id=1, processing_time=5)
    with pytest.raises(ValueError):
        Task(id=1, processing_time=13)
