
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
import schedule
from application.database.main_db.db import *
# from  application.client_view.client import client
#from  application.room_view.room import room
#from  application.employee_view.employee import employee
#from  application.guest_view.guest import guest





app.register_blueprint(user,url_prefix="/user")


app.register_blueprint(student,url_prefix="/student")
app.register_blueprint(school,url_prefix="/school")

app =app 

with app.app_context():
             db.create_all()

def update_countdown_and_schedule():
    def update_countdown():
         # Import SQLAlchemy model and db session here

        try:
            # Get the current date
            current_date = date.today()

            # Query all academic institutions with status="current"
            schools = Academic.query.filter_by(status="current").all()

            for school in schools:
                # Convert string closing_date to datetime object
                closing_date = datetime.strptime(school.closing_date, '%Y-%m-%d').date()

                # Calculate the difference in days between current_date and closing_date
                countdown_days = (closing_date - current_date).days

                # Update countdown only if it has changed
                if school.countdown != countdown_days:
                    school.countdown = countdown_days

            # Flush changes to the session
            db.session.flush()

            # Commit changes to Academic table after updating all schools
            db.session.commit()

            # TODO: Implement updating User table based on Academic countdown

        except Exception as e:
            print(f"Error updating countdown: {str(e)}")
            db.session.rollback()  # Rollback changes in case of error

    # Run update_countdown initially when the script starts
    update_countdown()

    # Schedule update_countdown to run daily at any time within the day
    schedule.every().day.do(update_countdown)

    # Keep the script running to allow scheduled jobs to execute
    while True:
        schedule.run_pending()
        time.sleep(1)

         
if __name__ =='__main__':
    with app.app_context():
        update_countdown_and_schedule()  # Start the scheduling loop
        # update_user_status()
    # Run the Flask app
    app.run(debug=True)
    
    # app.run(debug='True')