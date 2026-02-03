from datetime import date as date_type, timedelta
from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


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
    # default to weekly if unknown
    start = ref_date - timedelta(days=ref_date.weekday())
    end = start + timedelta(days=6)
    return start, end


@router.get("", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(
    range: str = "weekly",
    for_date: Optional[date_type] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    ref_date = for_date or date_type.today()
    start_date, end_date = _get_range_dates(range, ref_date)

    friend_ids_subq = (
        db.query(models.Friendship.friend_id)
        .filter(models.Friendship.user_id == current_user.id)
        .subquery()
    )

    user_ids = [current_user.id]
    # We will use subquery directly in filter; no need to materialize user_ids list.

    points_query = (
        db.query(
            models.User.id.label("user_id"),
            models.User.username,
            func.coalesce(func.sum(models.DailyTaskLog.points_awarded), 0).label(
                "total_points"
            ),
        )
        .outerjoin(
            models.DailyTaskLog,
            (models.DailyTaskLog.user_id == models.User.id)
            & (models.DailyTaskLog.date >= start_date)
            & (models.DailyTaskLog.date <= end_date),
        )
        .filter(
            (models.User.id == current_user.id)
            | (models.User.id.in_(friend_ids_subq))
        )
        .group_by(models.User.id)
        .order_by(func.coalesce(func.sum(models.DailyTaskLog.points_awarded), 0).desc())
    )

    rows = points_query.all()
    return [
        schemas.LeaderboardEntry(
            user_id=row.user_id, username=row.username, total_points=row.total_points
        )
        for row in rows
    ]

