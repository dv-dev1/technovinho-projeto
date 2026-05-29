import os
os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:sEQGFxDyvazjWFGkdGIdvEqIIJjGtkjN@zephyr.proxy.rlwy.net:43795/railway"

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password

def seed_admin():
    db = SessionLocal()
    admin_email = "admin@technovinho.com"
    user = db.query(User).filter(User.email == admin_email).first()
    if not user:
        user = User(
            name="Admin Technovinho",
            email=admin_email,
            password=hash_password("admin123"),
            role=UserRole.admin
        )
        db.add(user)
        db.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists!")
    db.close()

if __name__ == "__main__":
    seed_admin()
