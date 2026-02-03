from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/daily-logs", tags=["daily-logs"])


@router.post("", response_model=schemas.DailyTaskLogRead)
def upsert_daily_log(
    log_in: schemas.DailyTaskLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == log_in.task_id).first()
    if not task or not task.is_active:
        raise HTTPException(status_code=404, detail="Task not found")

    log = (
        db.query(models.DailyTaskLog)
        .filter(
            models.DailyTaskLog.user_id == current_user.id,
            models.DailyTaskLog.task_id == log_in.task_id,
            models.DailyTaskLog.date == log_in.date,
        )
        .first()
    )

    points_awarded = task.points if log_in.completed else 0

    if log:
        log.completed = log_in.completed
        log.points_awarded = points_awarded
    else:
        log = models.DailyTaskLog(
            user_id=current_user.id,
            task_id=log_in.task_id,
            date=log_in.date,
            completed=log_in.completed,
            points_awarded=points_awarded,
        )
        db.add(log)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not save log")

    db.refresh(log)
    return log

