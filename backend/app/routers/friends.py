from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import auth, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/friends", tags=["friends"])


@router.get("", response_model=List[schemas.FriendshipRead])
def list_friends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    friendships = (
        db.query(models.Friendship)
        .filter(models.Friendship.user_id == current_user.id)
        .join(models.Friendship.friend)
        .order_by(models.User.username)
        .all()
    )

    result: List[schemas.FriendshipRead] = []
    for fs in friendships:
        friend = schemas.FriendRead.from_orm(fs.friend)
        result.append(
            schemas.FriendshipRead(
                id=fs.id,
                friend=friend,
                created_at=fs.created_at,
            )
        )
    return result


@router.post("", response_model=schemas.FriendshipRead)
def add_friend(
    friendship_in: schemas.FriendshipCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    friend = (
        db.query(models.User)
        .filter(models.User.username == friendship_in.friend_username)
        .first()
    )
    if not friend:
        raise HTTPException(status_code=404, detail="Friend user not found")
    if friend.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot add yourself as a friend")

    existing = (
        db.query(models.Friendship)
        .filter(
            models.Friendship.user_id == current_user.id,
            models.Friendship.friend_id == friend.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Friendship already exists")

    friendship = models.Friendship(user_id=current_user.id, friend_id=friend.id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)

    return schemas.FriendshipRead(
        id=friendship.id,
        friend=schemas.FriendRead.from_orm(friend),
        created_at=friendship.created_at,
    )

