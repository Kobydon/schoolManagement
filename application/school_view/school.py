from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
from sqlalchemy.dialects.sqlite import *

# from application.forms import LoginForm
from application.database.main_db.db import *
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session
import random

class StudentSchema(ma.Schema):
    class Meta:
        fields=("id","firstname","lastname","student_number","email","parent_name","admitted_year",
                "address","resindential_status","parent_phone","address","phone","created_date",
                "form"
)
   
class DepartmentSchema(ma.Schema):
    class Meta:
        fields=("id","department_name","department_head","created_date","subject_name","total_teachers","total_subjects")
                        


class classSchema(ma.Schema):
    class Meta:
        fields=("id","staff_number","class_name","class_size"
)
        
        
class schemeSchema(ma.Schema):
    class Meta:
        fields=("id","exams_score","subject_name","midterm_score","class_score"
)
   
   
schema_schema=schemeSchema(many=True)
class_schema = classSchema(many=True)

department_schema = DepartmentSchema(many=True)

student_schema=StudentSchema(many=True)


student = Blueprint("student", __name__)
guard.init_app(app, User)


class schoolSchema(ma.Schema):
    class Meta:
        fields=("id","school_name","school_anthem","headmaster","mail","motto","established_year","status",
                "region","level","population","address","phone","created_date", "color_one",
                "color_two","color_three","address","logo","school_name","closing_date","reopening_date",
                "year","term","working_mail","push_notification","bulk_message","note","fees_type","total_amount","name",
                "amount","user","date")
        


class staffSchema(ma.Schema):
    class Meta:
        fields=("id","subject_name","bank_name","bank_branch","email","firstname","lastname",
                "phone","department","national_id","address","staff_number","appointment_date",
                "year_joined","created_date","subject_name","residential_status","bank_account_number","school_name","ssn",
                "promotional_status"
                
)
        

staff_schema=staffSchema(many=True)


school_schema=schoolSchema(many=True)


school = Blueprint("school", __name__)
guard.init_app(app, User)




@school.route("/register",methods=['POST'])
@flask_praetorian.auth_required
def register():
        school_name= request.json["school_name"]
        school_anthem= request.json["school_anthem"]
        established_year= request.json["established_year"]
        logo= request.json["logo"]
       
        mail= request.json["email"]
        level= request.json["level"]
        address = request.json["address"]
        region = request.json["region"]
        population = request.json["population"]
        motto= request.json["motto"]

        headmaster= request.json["head_master"]
        color_one= request.json["color_one"]
        color_two= request.json["color_two"]
        color_three= request.json["color_three"]
        username = request.json["username"]
        password = request.json["password"]
        phone = request.json["phone"]
        hashed_password= guard.hash_password(password)
  
        created_by_id = flask_praetorian.current_user().id
        
        
        sch = School(school_name=school_name,school_anthem=school_anthem,established_year=established_year,population=population,color_one=color_one,
                     address= address,color_two=color_two,color_three=color_three,username=username,password = hashed_password,
                     motto=motto,headmaster=headmaster,phone=phone,created_by_id = created_by_id,
                     level=level,region=region,mail=mail,logo =logo,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        usr = User(firstname = school_name ,lastname =school_name,roles="admin",username=username,hashed_password=hashed_password,
                   created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),school_name=school_name)
     
        
        db.session.add(sch)
        db.session.add(usr)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code =200
        return resp



@school.route("/get_schools",methods=['GET'])
@flask_praetorian.auth_required
def get_schools():
    sch =School.query.all()
    result = school_schema.dump(sch)
    return jsonify(result)



# @school.route("/get_school_detail_by_staff",methods=['GET'])
# @flask_praetorian.auth_required
# def get_school_detail_by_staff():
#     user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
#     staf = Staff.query.filter_by(staff_number =user.username).first()
#     sch =School.query.filter_by(school_name= staf.school_name)
#     result = school_schema.dump(sch)
#     return jsonify(result)


@school.route("/get_school_detail",methods=['GET'])
@flask_praetorian.auth_required
def get_school_detail():
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    sch =School.query.filter_by(school_name= user.school_name)
    result = school_schema.dump(sch)
    return jsonify(result)


