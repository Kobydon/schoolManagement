
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
# from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database import *
# from application.database.user.user_db import User
from sqlalchemy import or_,desc,and_
from datetime import datetime
from flask import session
from  application.user_view.user import user
from  application.student_view.student import student
from  application.school_view.school import school
from application.database.main_db.db import db,BroadSheet,Student,Class
from sqlalchemy import func
# from  application.client_view.client import client
#from  application.room_view.room import room
#from  application.employee_view.employee import employee
#from  application.guest_view.guest import guest




def fetch_student_names():
    student_names = {}
    try:
        students = db.session.query(
            Student.student_number,
            func.concat(
                Student.last_name, ' ', Student.other_name, ' ', Student.first_name
            ).label('full_name')
        ).all()

        for student in students:
            student_names[student.student_number] = student.full_name

    except Exception as e:
        print(f"An error occurred while fetching student names: {e}")

    return student_names

def update_broad_sheet_student_name():
    student_names = fetch_student_names()
    
    try:
        for student_number, full_name in student_names.items():
            db.session.query(BroadSheet).filter(
                BroadSheet.student_number == student_number
            ).update({
                BroadSheet.student_name: full_name
            }, synchronize_session=False)

        db.session.commit()
        print("Update successful!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()


def add_broad_sheet_student_name_all():
    student_names = fetch_student_names()

    try:
        for student_number, full_name in student_names.items():
            # Check if the student already exists
            existing_student = db.session.query(BroadSheet).filter(
                BroadSheet.student_number == student_number
            ).first()
            
            # Add a new record if the student doesn't exist
            if not existing_student:
                new_student = BroadSheet(
                    student_number=student_number,
                    student_name=full_name
                )
                db.session.add(new_student)

        db.session.commit()
        print("Addition successful!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()



if __name__ == '__main__':
    with app.app_context():
        update_broad_sheet_student_name()
        db.create_all()


# Call the function to update



app.register_blueprint(user,url_prefix="/user")


app.register_blueprint(student,url_prefix="/student")
app.register_blueprint(school,url_prefix="/school")

app =app 

if __name__ == '__main__':
    with app.app_context():
        update_broad_sheet_student_name()
        db.create_all()
    # with app.app_context():
        


    app.run(debug=True)
    
    # app.run(debug='True')