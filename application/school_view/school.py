from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
from sqlalchemy.dialects.sqlite import *
from sqlalchemy import or_,and_ ,desc ,cast, Float ,func
# from application.forms import LoginForm
from application.database.main_db.db import *

from sqlalchemy import or_,desc
from datetime import datetime,timedelta
from datetime import date
from flask import session
import random
import schedule
import time
from flask_praetorian import auth_required, current_user
from datetime import date, datetime
# from flask_praetorian import auth_required, current_user
import schedule
import time


class StudentSchema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","student_number","email","parent_name","admitted_year",
                "address","residential_status","parent_phone","address","phone","created_date",
                "form","class_name" ,"exams_score","midterm_score","class_score","total","remark","subject_name",
                "attitude","teacher_remark","interest","headmaster_remark","conduct",
                "attendance","class_term","grade","rank","pos","term","grade_id","staff_number","name",
                "status","amount","method","balance","paid_by","student","date","fees_type","cls","student_name",
                "other_name","aggregate",
                "rme","science","math","social","pos","creativeart","careertech","english","computing",
                "ghanalanguage","student_name","all_total","school_name","french","original_class_name","sa","admission_number"
)
   
class DepartmentSchema(ma.Schema):
    class Meta:
        fields=("id","department_name","department_head","created_date","subject_name","total_teachers","total_subjects")
                        


class classSchema(ma.Schema):
    class Meta:
        fields=("id","staff_number","class_name","class_size","grade_together","grade"
)
        
        
class schemeSchema(ma.Schema):
    class Meta:
        fields=("id","exams_score","subject_name","midterm_score","class_score","default","grade"
)
   
   
schema_schema=schemeSchema(many=True)
class_schema = classSchema(many=True)

department_schema = DepartmentSchema(many=True)

student_schema=StudentSchema(many=True)


student = Blueprint("student", __name__)
guard.init_app(app, User)


class schoolSchema(ma.Schema):
    class Meta:
        fields=("id","school_name","school_anthem","headmaster","mail","motto","established_year","status","letter",
                "region","level","population","address","phone","created_date", "color_one","church_logo","report_type",
                "color_two","color_three","address","logo","school_name","closing_date","reopening_date",
                "year","term","working_mail","push_notification","bulk_message","note","fees_type","total_amount","name",
                "amount","user","date","from_time","to_time","section","class_name","room","subject_name","countdown","created_by_id",
                "exam_name","district","circuit","status" ,"role","image","percentage","default","category","promotion_status",
                "strand","sub_strand","teacher","link","image","name","grade","basic_salary","net_salary","payment_date","method",
                "show_on","type")
        


