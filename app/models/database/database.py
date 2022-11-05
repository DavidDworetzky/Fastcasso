from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We take a default connection to start. 
# We should pull this from env / secrets when securing our server.
SQLALCHEMY_DATABASE_URL = "postgresql://default:default@localhost/db"

Engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()