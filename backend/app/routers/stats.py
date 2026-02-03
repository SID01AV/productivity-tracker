from datetime import date as date_type, timedelta
from typing import Optional, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/stats", tags=["stats"])


def _get_range_dates(
    range_type: str, ref_date: date_type
) -> Tuple[date_type, date_type]:
    if range_type == "daily":
        return ref_date, ref_date
    if range_type == "weekly":
        start = ref_date - timedelta(days=ref_date.weekday())
        end = start + timedelta(days=6)
        return start, end
    if range_type == "monthly":
        start = ref_date.replace(day=1)
        if start.month == 12:
            next_month = start.replace(year=start.year + 1, month=1, day=1)
        else:
            next_month = start.replace(month=start.month + 1, day=1)
        end = next_month - timedelta(days=1)
        return start, end
    # default weekly
    start = ref_date - timedelta(days=ref_date.weekday())
    end = start + timedelta(days=6)
    return start, end


@router.get("/summary", response_model=schemas.StatsSummary)
def get_stats_summary(
    range: str = "weekly",
    for_date: Optional[date_type] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    ref_date = for_date or date_type.today()
    start_date, end_date = _get_range_dates(range, ref_date)

    total_points = (
        db.query(func.coalesce(func.sum(models.DailyTaskLog.points_awarded), 0))
        .filter(
            models.DailyTaskLog.user_id == current_user.id,
            models.DailyTaskLog.date >= start_date,
            models.DailyTaskLog.date <= end_date,
        )
        .scalar()
    )

    by_date_rows = (
        db.query(
            models.DailyTaskLog.date,
            func.coalesce(func.sum(models.DailyTaskLog.points_awarded), 0).label(
                "points"
            ),
        )
        .filter(
            models.DailyTaskLog.user_id == current_user.id,
            models.DailyTaskLog.date >= start_date,
            models.DailyTaskLog.date <= end_date,
        )
        .group_by(models.DailyTaskLog.date)
        .order_by(models.DailyTaskLog.date)
        .all()
    )

    by_date = [
        schemas.StatsByDate(date=row.date, points=row.points) for row in by_date_rows
    ]

    return schemas.StatsSummary(
        range=range,  # type: ignore[arg-type]
        start_date=start_date,
        end_date=end_date,
        total_points=total_points or 0,
        by_date=by_date,
    )

