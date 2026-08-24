from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Make sure to replace 'your_password' with the password you set during initdb!
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:your_password@localhost:5445/elyon_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()