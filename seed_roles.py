from app.db.database import SessionLocal
from app.db.models import Role

db = SessionLocal()

roles = ["user", "admin"]

for role_name in roles:
    exists = db.query(Role).filter(Role.name == role_name).first()
    if not exists:
        db.add(Role(name=role_name))

db.commit()
db.close()

print("Roles seeded")
