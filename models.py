from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    dept = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f"<User {self.name}>"