from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    dept = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    password = db.Column(db.String(200), nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_num = db.Column(db.String(50))
    deadline = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.task_num}>"