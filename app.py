
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
            Student.student_number,Student.school_name,
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
        for student_number,school_name, full_name in student_names.items():
            # Check if the student already exists
            existing_student = db.session.query(BroadSheet).filter(
                BroadSheet.student_number == student_number
            ).first()
            
            # Add a new record if the student doesn't exist
            if not existing_student:
                new_student = BroadSheet(
                    student_number=student_number,
                    student_name=full_name,all_total="0",school_name =school_name
                )
                db.session.add(new_student)

        db.session.commit()
        print("Addition successful!")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.session.close()


def update_broadsheet_aggregate(session, term="1", class_names=None):
    """
    Update the 'aggregate' field in the BroadSheet table by summing scores from the Grading table
    for a specific term and class names.
    
    :param session: SQLAlchemy database session
    :param term: The academic term (default is "1")
    :param class_names: List of class names to filter (e.g., ["Basic 7", "Basic 8", "Basic 9"])
    """
    if class_names is None:
        class_names = ["Basic 7", "Basic 8", "Basic 9"]

    try:
        # Subquery to calculate the aggregate
        subquery = (
            session.query(db.func.sum(Grading.score).label("aggregate"))
            .filter(
                Grading.student_number == BroadSheet.student_number,
                Grading.term == term
            )
            .limit(6)
            .correlate(None)  # Prevent auto-correlation issues
        )

        # Update the BroadSheet table
        session.query(BroadSheet).filter(
            BroadSheet.term == term,
            BroadSheet.class_name.in_(class_names)
        ).update(
            {"aggregate": subquery.scalar_subquery()},
            synchronize_session=False
        )

        # Commit the changes
        session.commit()
        print("BroadSheet aggregates updated successfully.")

    except Exception as e:
        # Rollback in case of error
        session.rollback()
        print(f"An error occurred: {e}")




# Call the function to update



app.register_blueprint(user,url_prefix="/user")


app.register_blueprint(student,url_prefix="/student")
app.register_blueprint(school,url_prefix="/school")

app =app 

if __name__ == '__main__':
    with app.app_context():
        try:
            # Ensure database tables are created
            # db.create_all()

            # Perform BroadSheet updates
            update_broadsheet_aggregate(db.session, term="1", class_names=["Basic 7", "Basic 8", "Basic 9"])
            update_broad_sheet_student_name()

            print("BroadSheet updates completed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Start the Flask application
    app.run(debug=True)

    # app.run(debug='True')