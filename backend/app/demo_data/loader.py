from ..database.session import SessionLocal, engine, Base
from .seed_buyers import seed_demo_database

def init_and_seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_database(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_and_seed_db()
