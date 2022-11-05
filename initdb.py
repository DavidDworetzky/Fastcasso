#database imports
from app.models.database.database import Base
from app.models.database.database import Engine

Base.metadata.create_all(bind=Engine)