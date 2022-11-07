from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We take a default connection to start. 
# We should pull this from env / secrets when securing our server.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/db"

#instantiate database engine and session
Engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Session = SessionLocal()

Base = declarative_base()