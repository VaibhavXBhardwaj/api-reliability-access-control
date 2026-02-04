from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 🔥 IMPORTANT: import models so SQLAlchemy registers them
import app.db.models  # noqa
