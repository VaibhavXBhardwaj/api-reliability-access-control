def init_roles(db):
    from app.db.models import Role   # 👈 import INSIDE function

    if not db.query(Role).first():
        db.add(Role(name="admin"))
        db.add(Role(name="user"))
        db.commit()
