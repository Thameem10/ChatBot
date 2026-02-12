from sqlalchemy.orm import Session
from sqlalchemy import select
from database import SessionLocal, engine
from models import Admin
import bcrypt


def seed_data():
    db: Session = SessionLocal()

    try:
        print("Seeding initial data...")

        # --------------------------
        # 1. Hash Password
        # --------------------------
        password = "practice@123"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

        # --------------------------
        # 2. UPSERT ADMIN
        # --------------------------
        existing_admin = db.execute(
            select(Admin).where(Admin.email == "admin@123.com")
        ).scalar_one_or_none()

        if existing_admin:
            admin = existing_admin
        else:
            admin = Admin(
                name="admin",
                email="admin@123.com",
                password=hashed_password,
                role="super admin"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # --------------------------
       

        print("Admin seeded successfully")
        print("Admin:", admin.name, admin.email)
 

    except Exception as e:
        db.rollback()
        print("Seeding failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
