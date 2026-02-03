from sqlalchemy.orm import Session

from . import models
from .database import Base, engine


def init_db() -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed default tasks if not present
    from .database import SessionLocal

    db: Session = SessionLocal()
    try:
        existing = db.query(models.Task).count()
        if existing == 0:
            tasks = [
                models.Task(
                    name="Wake up on time",
                    code="wake_up",
                    description="Wake up at your planned time",
                    points=10,
                ),
                models.Task(
                    name="2 hours work/study",
                    code="work_2h",
                    description="Focus on work or study for at least 2 hours",
                    points=20,
                ),
                models.Task(
                    name="30 min workout",
                    code="workout_30m",
                    description="Do at least 30 minutes of exercise",
                    points=15,
                ),
            ]
            db.add_all(tasks)
            db.commit()
    finally:
        db.close()

