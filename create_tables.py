from app.db.session import engine, Base
from app.db.models import User

Base.metadata.create_all(bind=engine)

print("Tables created successfully")
