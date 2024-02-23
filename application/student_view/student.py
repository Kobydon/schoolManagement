from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.main_db.db import User,db,Student
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session

class StudentSchema(ma.Schema):
    class Meta:
        fields=("id","firstname","lastname","student_number","email","parent_name","admitted_year",
                "address","resendential_status","parent_phone","address","phone","created_date",
                "form"
)
        









student_schema=StudentSchema(many=True)


student = Blueprint("student", __name__)
guard.init_app(app, User)





@student.route("/add_student",methods=["POST"])

def add_student():
      
          first_name= request.json["first_name"]
          student_number= request.json["student_number"]
          last_name= request.json["last_name"]
          admitted_year= request.json["admitted_year"]
          parent_name= request.json["parent_name"]
          email= request.json["email"]
          address= request.json["address"]
          password= request.json["password"]
          parent_phone= request.json["parent_phone"]
          admitted_year= request.json["admitted_year"]
          form= request.json["form"]
          residential_status= request.json["residential_status"]
          created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
          picture = request.json["picture"]
        #   created_by_id = flask_praetorian.current_user().id
          
          std = Student(  first_name= first_name, student_number= student_number,
                        last_name=last_name,admitted_year=admitted_year,parent_name=parent_name,
                       email=email,address=address,password=password,parent_phone=parent_phone,
                     form=form ,residential_status=residential_status ,created_date=created_date,
                    picture=picture)
          
          db.session.add(std)
          db.session.commit()
          db.session.close()
          resp = jsonify("success")
          resp.status_code=200
          return resp
          
    
@student.route("/get_students",methods=["GET"])

def get_students():
    std = Student.query.all()
    lst = student_schema.dump(std)
    return jsonify(lst)
    

@student.route("/delete_student",methods=["DELETE"])

def delete_student():
    id = request.json["id"]
    std = Student.query.filter_by(id=id).first()
    db.session.delete(std)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    return resp
    
    