class staffSchema(ma.Schema):
    class Meta:
        fields=("id","subject_name","bank_name","bank_branch","email","firstname","lastname",
                "phone","department","national_id","address","staff_number","appointment_date",
                "year_joined","created_date","subject_name","residential_status","bank_account_number","school_name","ssn",
                "promotional_status","other_name",    "current_management_unit" ,"form_master",
      "payroll_status ", " at_post " ,"onleave_type","gender","for_class" ,"role"

                
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
        district= request.json["district"]
        mail= request.json["email"]
        
        level= request.json["level"]
        address = request.json["address"]
        region = request.json["region"]
        population = request.json["population"]
        motto= request.json["motto"]
        try:
            church_logo = request.json["church_logo"]
        except:
            church_logo = ""
        report_type ="default"
        headmaster= request.json["head_master"]
        color_one= request.json["color_one"]
        color_two= request.json["color_two"]
        color_three= request.json["color_three"]
        username = request.json["username"]
        password = request.json["password"]
        phone = request.json["phone"]
        circuit = request.json["circuit"]
        hashed_password= guard.hash_password(password)
  
        created_by_id = flask_praetorian.current_user().id
        
        
        sch = School(district=district,church_logo=church_logo,report_type=report_type,circuit=circuit,school_name=school_name,school_anthem=school_anthem,established_year=established_year,population=population,color_one=color_one,
                     address= address,color_two=color_two,color_three=color_three,username=username,password = hashed_password,
                     motto=motto,headmaster=headmaster,phone=phone,created_by_id = created_by_id,
                     level=level,region=region,mail=mail,logo =logo,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        usr = User(firstname = school_name ,lastname =school_name,roles="admin",username=username,hashed_password=hashed_password,
                   created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),school_name=school_name)
     
        sc = School.query.filter_by(school_name=school_name).first()
        if sc:
            sc.report_type="missionary"
            sc.church_logo = church_logo
            db.session.commit()
        else:
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
@school.route("/get_school_detail", methods=['GET'])
@flask_praetorian.auth_required
def get_school_detail():
    # Get the current authenticated user
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if user.roles == "sAdmin":
        return jsonify({"status": "success"}), 200
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update countdown by passing the user
    update_countdown(user)

    # Get the school details for the user's school
    sch = School.query.filter_by(school_name=user.school_name).all()
    if not sch:
        return jsonify({"error": "School not found"}), 404

    # Serialize the school data
    result = school_schema.dump(sch)
    return jsonify(result)

def update_countdown(user):
    try:
        # Get the current date
        current_date = date.today()

        # Query all academic institutions associated with the user's school and having status "current"
        schools = Academic.query.filter_by(status="current", school_name=user.school_name).all()
        
        if not schools:
            print(f"No 'current' schools found for user: {user.school_name}")
            return

        print(f"Found {len(schools)} 'current' school(s) for user: {user.school_name}")
        
        # Iterate through each school to update the countdown
        for school in schools:
            if school.closing_date:
                # Convert string closing_date to datetime object
                closing_date = datetime.strptime(school.closing_date, '%Y-%m-%d').date()

                # Calculate the difference in days between current_date and closing_date
                countdown_days = (closing_date - current_date).days

                # Update countdown only if it has changed
                if school.countdown != countdown_days:
                    school.countdown = countdown_days
                    print(f"Countdown for school '{school.school_name}' updated to {countdown_days} days.")
            else:
                print(f"Warning: School '{school.school_name}' has no closing date set.")

        # Commit changes to the database after updating all schools
        db.session.commit()
        print("Countdown successfully updated for all relevant schools.")

    except Exception as e:
        print(f"Error updating countdown: {str(e)}")
        db.session.rollback()  # Rollback changes in case of error


@school.route("/add_subject",methods=['POST'])
@flask_praetorian.auth_required
def add_subject():
    # try:
    #     department_name= request.json["department_name"]
        
    # except:
    #     department_name=""
        
    subject_name =request.json["subject_name"] 
    user = User.query.filter_by(id=flask_praetorian.current_user().id  ).first()
    subj = Subjectc( subject_name=subject_name,created_by_id=flask_praetorian.current_user().id ,school_name=user.school_name )
    # dep = Departmentb.query.filter_by(department_name=department_name).first()
    # dep.total_subjects = int(dep.total_subjects)+ 1
    db.session.add(subj)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_subjects",methods=['GET'])
@flask_praetorian.auth_required
def get_subjects():
    
    user = User.query.filter_by(id=flask_praetorian.current_user().id  ).first()
    subj = Subjectc.query.filter_by(school_name=user.school_name)
    result = department_schema.dump(subj)
    
    return jsonify(result)



@school.route("/get_subject/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_subject(id):

    subj = Subjectc.query.filter_by(id=id)
    result = department_schema.dump(subj)
    return jsonify(result)




@school.route("/update_subject",methods=['PUT'])
@flask_praetorian.auth_required
def update_subject():
    id = request.json["id"]
    sub_data = Subjectc.query.filter_by(id=id).first()
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
      sub_data = Subjectc.query.filter_by(id=id).first()
    #   dep = Departmentb.query.filter_by(department_name=sub_data.department_name).first()
    #   dep.total_subjects = int(dep.total_subjects) - 1
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      



@school.route("/delete_school/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_school(id):
      sub_data = School.query.filter_by(id=id).first()
     
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
    dep = Departmentb(department_name=department_name,total_teachers=0,total_subjects=0
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

    dep = Departmentb.query.filter_by(created_by_id = flask_praetorian.current_user().id)
    result = department_schema.dump(dep)
    return jsonify(result)




@school.route("/department_info/<id>",methods=['GET'])
@flask_praetorian.auth_required
def department_info(id):

    dep = Departmentb.query.filter_by(id=id)
    result = department_schema.dump(dep)
    return jsonify(result)



@school.route("/update_department",methods=['PUT'])
@flask_praetorian.auth_required
def update_department():
    id = request.json["id"]
    dep_data = Departmentb.query.filter_by(id=id).first()
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
      dep_data = Departmentb.query.filter_by(id=id).first()
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
        try:
            subject_name =request.json["Subject"]
        
        except:
            subject_name=""
        
        try:    
            gender = request.json["Gender"]
            
        except:
            gender =""
            
        try:
            firstname = request.json["First Name"]
        
        except:
             firstname =""
             
        try:
            
            lastname =request.json["Last Name"]
            
        except:
            lastname =""
       
        role =request.json["Role"]
        
        # other_name = request.json["Other Name"]
        try:
            current_management_unit =request.json["Current Management Unit/Cost Centre"]
        
        except:
            current_management_unit=""
            
        try:
            payroll_status =request.json["Payroll Active Status"]
            
        except:
            payroll_status=""
            
        try:
                
            at_post =request.json["At Post/On Leave"]
            
        except:
            at_post=""
            
        try:
            onleave_type=request.json["On Leave Type"]
            
        except:
             onleave_type=""
             
        try:
            staff_number= str(request.json["Staff No."])
            
        except:
             staff_number=""

        # 
      
        # dep = Subjectc.query.filter_by(subject_name=subject_name).first()
        # department = dep.department_name
        usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        school_name= usr.school_name
        sch = School.query.filter_by(username=usr.username).first()
        school_name = sch.school_name
        n = random.randint(0,100)
        sc = Staff.query.filter_by(school_name=sch.school_name).count()
        cc = int(sc)+1
        first_three = sch.school_name[:3] + str(cc)
         
        try:
            national_id = request.json["Gh No."]
            
        except:
             national_id =""

        try:
            bank_name =request.json["Bank"]
            
        except:
            bank_name=""
            
        try:
            bank_account_number= str(request.json["Account"])
        
        except :
            bank_account_number=""
        # 
        try:
            ssn= request.json["SSN"]
            
        except:
            ssn= ""
            
        role= request.json["Role"]
        

        try:
            department= request.json["Department"]
            
        except:
            department= ""
            
        try:
            job_grade =request.json["Job/Grade"]
            
        except:
            job_grade =""
            
        try:
          phone =request.json["Phone"]
          
        except:
            phone =""
            
        try:
            address=request.json["Address"]
            
        except:
             address=""
          
        try:
            residential_status =request.json["Resident"]
        
        except:
            residential_status=""
        try:    
            bank_branch =request.json["Branch"]
        except:
            bank_branch=""
        try:    
            other_name = request.json["Other Name"]
            
        except:
            other_name=""
        
        try:
            appointment_date =request.json["Appointment"]
            
        except:
            appointment_date=""
            
        try:
          year_joined =request.json["Joined"]
          
        except:
            year_joined=""
            
        try:
            email = request.json["Email"]
            
        except :
            email=""
            
        try:
            promotional_status =request.json["Promotion Status"]
        
        except:
            promotional_status=""
            
        try:
            bank_branch =request.json["Branch"]
            
        except:
            bank_branch=""
            
        try:
             ges_number =request.json["Register Number"]
             
        except:
            ges_number=""
            
        try:
            dob =request.json["DOB"]
            
        except:
            dob=""
            
     
          
     
        # subject =request.json["Subject"]
        created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
        created_by_id =flask_praetorian.current_user().id
        find = Staff.query.filter_by(staff_number = staff_number).first()
        if find:
            resp = jsonify("success")
            resp.status_code =200
            return resp
        
        else:
            stf = Staff(dob=dob,job_grade=job_grade,ges_number=ges_number,ssn=ssn,promotional_status=promotional_status,created_by_id=created_by_id,subject_name=subject_name ,created_date=created_date,bank_name=bank_name,school_name=school_name,
                bank_branch=bank_branch, bank_account_number=bank_account_number ,national_id=national_id,   staff_number=staff_number,
                residential_status=residential_status,appointment_date=appointment_date,year_joined=year_joined,department=department,
                address=address,firstname=firstname,lastname=lastname,email=email,phone =phone,payroll_status=payroll_status,role=role,
                other_name=other_name,current_management_unit=current_management_unit,at_post=at_post,onleave_type=onleave_type,gender=gender,
            
                )
        # subject = Subjectc.query.filter_by(subject_name =subject).first()
        # dep = Departmentb.query.filter_by(department_name=subject.department_name).first()
        # dep.total_teachers = int(dep.total_teachers)+ len(json_data)
        usr = User(firstname=firstname,lastname=lastname,roles=role,username=staff_number,
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
      other_name= request.json["other_name"]
      promotional_status =request.json["promotional_status"]
      lastname =request.json["last_name"]
      phone =request.json["phone"]
      email = request.json["email"]
      phone =request.json["phone"]
      address =request.json["address"]
      dep = Subjectc.query.filter_by(subject_name=subject_name).first()
      department = request.json["department"]
      usr = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      school_name= usr.school_name
      role= request.json["role"]
      sch = School.query.filter_by(username=usr.username).first()
      school_name = sch.school_name
      n = random.randint(0,100)
      first_three = sch.school_name[:3] + str(n)
      staff_number = request.json["staff_number"]
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
           address=address,firstname=firstname,lastname=lastname,phone =phone,other_name=other_name,role=role
           )
      subject = Subjectc.query.filter_by(subject_name =subject_name).first()
    #   dep = Departmentb.query.filter_by(department_name=subject.department_name).first()
    #   dep.total_teachers = int(dep.total_teachers)+ 1
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
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(school_name = user.school_name)
    la = stf.order_by(desc(Staff.firstname))
    result = staff_schema.dump(stf)
    return jsonify(result)



@school.route("/get_staff_inf",methods=['GET'])
@flask_praetorian.auth_required
def get_staff_inf():
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    stf = Staff.query.filter_by(staff_number = user.username,).all()
    result = staff_schema.dump(stf)
    return jsonify(result)

@school.route("/get_staf_a",methods=['POST'])
@flask_praetorian.auth_required
def get_staf_a():
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    class_name = request.json["class_name"]
    cls = Class.query.filter_by(class_name=class_name,school_name=user.school_name).first()
    
    stf = Staff.query.filter_by(staff_number = cls.staff_number).all()
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
  
      id = request.json["id"]
      stf_data = Staff.query.filter_by(id=id).first()
      try:
              
            stf_data.subject_name =request.json["subject_name"]
            
      except:
          stf_data.subject_name =""
          
      try:
              
            stf_data.gender =request.json["gender"]
            
      except:
             stf_data.gender =""

      try:
              
            stf_data.staff_number =request.json["staff_number"]
            
      except:
             stf_data.staff_number =""
      try:
          first_name= request.json["first_name"]
          stf_data.firstname =first_name
      except:
          stf_data.firstname =""
    #   2418072three9
      try:
        lastname=request.json["last_name"]
        stf_data.lastname  = lastname
      except:
           stf_data.lastname  = ""
        
      try:
        stf_data.email =request.json["email"]
      except:
            stf_data.email=""
     
      try:     
        stf_data.phone =request.json["phone"]
      except:
          stf_data.phone =""
      
      try:    
        stf_data.address =request.json["address"]
      except:
          stf_data.address =""
          
      try:
            stf_data.other_name =request.json["other_name"]
      except:
          stf_data.other_name =""
    #   dep = Subject.query.filter_by(subject_name=subject_name).first()
      try:
        stf_data.department =  request.json["deparment"]
        
      except:
          stf_data.department =  ""
    #   user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    #   stf_data.sch = School.query.filter_by(username=user.username).first()
    #   n = random.randint(0,100)
    #   first_three = sch.school_name[sch:3] + str(n)
      try:
        stf_data.national_id = request.json["national_id"]
      except:
         
        stf_data.subject_name =""
      try:
        stf_data.bank_name =request.json["bank_name"]
        
      except:
         stf_data.bank_name =""
         
      try:
        stf_data.bank_account_number =request.json["account_number"]
    
      except:
              
        stf_data.bank_branch =""
    #   stf_data.role =request.json["role"]
    #   course_name =request.json[""]
    
      try:   
        stf_data.residential_status =request.json["resedential_status"]
        
      except:
        stf_data.appointment_date =""
        
      try:
        stf_data.year_joined =request.json["year_joined"]
        
      except:
          stf_data.year_joined =""
        
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp

@school.route("/delete_staff/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_staff(id):
      stf_data = Staff.query.filter_by(id=id).first()
              

    #   dp= Departmentb.query.filter_by(department_name=stf_data.department).first()
    #   dp.total_teachers = int(dp.total_teachers) - 1
      
      db.session.delete(stf_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
    
      






@school.route("/add_class",methods=['POST'])
@flask_praetorian.auth_required
def add_class():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    class_name= request.json["class_name"]
    try:
        grade = request.json["grade"]
    except:
        grade =""
    try:
        staff_number =request.json["staff_number"]
        
    except:
        staff_number = ""
    cls = Class(class_name=class_name,staff_number=staff_number ,school_name =user.school_name,grade_together="0",grade=grade,
                created_by_id = flask_praetorian.current_user().id , created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                class_size=0)
    try:
        st = Staff.query.filter_by(staff_number =staff_number).first()
        if st:
            st.fore_master = "yes"
            st.for_class = request.json["class_name"]
            
        else: 
            st.for_class = ""
            
    except:
        print("dd")
        
    
    db.session.add(cls)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_class",methods=['GET'])
@flask_praetorian.auth_required
def get_class():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    cls = Class.query.filter_by(school_name=user.school_name).order_by(Class.class_name.asc())
    result = class_schema.dump(cls)
    return jsonify(result)


@school.route("/search_academic",methods=['POST'])
@flask_praetorian.auth_required
def search_academic():
    
    # class_name = request.json["class_name"]
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    term = request.json["term"]
    year = request.json["year"]# Example class_name
    school_name = user.school_name  # Example school_name
    acd = Academic.query.filter_by(school_name=user.school_name,term=term,year=year)
    result = school_schema.dump(acd)
    return jsonify(result)

@school.route("/search_class_list",methods=['POST'])
@flask_praetorian.auth_required
def search_class_list():
    
    # class_name = request.json["class_name"]
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    class_name = request.json["class_name"]
    term = request.json["term"]
    year = request.json["year"]# Example class_name
    school_name = user.school_name  # Example school_name
    # acd = Academic.query.filter_by(school_name=user.school_name,term=term,year=year).first()
    
    # Join the three tables based on their relationships
                # Join the three tables based on their relationships
    query = db.session.query(
    GeneralRemark.student_number,
    GeneralRemark.attitude,
    GeneralRemark.conduct,
    GeneralRemark.interest,
    GeneralRemark.attendance,
    GeneralRemark.teacher_remark,
    GeneralRemark.headmaster_remark,
    Grading.total,
    Grading.subject_name,
    Grading.class_score,
    Grading.exams_score,
    Grading.rank,
    Grading.grade,
    Grading.remark,
    BroadSheet.all_total,
    BroadSheet.pos,
    BroadSheet.student_name,
    Grading.name,
    BroadSheet.aggregate,
    BroadSheet.promotion_status
    ).join(
    Grading, GeneralRemark.student_number == Grading.student_number
    ).join(
    BroadSheet, GeneralRemark.student_number == BroadSheet.student_number
    ).filter(
    GeneralRemark.class_name == class_name,
    GeneralRemark.year == year,
    GeneralRemark.term == term,
    Grading.original_class_name == class_name,
    BroadSheet.original_class_name == class_name,
    Grading.school_name == school_name,
    BroadSheet.school_name == school_name,
    BroadSheet.year == year,
    BroadSheet.term == term,
    Grading.year == year,
    Grading.term == term,
    ).all()

    grouped_data = []

    for row in query:
        student_number = row[0]
        # Accessing attributes using index
        subject_name = row[8]  # Adjust indices according to the order of attributes in your query
        exams_score = row[10]
        class_score = row[9]
        rank = row[11]
        total = row[7]
        remark = row[13]
        attitude = row[1]
        conduct = row[2]
        interest = row[3]
        teacher_remark = row[5]
        headmaster_remark = row[6]
        attendance = row[4]
        all_total = row[14]
        pos = row[15]
        grade =row[12]
        name=  row[17]
        aggregate=row[18]
        promotion_status=row[19]
        

        # Check if student number is already in grouped_data
        student_data = next((data for data in grouped_data if data['student_number'] == student_number), None)

    # If not, create a new entry
        if not student_data:
            student_data = {
                'student_number': student_number,
                'name':name,
                'grading': [],
                'general_remark': [],
                'broad_sheet': []
            }
            grouped_data.append(student_data)

    # Append grading information
        student_data['grading'].append({
            'subject': subject_name,
            'exams_score': exams_score,
            'class_score': class_score,
            'total': total,
            'rank': rank,
            'grade':grade,
            'remark':remark
        })

    # Update or append general remark
        if not student_data['general_remark']:
            student_data['general_remark'].append({
                'attitude': attitude,
                'conduct': conduct,
                'interest': interest,
                'headmaster_remark': headmaster_remark,
                'attendance': attendance,
                'teacher_remark': teacher_remark
            })

    # Update or append broad sheet information
        if not student_data['broad_sheet']:
            student_data['broad_sheet'].append({
                'all_total': all_total,
                'pos': pos,
                'aggregate':aggregate,
                'promotion_status':promotion_status
            })

# No need to group the data again by student number

    print(grouped_data)
    return grouped_data
        # Return the formatted data
        


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
    staff_number=request.json["staff_number"]

    grade=request.json["grade"]

    cls_data = Class.query.filter_by(id=id).first()
    ct = Staff.query.filter_by(staff_number=cls_data.staff_number).first()
    if ct:
        ct.form_master = "no"
        ct.for_class = ""
    db.session.commit()
    cls_data.class_name = request.json["class_name"]
    cls_data.staff_number=request.json["staff_number"]
    cls_data.grade=request.json["grade"]
    st = Staff.query.filter_by(staff_number=staff_number).first()
   
    if st:
        st.form_master = "yes"
        st.for_class = request.json["class_name"]
       
    else: 
        #  st.for_class = "no"
        print("hh")
        
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
 
    
    
@school.route("/search_class", methods=['POST'])
@flask_praetorian.auth_required  # Requires authentication using flask_praetorian
def search_class():
    # Fetch the current user
    user = db.session.query(User).filter_by(id=flask_praetorian.current_user().id).first()
    
    # Get the class_name from JSON request data
    class_name = request.json["class_name"]
    year = request.json["year"]
    term = request.json["term"]
    
    # Query the Class table to find the class based on class_name
    clss = Class.query.filter_by(class_name=class_name).first()
    
    # Check if classes should be grouped together based on grade
    if clss.grade_together == "1":
        # Define how classes are grouped together based on class_name pattern
        if class_name in ["JHS 1A", "JHS 1B"]:
            c_name = class_name[:5]
        elif class_name in ["JHS 2A", "JHS 2B"]:
            c_name = class_name[:5]
        elif class_name in ["JHS 3A", "JHS 3B", "JHS 3C"]:
            c_name = class_name[:5]
        else:
            c_name = class_name
        # Query BroadSheet for classes that match the grouped name and school_name
        cls_data = BroadSheet.query.filter_by(class_name=c_name, school_name=user.school_name,year=year,term=term).all()
    else:
        # Query BroadSheet for classes that match the exact class_name and school_name
        cls_data = BroadSheet.query.filter_by(original_class_name=class_name, school_name=user.school_name,year=year,term=term).all()
    
    # Serialize the query results using student_schema (assuming it's defined elsewhere)
    result = student_schema.dump(cls_data)
    
    # Return JSON response
    return jsonify(result)







@school.route("/add_scheme",methods=['POST'])
@flask_praetorian.auth_required
def add_scheme():
    exams_score= request.json["exams_score"]
    # midterm_score =request.json["midterm_score"]
    class_score =request.json["class_score"]
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
   
    school_name = user.school_name
    # subject_name = request.json["subject_name"]
    created_by_id= flask_praetorian.current_user().id
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    scm = Scheme(exams_score=exams_score,
                class_score=class_score,
                   school_name=school_name,created_date=created_date,
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
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    subj = Scheme.query.filter_by(school_name=user.school_name).all()
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
    # sub_data.midterm_score =request.json["midterm_score"]
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
    
      







@school.route("/add_academic_setup", methods=['POST'])
@flask_praetorian.auth_required
def add_academic_setup():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        year = request.json["year"]
        term = request.json["term"]
        closing_date = request.json["closing_date"]
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        reopening_date = request.json["reopen_date"]
        school_name = user.school_name
        created_by_id = flask_praetorian.current_user().id
        status = "current"
        
        # Update existing Academic setup status to "old"
        Ad = Academic.query.filter_by(school_name=user.school_name, status="current").first()
        if Ad:
            Ad.status = "old"
    
        db.session.commit()
        
        # Add new Academic setup
        acd = Academic(
            closing_date=closing_date, created_date=created_date, term=term, year=year,
            reopening_date=reopening_date, school_name=school_name, created_by_id=created_by_id, status=status
        )
        db.session.add(acd)
        db.session.commit()
        
        # Query BroadSheet and insert new data
        if term=="1":

          broadsheet_entries = BroadSheet.query.filter(BroadSheet.school_name==user.school_name,BroadSheet.current_status=="new",
                                                       BroadSheet.class_name!="Graduate").all()

        else:
            broadsheet_entries = BroadSheet.query.filter(BroadSheet.school_name==user.school_name,BroadSheet.class_name!="Graduate").all()
        for entry in broadsheet_entries:
            new_entry = BroadSheet(
                student_number=entry.student_number, student_name=entry.student_name, class_name=entry.class_name,
                original_class_name=entry.original_class_name, year=year, term=term,
                owop="", history="", english="", math="", science="", socialstudies="", ghanalanguage="",
                creativeart="", social="", rme="", careertech="", pos="", created_date="", all_total="0",
                computing="", french="", promotion_status="", current_status="", aggregate="", school_name=school_name
            )
            db.session.add(new_entry)
        
        db.session.commit()
        return jsonify("success"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        db.session.close()

@school.route("/get_academic_current",methods=['GET'])
@flask_praetorian.auth_required
def get_academic_current():
    
    v="2"
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").order_by(desc(Academic.year))
    result = school_schema.dump(acd)
    return jsonify(result)



@school.route("/get_academic_setup",methods=['GET'])
@flask_praetorian.auth_required
def get_academic_setup():
    
    v="2"
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name).order_by(desc(Academic.year))
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







@school.route("/search_fees_type",methods=['POST'])
@flask_praetorian.auth_required
def search_fees_type():
    class_name= request.json["class_name"]
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first() 
    cls = FeesType.query.filter(FeesType.school_name.contains(user.school_name),FeesType.class_name.contains(class_name)).all()
    result = school_schema.dump(cls)
    return jsonify(result)



@school.route("/add_fees_type", methods=['POST'])
@flask_praetorian.auth_required
def add_fees_type():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    
    fees_type = request.json["fees_type"]
    note = request.json["note"]
    total_amount = request.json["total_amount"]
    class_name = request.json["class_name"]
    show_on = request.json["show_on"]
    
    if class_name == "All":
        # Query all classes based on the user's school_name
        classes = db.session.query(Class).filter_by(school_name=user.school_name).all()
        
        # Assuming Class has an attribute 'class_name', modify this line accordinglyfor
        class_name = ', '.join([c.class_name for c in classes])


    else:
          classes = db.session.query(Class).filter_by(school_name=user.school_name,grade=class_name).all()
        
        # Assuming Class has an attribute 'class_name', modify this line accordingly
          class_name = ', '.join([c.class_name for c in classes])
        

    school_name = user.school_name
    
    # Create a new FeesType instance
    cls = FeesType(
        fees_type=fees_type,
        note=note,
        total_amount=total_amount,
        class_name=class_name,
        created_by_id=flask_praetorian.current_user().id,
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        school_name=school_name,show_on=show_on
    )

    # Add and commit the new fee type to the database
    db.session.add(cls)
    db.session.commit()
    db.session.close()

    resp = jsonify("success")
    resp.status_code = 200
    return resp



@school.route("/pay_staff",methods=['POST'])
@flask_praetorian.auth_required
def pay_staff():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    school_name = user.school_name
    role= request.json["role"]
    if (role =="all"):
        rle ="accountant,teacher"
        
    else:
        rle =role
        
    date = request.json["date"]
    # date =request.json["date"]
    method = request.json["method"]
    total_salary = db.session.query(func.sum(cast(SalaryTemplate.net_salary, Float))).filter(
        SalaryTemplate.school_name.contains(school_name),
        SalaryTemplate.role.contains(rle)
    ).scalar()

    all_staff  =  db.session.query(Staff).filter(
        Staff.school_name.contains(school_name),
        Staff.role.contains(rle)
    ).count()
    amount= total_salary * all_staff
    # school_name = user.school_name
    status = "Success"
    cls = SalaryPayment(amount=amount,method=method ,role=rle,status=status,
                created_by_id = flask_praetorian.current_user().id , payment_date=date,
                school_name=school_name
               )
    # ntf = Notify(receiver=,message="Salary paid")
    ntc=Noticer(name="Salary ",note="Salary Paid",date=date,
                   created_by_id=flask_praetorian.current_user().id ,letter="",
                   created_date=date,school_name=user.school_name,role=rle)
  
    db.session.add(ntc)
    db.session.add(cls)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


 

@school.route("/get_salary_payment",methods=['GET'])
@flask_praetorian.auth_required
def get_salary_payment():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first() 
    cls = SalaryPayment.query.filter_by(school_name=user.school_name).all()
    result = school_schema.dump(cls)
    return jsonify(result)



@school.route("/get_fees_type",methods=['GET'])
@flask_praetorian.auth_required
def get_fees_type():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first() 
    cls = FeesType.query.filter_by(school_name=user.school_name).all()
    result = school_schema.dump(cls)
    return jsonify(result)


@school.route("/get_fees_type_report",methods=['GET'])
@flask_praetorian.auth_required
def get_fees_type_report():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first() 
    cls = FeesType.query.filter_by(school_name=user.school_name,show_on="yes").all()
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
    cls_data.show_on = request.json["show_on"]
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
    name= request.json["name"]
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
    name= request.json["name"]
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
    try:
         letter =request.json["letter"]
    except:
        letter=""
    # note =request.json["note"]
    role =  request.json["role"]
    if (role =="all"):
        rle ="admin,accountant,student,teacher"
        
    else:
        rle =role
        
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc=Noticer(name=name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,letter=letter,
                   created_date=created_date,school_name=user.school_name,role=rle)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_notice_list",methods=['GET'])
@flask_praetorian.auth_required
def get_notice_list():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if user.roles == "sAdmin":
        return jsonify({"status": "success"}), 200
    if not user:
        return jsonify({"error": "User not found"}), 404
    ntc=Noticer.query.filter(Noticer.school_name.contains(user.school_name),Noticer.role.contains(user.roles))
    btc = ntc.order_by(desc(Noticer.date))
    result = school_schema.dump(btc)
    return jsonify(result)


@school.route("/get_all_notice_list",methods=['GET'])
@flask_praetorian.auth_required
def get_all_notice_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc=Noticer.query.filter(Noticer.school_name ==user.school_name)
    btc = ntc.order_by(desc(Noticer.date))
    result = school_schema.dump(btc)
    return jsonify(result)


@school.route("/get_notice/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_notice(id):

    ntc=Noticer.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_notice",methods=['PUT'])
@flask_praetorian.auth_required
def update_notice():

    role =  request.json["role"]
    sub_data=Noticer.query.filter_by(id=id).first()
    if (role =="all"):
        rle ="admin,accountant,student,teacher"
        
    else:
        rle =role
    id = request.json["id"]
    
    letter= request.json["letter"]

    if letter=="":
            sub_data.letter=sub_data.letter
    else:
        sub_data.letter=letter
    
    sub_data.name = request.json["name"]
    sub_data.role = rle
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
      sub_data=Noticer.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp







@school.route("/add_signature",methods=['POST'])
@flask_praetorian.auth_required
def add_signature():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    image= request.json["image"]
   
    # usr = user.firstname +" " + user.lastname
    # created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    sgn = Signaturer(image=image,school_name=user.school_name)
  
    db.session.add(sgn)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


@school.route("/get_signature",methods=['GET'])
@flask_praetorian.auth_required
def get_signature():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    sgn = Signaturer.query.filter_by(school_name=user.school_name)
    
    result = school_schema.dump(sgn)
    return jsonify(result)


@school.route("/delete_signature/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_signature(id):
      sub_data = Signaturer.query.filter_by(id=id).first()
      
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






@school.route("/activate_school/<id>", methods=['PUT'])
@flask_praetorian.auth_required
def activate_school(id):
    # Fetch the school by its ID
    sub_data = School.query.filter_by(id=id).first()
    
    if not sub_data:
        # If school is not found, return an error response
        return jsonify({"error": "School not found"}), 404
    
    # Get all users associated with the school (assuming the 'id' in User refers to the school ID)
    users = User.query.filter_by(school_name=sub_data.school_name).all()
    
    if not users:
        # If no users are associated with the school, return an error response
        return jsonify({"error": "No users found for this school"}), 404

    # Loop through users and activate each user
    for user in users:
        user.is_active = True  # Set the user's status to active
        db.session.commit()  # Commit the change after each user is updated
    
    # Close the session
    db.session.close()
    
    # Return success response
    resp = jsonify({"message": "School and users activated successfully"})
    resp.status_code = 201
    return resp






@school.route("/deactivate_school/<id>", methods=['PUT'])
@flask_praetorian.auth_required
def deactivate_school(id):
    # Fetch the school by its ID
    sub_data = School.query.filter_by(id=id).first()
    
    if not sub_data:
        # If school is not found, return an error response
        return jsonify({"error": "School not found"}), 404
    
    # Get all users associated with the school (assuming the 'id' in User refers to the school ID)
    users = User.query.filter_by(school_name=sub_data.school_name).all()
    
    if not users:
        # If no users are associated with the school, return an error response
        return jsonify({"error": "No users found for this school"}), 404

    # Loop through users and activate each user
    for user in users:
        user.is_active = False  # Set the user's status to active
        db.session.commit()  # Commit the change after each user is updated
    
    # Close the session
    db.session.close()
    
    # Return success response
    resp = jsonify({"message": "School and users activated successfully"})
    resp.status_code = 201
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



@school.route("/search_income_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    date = request.json["date"]
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    print(date)
    pay = Income.query.filter(Income.date.contains(date), Income.school_name == school_name)
    lst = pay.order_by(desc(Income.date))
    result = school_schema.dump(lst)
    return jsonify(result)


@school.route("/search_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_budget_dates():
    date = request.json["date"]
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    print(date)
    pay = Budget.query.filter(Budget.created_date.contains(date), Budget.school_name == school_name)
    lst = pay.order_by(desc(Budget.created_date))
    result = school_schema.dump(lst)
    return jsonify(result)


@school.route("/search_income_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates_two():
    date = request.json.get("date")
    date_two = request.json.get("datetwo")
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    if not date or not date_two:
        return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Income.query.filter(
            or_(
                Income.date.contains(date),
                Income.date.contains(date_two)
            ),
            Income.school_name == school_name
        ).order_by(desc(Income.date)).all()

        result = school_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@school.route("/search_salary_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_salary_dates():
    date = request.json["date"]
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    print(date)
    pay = SalaryPayment.query.filter(SalaryPayment.payment_date.contains(date), SalaryPayment.school_name == school_name)
    lst = pay.order_by(desc(SalaryPayment.payment_date))
    result = school_schema.dump(lst)
    return jsonify(result)


@school.route("/search_expense_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates():
    date = request.json["date"]
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    print(date)
    pay = Expenses.query.filter(Expenses.date.contains(date), Expenses.school_name == school_name)
    lst = pay.order_by(desc(Expenses.date))
    result = school_schema.dump(lst)
    return jsonify(result)


@school.route("/search_expense_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_budget_dates():
    term = request.json["term"]
    year = request.json["year"]
    type = "expense"
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    pay = Budget.query.filter(
        Budget.term.contains(term),
        Budget.year.contains(year),
        Budget.type.contains(type),
        Budget.school_name == school_name
    )
    lst = pay.order_by(desc(Budget.created_date))
    result = school_schema.dump(lst)
    return jsonify(result)


@school.route("/search_income_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_budget_dates():
    term = request.json["term"]
    year = request.json["year"]
    type = "income"
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    pay = Budget.query.filter(
        Budget.term.contains(term),
        Budget.year.contains(year),
        Budget.type.contains(type),
        Budget.school_name == school_name
    )
    lst = pay.order_by(desc(Budget.created_date))
    result = school_schema.dump(lst)
    return jsonify(result)


def get_current_user_school_name():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    return user.school_name if user else None


@school.route("/search_expense_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates_two():
    date = request.json.get("date")
    date_two = request.json.get("datetwo")
    school_name = get_current_user_school_name()
    if not school_name:
        return jsonify({"error": "User's school name not found"}), 404

    if not date or not date_two:
        return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Expenses.query.filter(
            or_(
                Expenses.date.contains(date),
                Expenses.date.contains(date_two)
            ),
            Expenses.school_name == school_name
        ).order_by(desc(Expenses.date)).all()

        result = school_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500



@school.route("/add_schedule",methods=["POST"])
@flask_praetorian.auth_required
def add_schedule():
      user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
      subject_name=request.json["subject_name"]
      class_name=request.json["class_name"]
      from_time=request.json["from_time"]
      to_time=request.json["to_time"]
      section=request.json["section"]
      date=request.json["date"]
      room=request.json["room"]
      exam_name=request.json["exam_name"]
      created_by_id = user.id
    #   created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
      school_name = user.school_name
      scd = Schedule(subject_name=subject_name,class_name=class_name,from_time=from_time,to_time=to_time,
                     section=section,date=date,room=room,exam_name=exam_name,
                     created_by_id=created_by_id,school_name=school_name)
      db.session.add(scd)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code= 200
      return resp

@school.route("/get_schedule_list",methods=["GET"])
@flask_praetorian.auth_required
def get_schedule_list():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    # stff = Staff.query.filter_by(staff_number=user.username).first()
    cls = Class.query.filter_by(staff_number=user.username).first()
    scd = Schedule.query.filter_by(school_name =user.school_name,class_name =cls.class_name)
    result = school_schema.dump(scd)
    return jsonify(result)

@school.route("/get_all_schedule",methods=["GET"])
@flask_praetorian.auth_required
def get_all_schedule():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    # stff = Staff.query.filter_by(staff_number=user.username).first()
    # cls = Class.query.filter_by(staff_number=user.username).first()
    scd = Schedule.query.filter_by(school_name =user.school_name)
    result = school_schema.dump(scd)
    return jsonify(result)


@school.route("/get_schedule/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_schedule(id):
   
    scd = Schedule.query.filter_by(id=id)
    result = school_schema.dump(scd)
    return jsonify(result)
      
      
@school.route("/update_schedule",methods=["PUT"])
@flask_praetorian.auth_required
def update_schedule():
    #   user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
      id = request.json["id"]
      scd_data = Schedule.query.filter_by(id = id).first()
      scd_data.subject_name=request.json["subject_name"]
      scd_data.class_name=request.json["class_name"]
      scd_data.from_time=request.json["from_time"]
      scd_data.to_time=request.json["to_time"]
      scd_data.section=request.json["section"]
      scd_data.date=request.json["date"]
      scd_data.room=request.json["room"]
      scd_data.exam_name=request.json["exam_name"]
      
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code= 201
      return resp

     
@school.route("/delete_schedule/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_schedule(id):
     scd_data = Schedule.query.filter_by(id = id).first()
     db.session.delete(scd_data)
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code= 201
     return resp

@school.route("/add_exam_attendance",methods=['POST', 'PUT'])
@flask_praetorian.auth_required
def add_exam_attendance():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
    term = acd.term
    year=acd.year
    id = request.json["id"]
    std =  Student.query.filter_by(student_number =id).first()
    class_name = request.json["class_name"]
    subject_name = request.json["subject_name"]
    student_number = std.student_number
    status = request.json["status"]
    name = std.first_name +" "+ std.last_name
    school_name = user.school_name
    created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
    exam_name =  request.json["exam_name"]
    created_by_id = flask_praetorian.current_user().id
    find =  ExamAttend.query.filter_by(student_number =id,exam_name=exam_name,subject_name=subject_name).first()
    if find:
         print("yes")
         atd =  ExamAttend.query.filter_by(student_number =id,exam_name=exam_name,subject_name=subject_name).first()
  
         atd.status = request.json["status"]
         atd.subject_name = request.json["subject_name"]
   
    
   
         atd.exam_name =  request.json["exam_name"]
         atd.year =year
         atd.term =term
         db.session.commit()
         db.session.close()
         resp = jsonify("success")
         resp.status_code=201
         return resp
    
    else:
        atd = ExamAttend(class_name=class_name,subject_name=subject_name,student_number=student_number,
                            status="Present",name=name,school_name=school_name,created_date=created_date,
                            exam_name=exam_name,created_by_id=created_by_id )
    
        db.session.add(atd)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code=201
        return resp

@school.route("/get_exam_attendance",methods=['POST'])
@flask_praetorian.auth_required
def get_exam_attendance():
    user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    exam_name= request.json["exam_name"]
    subject_name = request.json["subject_name"]
    class_name= request.json["class_name"]
    term = request.json["term"]
    year= request.json["year"]
   
    atd = ExamAttend.query.filter_by(school_name=user.school_name,year=year,term=term,exam_name=exam_name,subject_name=subject_name, class_name=class_name)
    result = student_schema.dump(atd)
    return jsonify(result)


@school.route("/update_exam_attendance",methods=['PUT'])
@flask_praetorian.auth_required
def update_exam_attendance():
    # user = User.query.filter_by(id= flask_praetorian.current_user().id).first()
    id = request.json["id"]
    atd =  ExamAttend.query.filter_by(student_number =id).first()
  
    atd.status = request.json["status"]
   
    atd.subject_name = request.json["subject_name"]
   
    atd.exam_name =  request.json["exam_name"]
    
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=201
    return resp
  
  
  
@school.route("/update_grade_together",methods=['PUT'])
@flask_praetorian.auth_required
def update_grade_together():
    id =request.json["id"]
    status = request.json["status"]
    Cla = Class.query.filter_by(id=id).first()
    Cla.grade_together = status
    
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=201
    return resp

@school.route("/update_default",methods=['PUT'])
@flask_praetorian.auth_required
def update_default():
    id =request.json["id"]
    default = request.json["status"]
    sba = SBA.query.filter_by(id=id).first()
    sba.default = default
    
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=201
    return resp

@school.route("/update_scheme_default",methods=['PUT'])
@flask_praetorian.auth_required
def update_scheme_default():
    id =request.json["id"]
    default = request.json["status"]
    sba = Scheme.query.filter_by(id=id).first()
    sba.default = default
    
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=201
    return resp











@school.route("/add_sba",methods=['POST'])
@flask_praetorian.auth_required
def add_sba():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    category =request.json["category"]
    percentage =request.json["percentage"]
    default =""
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = SBA(name=name,category=category,default=default,percentage=percentage,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


@school.route("/get_scheme_default",methods=['GET'])
@flask_praetorian.auth_required
def get_scheme_default():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Scheme.query.filter_by(school_name=user.school_name,default="1").order_by(Scheme.created_date.asc())
    # btc = ntc.order_by(desc(SBA.created_date))
    result = schema_schema.dump(ntc)
    return jsonify(result)


@school.route("/get_sba_default",methods=['GET'])
@flask_praetorian.auth_required
def get_sba_default():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = SBA.query.filter_by(school_name=user.school_name,default="1").order_by(SBA.created_date.asc())
    # btc = ntc.order_by(desc(SBA.created_date))
    result = school_schema.dump(ntc)
    return jsonify(result)


@school.route("/get_sba_class_score",methods=['GET'])
@flask_praetorian.auth_required
def get_sba_class_score():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc =  db.session.query(SBA).filter_by(category="class_score",school_name=user.school_name).all()
    # btc = ntc.order_by(desc(SBA.created_date))
    # print(ntc)
    result = school_schema.dump(ntc)
    return jsonify(result)

@school.route("/get_sba_exam_score",methods=['GET'])
@flask_praetorian.auth_required
def get_sba_exam_score():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc =  db.session.query(SBA).filter_by(category="exam_score",school_name=user.school_name).all()
    # btc = ntc.order_by(desc(SBA.created_date))
    result = school_schema.dump(ntc)
    return jsonify(result)


@school.route("/get_sba_list",methods=['GET'])
@flask_praetorian.auth_required
def get_sba_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = SBA.query.filter_by(school_name=user.school_name)
    btc = ntc.order_by(desc(SBA.created_date))
    result = school_schema.dump(btc)
    return jsonify(result)



@school.route("/get_sba/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_sba(id):

    ntc = SBA.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_sba",methods=['PUT'])
@flask_praetorian.auth_required
def update_sba():
    id = request.json["id"]
    sub_data = SBA.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.category = request.json["category"]
    sub_data.percentage = request.json["percentage"]
     
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_sba/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_sba(id):
      sub_data = SBA.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
  











@school.route("/add_note",methods=['POST'])
@flask_praetorian.auth_required
def add_note():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    note= request.json["note"]
    class_name =request.json["class_name"]
    strand =request.json["strand"]
    sub_strand =request.json["sub_strand"]
    # note =request.json["note"]
    date =  datetime.now().strftime('%Y-%m-%d %H:%M')
    teacher = user.firstname +" "+user.lastname
    
    # usr = user.firstname +" " + user.lastname
    # created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc=Note(class_name=class_name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,strand=strand,
                   sub_strand=sub_strand,school_name=user.school_name,teacher=teacher)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


@school.route("/get_note_list", methods=['GET'])
@flask_praetorian.auth_required
def get_note_list():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if user.roles == "sAdmin":
        return jsonify({"status": "success"}), 200
    else:
        std = Student.query.filter_by(student_number=user.username).first()
        ntc = Note.query.filter(
            Note.school_name.contains(user.school_name),
            Note.class_name.contains(std.class_name)
        )
        btc = ntc.order_by(desc(Note.date))
        result = school_schema.dump(btc)
        return jsonify(result)


@school.route("/get_all_note_list",methods=['GET'])
@flask_praetorian.auth_required
def get_all_note_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc=Note.query.filter(Note.created_by_id==user.id)
    btc = ntc.order_by(desc(Note.date))
    result = school_schema.dump(btc)
    return jsonify(result)


@school.route("/get_note/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_note(id):

    ntc=Note.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_note",methods=['PUT'])
@flask_praetorian.auth_required
def update_note():

    # role =  request.json["role"]
    # if (role =="all"):
    #     rle ="admin,accountant,student,teacher"
        
    # else:
    #     rle =role
    sub_data=Note.query.filter_by(id=id).first()
    id = request.json["id"]
    
    note= request.json["note"]

    if note=="":
            sub_data.note=sub_data.note
    else:
        sub_data.letter=note
  
    sub_data.strand = request.json["strand"]
    sub_data.sub_strand =  request.json["sub_strand"]
    sub_data.class_name = request.json["class_name"]
    # sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_note/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_note(id):
      sub_data=Note.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp










@school.route("/add_material",methods=['POST'])
@flask_praetorian.auth_required
def add_material():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    link= request.json["link"]
    class_name =request.json["class_name"]
    if class_name =="All":
        cls_name="Basic 1,Basic 2,Basic 3,Basic 4,Basic 5,Basic 6,Basic 7,JHS 1,JHS 2,JHS 3"
    else:
        cls_name=class_name
    image =request.json["image"]
    role =request.json["role"]
    # note =request.json["note"]
    date =  datetime.now().strftime('%Y-%m-%d %H:%M')
    # teacher = user.firstname +" "+user.lastname
    
    # usr = user.firstname +" " + user.lastname
    # created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc=Material(class_name=cls_name,role=role,date=date,
                   created_by_id=flask_praetorian.current_user().id ,link=link,
                   image=image,school_name=user.school_name)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_material_list",methods=['GET'])
@flask_praetorian.auth_required
def get_material_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    std= Student.query.filter_by(student_number=user.username).first()
    if user.roles=="student":
        ntc=Material.query.filter(Material.class_name.contains(std.class_name),
                                Material.role.contains(user.roles))
        # Material.school_name.contains,
    else:
        ntc=Material.query.filter(
                                Material.role.contains(user.roles))
    btc = ntc.order_by(desc(Material.date))
    result = school_schema.dump(btc)
    return jsonify(result)


@school.route("/get_all_material_list",methods=['GET'])
@flask_praetorian.auth_required
def get_all_material_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc=Material.query.filter(Material.created_by_id==user.id)
    btc = ntc.order_by(desc(Material.date))
    result = school_schema.dump(btc)
    return jsonify(result)


@school.route("/get_material/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_material(id):

    ntc=Material.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_material",methods=['PUT'])
@flask_praetorian.auth_required
def update_material():

    # role =  request.json["role"]
    # if (role =="all"):
    #     rle ="admin,accountant,student,teacher"
        
    # else:
    #     rle =role
    sub_data=Material.query.filter_by(id=id).first()
    id = request.json["id"]
    
    image= request.json["image"]

    if image=="":
            sub_data.image=sub_data.image
    else:
        sub_data.image=image
   
    sub_data.link = request.json["link"]
    sub_data.role =  request.json["role"]
    sub_data.class_name = request.json["class_name"]
    # sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_Material/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_Material(id):
      sub_data=Material.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp









@school.route("/add_deduction",methods=['POST'])
@flask_praetorian.auth_required
def add_deduction():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    role= request.json["role"]
    # date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = Deduction(name=name,amount=amount,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name,role=role)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_all_deduction",methods=['GET'])
@flask_praetorian.auth_required
def get_all_deduction():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Deduction.query.filter_by(school_name=user.school_name)
    # btc = ntc.order_by(desc(Deduction.date))
    result = school_schema.dump(ntc)
    return jsonify(result)



@school.route("/get_deduction/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_deduction(id):

    ntc = Deduction.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_deduction",methods=['PUT'])
@flask_praetorian.auth_required
def update_deduction():
    id = request.json["id"]
    sub_data = Deduction.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.amount = request.json["amount"]
    sub_data.role = request.json["role"]
    # sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_deduction/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_deduction(id):
      sub_data = Deduction.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp


















@school.route("/add_salary",methods=['POST'])
@flask_praetorian.auth_required
def add_salary():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    basic_salary= request.json["basic_salary"]
    role =request.json["role"]
    grade =request.json["grade"]
    net_salary =request.json["net_salary"]

    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = SalaryTemplate(basic_salary=basic_salary,role=role,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name,grade=grade,net_salary=net_salary)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_all_salary",methods=['GET'])
@flask_praetorian.auth_required
def get_all_salary():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = SalaryTemplate.query.filter_by(school_name=user.school_name)
    # btc = ntc.order_by(desc(Deduction.date))
    result = school_schema.dump(ntc)
    return jsonify(result)



@school.route("/get_salary/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_salary(id):

    ntc = SalaryTemplate.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_salary",methods=['PUT'])
@flask_praetorian.auth_required
def update_salary():
    id = request.json["id"]
    sub_data = SalaryTemplate.query.filter_by(id=id).first()
    sub_data.basic_salary = request.json["basic_salary"]
    sub_data.net_salary = request.json["net_salary"]
    sub_data.role = request.json["role"]
    sub_data.grade = request.json["grade"]
    # sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_salary/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_salary(id):
      sub_data = SalaryTemplate.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp




@school.route("/search_salary",methods=['POST'])
@flask_praetorian.auth_required
def search_salary():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      role = request.json["role"]
      std = Deduction.query.filter_by(school_name=user.school_name,role=role).all()
      result =  school_schema.dump(std)
     
      return jsonify(result)  



@school.route("/get_salary_by_role",methods=['GET'])
@flask_praetorian.auth_required
def get_salary_by_role():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      role = user.roles
      std = SalaryTemplate.query.filter_by(school_name=user.school_name,role=role).all()
      result =  school_schema.dump(std)
     
      return jsonify(result)  




@school.route("/get_deduction_by_role",methods=['GET'])
@flask_praetorian.auth_required
def get_deduction_by_role():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      role = user.roles
      std = Deduction.query.filter_by(school_name=user.school_name,role=role).all()
      result =  school_schema.dump(std)
     
      return jsonify(result)  




@school.route("/get_allowance_by_role",methods=['GET'])
@flask_praetorian.auth_required
def get_allowance_by_role():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      role = user.roles
      std = Allowance.query.filter_by(school_name=user.school_name,role=role).all()
      result =  school_schema.dump(std)
     
      return jsonify(result)  









@school.route("/add_allowance",methods=['POST'])
@flask_praetorian.auth_required
def add_allowance():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    role= request.json["role"]
    # date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc = Allowance(name=name,amount=amount,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name,role=role)
  
    db.session.add(ntc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_all_allowance",methods=['GET'])
@flask_praetorian.auth_required
def get_all_allowance():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    ntc = Allowance.query.filter_by(school_name=user.school_name)
    # btc = ntc.order_by(desc(Deduction.date))
    result = school_schema.dump(ntc)
    return jsonify(result)



@school.route("/get_allowance/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_allowance(id):

    ntc = Allowance.query.filter_by(id=id)
    result = school_schema.dump(ntc)
    return jsonify(result)




@school.route("/update_allowance",methods=['PUT'])
@flask_praetorian.auth_required
def update_allowance():
    id = request.json["id"]
    sub_data = Allowance.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
   
    sub_data.amount = request.json["amount"]
    sub_data.role = request.json["role"]
    # sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_allowance/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_allowance(id):
      sub_data = Allowance.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp





@school.route("/search_allowance",methods=['POST'])
@flask_praetorian.auth_required
def search_allowance():
      user = db.session.query(User).filter_by(id = flask_praetorian.current_user().id).first()
      role = request.json["role"]
      std = Allowance.query.filter_by(school_name=user.school_name,role=role).all()
      result =  school_schema.dump(std)
     
      return jsonify(result)  


# Import your models

@school.route("/search_salary_list", methods=['POST'])
@flask_praetorian.auth_required
def search_salary_list():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    role = request.json.get("role")
    if not role:
        return jsonify({'error': 'Role not provided'}), 400

    # Construct query
    query = db.session.query(
        Staff.staff_number,
        Staff.firstname,
        Staff.lastname,
        Staff.other_name,
        Staff.bank_account_number,
        Staff.bank_name,
        Staff.national_id,
        SalaryTemplate.net_salary,
        Allowance.name.label('allowance_name'),
        Allowance.amount.label('allowance_amount'),
        Deduction.name.label('deduction_name'),
        Deduction.amount.label('deduction_amount')
    ).join(
        SalaryTemplate, SalaryTemplate.staff_number == Staff.staff_number
    ).outerjoin(
        Allowance, Allowance.staff_number == Staff.staff_number
    ).outerjoin(
        Deduction, Deduction.staff_number == Staff.staff_number
    ).filter(
        SalaryTemplate.role == role,
        Allowance.role == role,
        Deduction.role == role
    ).all()

    grouped_data = {}
    
    for row in query:
        staff_number = row[0]
        if staff_number not in grouped_data:
            grouped_data[staff_number] = {
                'staff_number': staff_number,
                'name': f"{row[1]} {row[3]} {row[2]}",
                'national_id': row[6],
                'bank_account_number': row[4],
                'bank_name': row[5],
                'allowance': [],
                'deduction': [],
                'salary': []
            }

        # Append allowance
        if row[8] and row[9]:
            grouped_data[staff_number]['allowance'].append({
                'name': row[8],
                'amount': row[9]
            })

        # Append deduction
        if row[10] and row[11]:
            grouped_data[staff_number]['deduction'].append({
                'name': row[10],
                'amount': row[11]
            })

        # Append salary (assuming only one salary entry per staff number)
        if row[7] and not grouped_data[staff_number]['salary']:
            grouped_data[staff_number]['salary'].append({
                'net_salary': row[7]
            })

    # Convert dictionary to list of values
    result = list(grouped_data.values())

    return jsonify(result)








@school.route("/add_budget",methods=['POST'])
@flask_praetorian.auth_required
def add_budget():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    acd = Academic.query.filter_by(school_name=user.school_name,status="current").first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    type =request.json["type"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Budget(name=name,amount=amount,note=note,type=type,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,school_name=user.school_name,term=acd.term,year=acd.year)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@school.route("/get_budget_list",methods=['GET'])
@flask_praetorian.auth_required
def get_budget_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Budget.query.filter_by(school_name=user.school_name)
    result = school_schema.dump(inc)
    return jsonify(result)



@school.route("/get_budget/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_budget(id):

    inc = Budget.query.filter_by(id=id)
    result = school_schema.dump(inc)
    return jsonify(result)




@school.route("/update_Budget",methods=['PUT'])
@flask_praetorian.auth_required
def update_Budget():
    id = request.json["id"]
    sub_data = Budget.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.type =request.json["type"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@school.route("/delete_budget<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_budget(id):
      sub_data = Budget.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp




@school.route("/delete_general_remarks", methods=['POST'])  # Change to POST if sending data
@flask_praetorian.auth_required
def delete_general_remarks():
    data = request.json.get('items', [])
    
    if not data:
        return jsonify({"error": "No items provided"}), 400
    
    try:
        # Collect all IDs or criteria for deletion
        ids_to_delete = [item.get('id') for item in data if 'id' in item]
        
        if not ids_to_delete:
            return jsonify({"error": "No valid IDs found"}), 400

        # Delete all matching records in one go
        GeneralRemark.query.filter(GeneralRemark.id.in_(ids_to_delete)).delete(synchronize_session='fetch')
        db.session.commit()
        
        return jsonify({"message": "Deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
