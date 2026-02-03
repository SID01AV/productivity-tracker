from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, EmailStr


# User schemas


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class TokenData(BaseModel):
    user_id: Optional[int] = None


# Task & logs


class TaskRead(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    points: int
    is_active: bool

    class Config:
        from_attributes = True


class DailyTaskLogBase(BaseModel):
    task_id: int
    date: date
    completed: bool


class DailyTaskLogCreate(DailyTaskLogBase):
    pass


class DailyTaskLogRead(BaseModel):
    id: int
    task: TaskRead
    date: date
    completed: bool
    points_awarded: int

    class Config:
        from_attributes = True


class DailyTaskWithStatus(BaseModel):
    task: TaskRead
    date: date
    completed: bool
    points_awarded: int


# Friends & leaderboard


class FriendRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class FriendshipRead(BaseModel):
    id: int
    friend: FriendRead
    created_at: datetime

    class Config:
        from_attributes = True


class FriendshipCreate(BaseModel):
    friend_username: str


class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    total_points: int


# Stats


class StatsByDate(BaseModel):
    date: date
    points: int


class StatsSummary(BaseModel):
    range: Literal["daily", "weekly", "monthly"]
    start_date: date
    end_date: date
    total_points: int
    by_date: List[StatsByDate]

