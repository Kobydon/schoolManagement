
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
from  application.school_view.school import school,update_countdown_and_schedule
from application.database.main_db.db import db
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
             
if __name__ =='__main__':
    with app.app_context():
        update_countdown_and_schedule()  # Start the scheduling loop
        # update_user_status()
    # Run the Flask app
    app.run(debug=True)
    
    # app.run(debug='True')