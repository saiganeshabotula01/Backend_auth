from flask import Flask
from extensions import db
from models import User
import bcrypt

# 🔥 CREATE APP MANUALLY (IMPORTANT)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/flask_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    users = User.query.all()

    print(f"Total users found: {len(users)}")

    for user in users:
        print(f"Checking user: {user.name}")

        if user.password.startswith("$2b$"):
            print("Already hashed ✅")
            continue

        print("Hashing password...")

        hashed = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed.decode('utf-8')

    db.session.commit()

print("Migration completed ✅")