@school.route("/add_subject",methods=['POST'])
@flask_praetorian.auth_required
def add_subject():
    department_name= request.json["department_name"]
    subject_name =request.json["subject_name"]
    subj = Subject(department_name=department_name,
                   subject_name=subject_name,created_by_id=flask_praetorian.current_user().id  )
    dep = Department.query.filter_by(department_name=department_name).first()
    dep.total_subjects = int(dep.total_subjects)+ 1
    db.session.add(subj)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_subjects",methods=['GET'])
@flask_praetorian.auth_required
def get_subjects():

    subj = Subject.query.all()
    result = department_schema.dump(subj)
    return jsonify(result)



@school.route("/get_subject/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_subject(id):

    subj = Subject.query.filter_by(id=id)
    result = department_schema.dump(subj)
    return jsonify(result)




@school.route("/update_subject",methods=['PUT'])
@flask_praetorian.auth_required
def update_subject():
    id = request.json["id"]
    sub_data = Subject.query.filter_by(id=id).first()
    sub_data.department_name = request.json["department_name"]
    sub_data.subject_name =request.json["subject_name"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_subject/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_subject(id):
      sub_data = Subject.query.filter_by(id=id).first()
      dep = Department.query.filter_by(department_name=sub_data.department_name).first()
      dep.total_subjects = int(dep.total_subjects) - 1
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      


@school.route("/add_department",methods=['POST'])
@flask_praetorian.auth_required
def add_department():
    department_name= request.json["department_name"]
    department_head =request.json["department_head"]
    dep = Department(department_name=department_name,total_teachers=0,total_subjects=0
                     ,created_by_id = flask_praetorian.current_user().id,
                     department_head=department_head,created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
                     )
    db.session.add(dep)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


@school.route("/get_department",methods=['GET'])
@flask_praetorian.auth_required
def get_department():

    dep = Department.query.filter_by(created_by_id = flask_praetorian.current_user().id)
    result = department_schema.dump(dep)
    return jsonify(result)




@school.route("/department_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def department_info(id):

    dep = Department.query.filter_by(id=id)
    result = department_schema.dump(dep)
    return jsonify(result)



@school.route("/update_department",methods=['PUT'])
@flask_praetorian.auth_required
def update_department():
    id = request.json["id"]
    dep_data = Department.query.filter_by(id=id).first()
    dep_data.department_name = request.json["department_name"]
    dep_data.department_head =request.json["department_head"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp
    
    
# @school.route("/update_department",methods=['PUT'])
# @flask_praetorian.auth_required
# def update_department():
#     id = request.json["id"]
#     dep_data = Department.query.filter_by(id=id).first()
#     dep_data.department_name = request.json["department_name"]
#     dep_data.department_head =request.json["department_head"]
#     db.session.commit()
#     db.session.close()
#     resp = jsonify("success")
#     resp.status_code =201
#     return resp
    
    
@school.route("/delete_department/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_department(id):
      dep_data = Department.query.filter_by(id=id).first()
      db.session.delete(dep_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
 
 
@school.route("/add_staff_b_excel",methods=['POST'])
@flask_praetorian.auth_required
def add_staff_b_excel():
    #   json_data = request.json
    #   for s in range(len(json_data)):
    #       if request.json["Resident" and "Branch" and "First Name" and "Address" and "Subject" and
    #                     "Email" and "Department" and "Phone" and "Bank" and "Account" and "Last Name" and 
    #                     "Joined"]:
              
      
 
        json_data= request.json
        subject_name =request.json["Subject"]
        
        firstname = request.json["First Name"]

        lastname =request.json["Last Name"]
        phone =request.json["Phone"]
        email = request.json["Email"]

        address =request.json["Address"]
        dep = Subject.query.filter_by(subject_name=subject_name).first()
        department = dep.department_name
        usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        school_name= usr.school_name
        sch = School.query.filter_by(username=usr.username).first()
        school_name = sch.school_name
        n = random.randint(0,100)
        first_three = sch.school_name[:3] + str(n)
        staff_number = first_three
        national_id = request.json["ID No."]

        bank_name =request.json["Bank"]
        bank_account_number= request.json["Account"]
        bank_branch =request.json["Branch"]
        ssn= request.json["SSN"]
        role= request.json["role"]
        promotional_status =request.json["Promotion Status"]
#   course_name =request.json[""]
        residential_status =request.json["Resident"]
        appointment_date =request.json["Appointment"]
        year_joined =request.json["Joined"]
#   subject =request.json["subject"]
        created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
        created_by_id =flask_praetorian.current_user().id
        stf = Staff(ssn=ssn,promotional_status=promotional_status,created_by_id=created_by_id,subject_name=subject_name ,created_date=created_date,bank_name=bank_name,school_name=school_name,
            bank_branch=bank_branch, bank_account_number=bank_account_number ,national_id=national_id,   staff_number=staff_number,
            residential_status=residential_status,appointment_date=appointment_date,year_joined=year_joined,department=department,
            address=address,firstname=firstname,lastname=lastname,email=email,phone =phone
            )
        dep = Department.query.filter_by(department_name=dep.department_name).first()
        dep.total_teachers = int(dep.total_teachers)+ len(json_data)
        usr = User(firstname=firstname,lastname=lastname,roles="role",username=staff_number,
                   hashed_password= guard.hash_password(staff_number),created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                   school_name=school_name)
        
        db.session.add(stf)
        db.session.add(usr)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code =200
        return resp   

@school.route("/add_staff",methods=['POST'])
@flask_praetorian.auth_required
def add_staff():
      subject_name =request.json["subject_name"]
      firstname =request.json["first_name"]
      ssn= request.json["ssn"]
      promotional_status =request.json["promotional_status"]
      lastname =request.json["last_name"]
      phone =request.json["phone"]
      email = request.json["email"]
      phone =request.json["phone"]
      address =request.json["address"]
      dep = Subject.query.filter_by(subject_name=subject_name).first()
      department = dep.department_name
      usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      school_name= usr.school_name
      role= request.json["role"]
      sch = School.query.filter_by(username=usr.username).first()
      school_name = sch.school_name
      n = random.randint(0,100)
      first_three = sch.school_name[:3] + str(n)
      staff_number = first_three
      national_id = request.json["national_id"]
     
      bank_name =request.json["bank_name"]
      bank_account_number =request.json["account_number"]
      bank_branch =request.json["bank_branch"]
    #   course_name =request.json[""]
      residential_status =request.json["resedential_status"]
      appointment_date =request.json["appointment_date"]
      year_joined =request.json["year_joined"]
    #   subject =request.json["subject"]
      created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id =flask_praetorian.current_user().id
      stf = Staff(ssn=ssn,promotional_status=promotional_status,created_by_id=created_by_id,subject=subject_name ,created_date=created_date,bank_name=bank_name,school_name=school_name,
           bank_branch=bank_branch, bank_account_number=bank_account_number ,national_id=national_id,   staff_number=staff_number,
           residential_status=residential_status,appointment_date=appointment_date,year_joined=year_joined,department=department,
           address=address,firstname=firstname,lastname=lastname,phone =phone
           )
      dep = Department.query.filter_by(department_name=dep.department_name).first()
      dep.total_teachers = int(dep.total_teachers)+ 1
      usr = User(firstname=firstname,lastname=lastname,roles=role,username=staff_number,
                   hashed_password= guard.hash_password(staff_number),email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                   school_name=school_name)
      db.session.add(stf)
      db.session.add(usr)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp



@school.route("/get_staff",methods=['GET'])
@flask_praetorian.auth_required
def get_staff():

    stf = Staff.query.filter_by(created_by_id = flask_praetorian.current_user().id)
    result = staff_schema.dump(stf)
    return jsonify(result)



@school.route("/get_staff_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_staff_info(id):

    stf = Staff.query.filter_by(id=id)
    result = staff_schema.dump(stf)
    return jsonify(result)




@school.route("/update_staff",methods=['PUT'])
@flask_praetorian.auth_required
def update_staff():
      subject_name =request.json["subject_name"]
      id = request.json["id"]
      stf_data = Staff.query.filter_by(id=id).first()
      stf_data.firstname =request.json["first_name"]
      
      stf_data.lastname =request.json["last_name"]
      stf_data.email = request.json["email"]
      stf_data.phone =request.json["phone"]
      stf_data.address =request.json["address"]
      dep = Subject.query.filter_by(subject_name=subject_name).first()
      stf_data.department = dep.department_name
    #   user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    #   stf_data.sch = School.query.filter_by(username=user.username).first()
    #   n = random.randint(0,100)
    #   first_three = sch.school_name[sch:3] + str(n)
      
      stf_data.national_id = request.json["national_id"]
      stf_data.subject_name =request.json["subject_name"]
      stf_data.bank_name =request.json["bank_name"]
      stf_data.bank_account_number =request.json["account_number"]
      stf_data.bank_branch =request.json["bank_branch"]
    #   stf_data.role =request.json["role"]
    #   course_name =request.json[""]
      stf_data.residential_status =request.json["resedential_status"]
      stf_data.appointment_date =request.json["appointment_date"]
      stf_data.year_joined =request.json["year_joined"]
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp

@school.route("/delete_staff/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_staff(id):
      stf_data = Staff.query.filter_by(id=id).first()
      dp= Department.query.filter_by(department_name=stf_data.department).first()
      dp.total_teachers = int(dp.total_teachers) - 1
      
      db.session.delete(stf_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      






@school.route("/add_class",methods=['POST'])
@flask_praetorian.auth_required
def add_class():
    class_name= request.json["class_name"]
    staff_number =request.json["staff_number"]
    cls = Class(class_name=class_name,staff_number=staff_number ,
                created_by_id = flask_praetorian.current_user().id , created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                class_size=0)
   
    db.session.add(cls)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_class",methods=['GET'])
@flask_praetorian.auth_required
def get_class():

    cls = Class.query.all()
    result = class_schema.dump(cls)
    return jsonify(result)



@school.route("/get_class_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_class_info(id):

    cls = Class.query.filter_by(id=id)
    result = class_schema.dump(cls)
    return jsonify(result)




@school.route("/update_class",methods=['PUT'])
@flask_praetorian.auth_required
def update_class():
    id = request.json["id"]
    cls_data = Class.query.filter_by(id=id).first()
    cls_data.class_name = request.json["class_name"]
    cls_data.staff_number=request.json["staff_number"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_class/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def cls_data(id):
      cls_data = Class.query.filter_by(id=id).first()
     
      db.session.delete(cls_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      






@school.route("/add_scheme",methods=['POST'])
@flask_praetorian.auth_required
def add_scheme():
    exams_score= request.json["exams_score"]
    midterm_score =request.json["midterm_score"]
    class_score =request.json["class_score"]
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(staff_number=user.username).first()
    school_name = stf.school_name
    subject_name = request.json["subject_name"]
    created_by_id= flask_praetorian.current_user().id
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    scm = Scheme(exams_score=exams_score,
                   midterm_score=midterm_score,class_score=class_score,
                   school_name=school_name,subject_name=subject_name,created_date=created_date,
                   created_by_id=created_by_id)
    
    db.session.add(scm)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_scheme",methods=['GET'])
@flask_praetorian.auth_required
def get_scheme():

    subj = Scheme.query.filter_by(created_by_id = flask_praetorian.current_user().id)
    result = schema_schema.dump(subj)
    return jsonify(result)



@school.route("/get_scheme_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_scheme_info(id):

    subj = Scheme.query.filter_by(id=id)
    result = schema_schema.dump(subj)
    return jsonify(result)




@school.route("/update_scheme",methods=['PUT'])
@flask_praetorian.auth_required
def update_scheme():
    id = request.json["id"]
    sub_data = Scheme.query.filter_by(id=id).first()
    sub_data.subject_name = request.json["subject_name"]
    sub_data.exams_score = request.json["exams_score"]
    sub_data.midterm_score =request.json["midterm_score"]
    sub_data.class_score =request.json["class_score"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_scheme/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_scheme(id):
      sub_data = Scheme.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      






@school.route("/add_academic_setup",methods=['POST'])
@flask_praetorian.auth_required
def add_academic_setup():
        user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        year =request.json["year"]
        term=request.json["term"]
        closing_date=request.json["closing_date"]
        created_date= datetime.now().strftime('%Y-%m-%d %H:%M')
        reopening_date =request.json["reopen_date"]
        school_name = user.school_name
        created_by_id =flask_praetorian.current_user().id
        
        acd = Academic(closing_date=closing_date,created_date=created_date,term=term,year=year,
                       reopening_date=reopening_date,school_name=school_name,created_by_id=created_by_id
                       )
    
        db.session.add(acd)
    
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code =200
        return resp



@school.route("/get_academic_setup",methods=['GET'])
@flask_praetorian.auth_required
def get_academic_setup():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name)
    result = school_schema.dump(acd)
    return jsonify(result)



@school.route("/get_academic/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_academic(id):

    acd = Academic.query.filter_by(id=id)
    result = school_schema.dump(acd)
    return jsonify(result)




@school.route("/update_academic",methods=['PUT'])
@flask_praetorian.auth_required
def update_academic():
      id = request.json["id"]
    #   closing_date =request.json["closing_date"]
     
      stf_data = Academic.query.filter_by(id=id).first()
      stf_data.closing_date =request.json["closing_date"]
      
      stf_data.reopening_date =request.json["reopen_date"]
      stf_data.year = request.json["year"]
      stf_data.term =request.json["term"]
    
    #   user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
  
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp

@school.route("/delete_academic/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_academic(id):
      stf_data = Academic.query.filter_by(id=id).first()     
      db.session.delete(stf_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      




@school.route("/add_mail",methods=['POST'])
@flask_praetorian.auth_required
def add_mail():
    working_mail= request.json["working_mail"]
    push_notification =request.json["push_notification"]
    bulk_message =request.json["bulk_message"]
    user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
    school_name = user.school_name
    created_by_id = flask_praetorian.current_user().id
    created_date= datetime.now().strftime('%Y-%m-%d %H:%M')
    status = "Pending"
    m = MailSetup(working_mail=working_mail,push_notification=push_notification,bulk_message=bulk_message,school_name=school_name,
                  created_by_id=created_by_id,created_date=created_date,status=status)
    db.session.add(m)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_mail_setup",methods=['GET'])
@flask_praetorian.auth_required
def get_mail_setup():
    user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
    
    n = MailSetup.query.filter_by(school_name=user.school_name)
    result = school_schema.dump(n)
    return jsonify(result)

@school.route("/get_all_mail",methods=['GET'])
@flask_praetorian.auth_required
def get_all_mail():
    # user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
    
    n = MailSetup.query.all()
    result = school_schema.dump(n)
    return jsonify(result)



# @school.route("/get_subject/<id>",methods=['GET'])
# @flask_praetorian.auth_required
# def get_subject(id):

#     subj = Subject.query.filter_by(id=id)
#     result = department_schema.dump(subj)
#     return jsonify(result)


@school.route("/update_mail",methods=['PUT'])
@flask_praetorian.auth_required
def update_mail():
    id = request.json["id"]
    sub_data = MailSetup.query.filter_by(id=id).first()
    
    sub_data.status ="Success"
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp


@school.route("/cancel_mail",methods=['PUT'])
@flask_praetorian.auth_required
def cancel_mail():
    id = request.json["id"]
    sub_data = MailSetup.query.filter_by(id=id).first()
    sub_data.push_notification = request.json["No"]
    sub_data.bulk_message =request.json["No"]
    sub_data.status ="Deactivated"
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp










@school.route("/add_fees_type",methods=['POST'])
@flask_praetorian.auth_required
def add_fees_type():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    fees_type= request.json["fees_type"]
    note =request.json["note"]
    total_amount =request.json["total_amount"]
    school_name = user.school_name
    cls = FeesType(fees_type=fees_type,note=note ,total_amount=total_amount,
                created_by_id = flask_praetorian.current_user().id , created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                school_name=school_name
               )
   
    db.session.add(cls)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_fees_type",methods=['GET'])
@flask_praetorian.auth_required
def get_fees_type():

    cls = FeesType.query.all()
    result = school_schema.dump(cls)
    return jsonify(result)



@school.route("/get_fee/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_fee(id):

    cls = FeesType.query.filter_by(id=id)
    result = school_schema.dump(cls)
    return jsonify(result)




@school.route("/update_fees_type",methods=['PUT'])
@flask_praetorian.auth_required
def update_fees_type():
    id = request.json["id"]
    cls_data = FeesType.query.filter_by(id=id).first()
    cls_data.fees_type = request.json["fees_type"]
    cls_data.note=request.json["note"]
    cls_data.total_amount=request.json["total_amount"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_fees_type/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_fees_type(id):
      cls_data = FeesType.query.filter_by(id=id).first()
     
      db.session.delete(cls_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      










@school.route("/add_expense",methods=['POST'])
@flask_praetorian.auth_required
def add_expense():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["amount"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    exp = Expenses(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(exp)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_expense_list",methods=['GET'])
@flask_praetorian.auth_required
def get_expense_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    exp = Expenses.query.filter_by(school_name =user.school_name)
    result = school_schema.dump(exp)
    return jsonify(result)



@school.route("/get_expense/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_expense(id):

    exp = Expenses.query.filter_by(id=id)
    result = school_schema.dump(exp)
    return jsonify(result)




@school.route("/update_expense",methods=['PUT'])
@flask_praetorian.auth_required
def update_expense():
    id = request.json["id"]
    sub_data = Expenses.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_expense/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_expense(id):
      sub_data = Expenses.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp










@school.route("/add_income",methods=['POST'])
@flask_praetorian.auth_required
def add_income():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["amount"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Income(name=name,amount=amount,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_income_list",methods=['GET'])
@flask_praetorian.auth_required
def get_income_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Income.query.filter_by(school_name=user.school_name)
    result = school_schema.dump(inc)
    return jsonify(result)



@school.route("/get_income/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_income(id):

    inc = Income.query.filter_by(id=id)
    result = school_schema.dump(inc)
    return jsonify(result)




@school.route("/update_income",methods=['PUT'])
@flask_praetorian.auth_required
def update_income():
    id = request.json["id"]
    sub_data = Income.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_income/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_income(id):
      sub_data = Income.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp











@school.route("/add_notice",methods=['POST'])
@flask_praetorian.auth_required
def add_notice():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    note =request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = Notice(name=name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_notice_list",methods=['GET'])
@flask_praetorian.auth_required
def get_notice_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Notice.query.filter_by(school_name=user.school_name)
    btc = ntc.order_by(desc(Notice.date))
    result = school_schema.dump(btc)
    return jsonify(result)



@school.route("/get_notice/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_notice(id):

    ntc = Notice.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_notice",methods=['PUT'])
@flask_praetorian.auth_required
def update_notice():
    id = request.json["id"]
    sub_data = Notice.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_notice/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_notice(id):
      sub_data = Notice.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp














@school.route("/add_event",methods=['POST'])
@flask_praetorian.auth_required
def add_event():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    note =request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = Event(name=name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_event_list",methods=['GET'])
@flask_praetorian.auth_required
def get_event_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Event.query.filter_by(school_name=user.school_name)
    btc = ntc.order_by(desc(Event.date))
    result = school_schema.dump(btc)
    return jsonify(result)



@school.route("/get_event/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_event(id):

    ntc = Event.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_event",methods=['PUT'])
@flask_praetorian.auth_required
def update_event():
    id = request.json["id"]
    sub_data = Event.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_event/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_event(id):
      sub_data = Event.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp












@school.route("/add_holiday",methods=['POST'])
@flask_praetorian.auth_required
def add_holiday():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    note =request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = Holiday(name=name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_holiday_list",methods=['GET'])
@flask_praetorian.auth_required
def get_holiday_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Holiday.query.filter_by(school_name=user.school_name)
    btc = ntc.order_by(desc(Holiday.date))
    
    result = school_schema.dump(btc)
    return jsonify(result)



@school.route("/get_holiday/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_holiday(id):

    ntc = Holiday.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_holiday",methods=['PUT'])
@flask_praetorian.auth_required
def update_holiday():
    id = request.json["id"]
    sub_data = Holiday.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_holiday/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_holiday(id):
      sub_data = Holiday.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp







@school.route("/search_income_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    date = request.json["date"]
    print(date)
    pay = Income.query.filter(Income.date.contains(date) )
    lst = pay.order_by(desc(Income.date))
    result = school_schema.dump(lst)
    return jsonify(result)



@school.route("/search_expense_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates():
    date = request.json["date"]
    print(date)
    pay = Expenses.query.filter(Expenses.date.contains(date) )
    lst = pay.order_by(desc(Expenses.date))
    result = school_schema.dump(lst)
    return jsonify(result)

