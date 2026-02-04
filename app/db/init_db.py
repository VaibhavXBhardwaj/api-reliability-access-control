from sqlalchemy.orm import Session
from app.db.models import Role

def init_roles(db: Session):
    # If roles already exist, do nothing
    if db.query(Role).first():
        return

    roles = [
        Role(id=1, name="user"),
        Role(id=2, name="admin"),
    ]

    db.add_all(roles)
    db.commit()
