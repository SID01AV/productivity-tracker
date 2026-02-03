from datetime import date as date_type
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[schemas.TaskRead])
def list_tasks(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Task)
    if not include_inactive:
        query = query.filter(models.Task.is_active.is_(True))
    return query.order_by(models.Task.id).all()


@router.get("/daily", response_model=List[schemas.DailyTaskWithStatus])
def get_daily_tasks(
    for_date: Optional[date_type] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    target_date = for_date or date_type.today()

    tasks = (
        db.query(models.Task)
        .filter(models.Task.is_active.is_(True))
        .order_by(models.Task.id)
        .all()
    )

    logs = (
        db.query(models.DailyTaskLog)
        .filter(
            models.DailyTaskLog.user_id == current_user.id,
            models.DailyTaskLog.date == target_date,
        )
        .all()
    )
    logs_by_task_id = {log.task_id: log for log in logs}

    result: List[schemas.DailyTaskWithStatus] = []
    for task in tasks:
        log = logs_by_task_id.get(task.id)
        completed = log.completed if log else False
        points_awarded = log.points_awarded if log else 0
        result.append(
            schemas.DailyTaskWithStatus(
                task=schemas.TaskRead.from_orm(task),
                date=target_date,
                completed=completed,
                points_awarded=points_awarded,
            )
        )
    return result

