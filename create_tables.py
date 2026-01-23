from app.db.database import engine
from app.db.base import Base
from app.db import models  # IMPORTANT: this loads Role, User, RefreshToken

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done")
