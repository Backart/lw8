"""TMS API Module."""

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TMS API", version="1.0.0")


class TaskCreate(BaseModel):
    """Schema for creating a task."""

    title: str
    user: str


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "TMS",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }


@app.get("/tasks")
def get_tasks():
    """Get all tasks endpoint."""
    return {"tasks": [], "total": 0}


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Create a new task endpoint."""
    return {"message": "Task created successfully", "task": task.model_dump()}
