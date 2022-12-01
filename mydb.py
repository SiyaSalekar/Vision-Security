# Database code - on AWS

from flask_sqlalchemy import SQLAlchemy
from .__init__ import db


class UserTable(db.Model):
    __tablename__ = "student_login"
    student_id = db.Column(db.String(255), primary_key = True)
    email = db.Column(db.String(30))
    auth_key = db.Column(db.String(255))
    login = db.Column(db.Integer)

    # constructor
    def __init__(self, email, student_id, auth_key, login):
        self.email = email
        self.student_id = student_id
        self.auth_key = auth_key
        self.login = login


def delete_all():
    try:
        db.session.query(UserTable).delete()
        db.session.commit()
        print("delete all")
    except Exception as e:
        print("Failed "+str(e))
        db.session.rollback()


def get_user_row_if_exists(student_id):
    get_user_row = UserTable.query.filter_by(student_id=student_id).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("Student doesnt exist")
        return False


def add_user_and_login(email, student_id):
    row = get_user_row_if_exists(student_id)
    if row is not False:
        row.login = 1
        db.session.commit()
    else:
        print("Adding Student "+email)

        new_user = UserTable(email, student_id, None, 1)
        db.session.add(new_user)
        db.session.commit()


def user_logout(student_id):
    row = get_user_row_if_exists(student_id)
    if row is not False:
        row.login = 0
        db.session.commit()
        print("Student "+row.email+" logged out")


def add_auth_key(student_id, auth_key):
    row = get_user_row_if_exists(student_id)
    if row is not False:
        row.authkey = auth_key
        db.session.commit()
        print("Student "+row.name+" authkey added")


def view_all():
    row = UserTable.query.all()
    for n in range(0, len(row)):
        print(str(row[n].student_id) + " | "+ row[n].email +" | "+ str(row[n].student_number) + " | " + str(row[n].authkey) + " | " + str(row[n].login))

