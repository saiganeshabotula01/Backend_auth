from flask import Flask, request, jsonify
from extensions import db
from models import User, Task
import bcrypt
from dotenv import load_dotenv
import os

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

# Load environment variables
load_dotenv()

app = Flask(__name__)

#  CONFIG FROM .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# INIT
db.init_app(app)
jwt = JWTManager(app)

# CREATE TABLES
with app.app_context():
    db.create_all()


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("name") or not data.get("password"):
        return jsonify({"message": "Missing fields"}), 400

    existing_user = User.query.filter_by(name=data["name"]).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(
        data["password"].encode('utf-8'), bcrypt.gensalt()
    )

    user = User(
        name=data["name"],
        age=data["age"],
        dept=data["dept"],
        salary=data["salary"],
        password=hashed_password.decode('utf-8')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"})


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data.get("name") or not data.get("password"):
        return jsonify({"message": "Missing fields"}), 400

    user = User.query.filter_by(name=data["name"]).first()

    if not user or not bcrypt.checkpw(
        data["password"].encode('utf-8'),
        user.password.encode('utf-8')
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token})


# =========================
# CREATE 
# =========================


# @app.route("/add_user", methods=["POST"])
# @jwt_required()
# def add_user():
#     data = request.json

#     hashed_password = bcrypt.hashpw(
#         data["password"].encode('utf-8'), bcrypt.gensalt()
#     )

#     new_user = User(
#         name=data["name"],
#         age=data["age"],
#         dept=data["dept"],
#         salary=data["salary"],
#         password=hashed_password.decode('utf-8')
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({"message": "User added"})



# =========================
# READ
# =========================
@app.route("/me", methods=["GET"])
@jwt_required()
def get_my_data():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "dept": user.dept,
        "salary": user.salary
    })

# =========================
# UPDATE
# =========================
@app.route("/update_user", methods=["PUT"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json

    user.name = data.get("name", user.name)
    user.age = data.get("age", user.age)
    user.dept = data.get("dept", user.dept)
    user.salary = data.get("salary", user.salary)

    if "password" in data:
        hashed_password = bcrypt.hashpw(
            data["password"].encode('utf-8'), bcrypt.gensalt()
        )
        user.password = hashed_password.decode('utf-8')

    db.session.commit()

    return jsonify({"message": "Updated"})


# =========================
# DELETE
# =========================
@app.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Deleted"})


# =========================
#   ADD Task
# =========================

@app.route("/add_task", methods=["POST"])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get("task_num") or not data.get("deadline"):
        return jsonify({"message": "Missing task data"}), 400

    task = Task(
        task_num=data["task_num"],
        deadline=data["deadline"],
        user_id=int(user_id)
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task added"})


# =========================
#   Tasks
# =========================

@app.route("/my_tasks", methods=["GET"])
@jwt_required()
def get_my_tasks():
    user_id = get_jwt_identity()

    tasks = Task.query.filter_by(user_id=int(user_id)).all()

    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "task_num": task.task_num,
            "deadline": task.deadline
        })

    return jsonify(result)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)