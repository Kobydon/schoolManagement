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
        fields=("id","staff_number","class_name","class_size","grade_together"
)
        
        
class schemeSchema(ma.Schema):
    class Meta:
        fields=("id","exams_score","subject_name","midterm_score","class_score","default"
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
                "region","level","population","address","phone","created_date", "color_one","church_logo","report_type",
                "color_two","color_three","address","logo","school_name","closing_date","reopening_date",
                "year","term","working_mail","push_notification","bulk_message","note","fees_type","total_amount","name",
                "amount","user","date","from_time","to_time","section","class_name","room","subject_name","countdown",
                "exam_name","district","circuit","status" ,"role","image","percentage","default","category","promotion_status")
        


class staffSchema(ma.Schema):
    class Meta:
        fields=("id","subject_name","bank_name","bank_branch","email","firstname","lastname",
                "phone","department","national_id","address","staff_number","appointment_date",
                "year_joined","created_date","subject_name","residential_status","bank_account_number","school_name","ssn",
                "promotional_status","other_name",    "current_management_unit" ,"form_master",
      "payroll_status ", " at_post " ,"onleave_type","gender","for_class"

                
)
        

staff_schema=staffSchema(many=True)


school_schema=schoolSchema(many=True)


school = Blueprint("school", __name__)
guard.init_app(app, User)


def update_countdown():
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

def update_countdown_and_schedule():
    # Run update_countdown initially when the script starts
    update_countdown()

    # Schedule update_countdown to run daily at any time within the day
    schedule.every().day.do(update_countdown)

    # Keep the script running to allow scheduled jobs to execute
    while True:
        schedule.run_pending()
        time.sleep(1)


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


@school.route("/get_school_detail",methods=['GET'])
@flask_praetorian.auth_required
def get_school_detail():
    
    update_countdown()
    
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    sch =School.query.filter_by(school_name= user.school_name)
    result = school_schema.dump(sch)
    return jsonify(result)


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
                address=address,firstname=firstname,lastname=lastname,email=email,phone =phone,payroll_status=payroll_status,
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
           address=address,firstname=firstname,lastname=lastname,phone =phone,other_name=other_name,
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
        staff_number =request.json["staff_number"]
        
    except:
        staff_number = ""
    cls = Class(class_name=class_name,staff_number=staff_number ,school_name =user.school_name,grade_together="0",
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
   
    cls_data = Class.query.filter_by(id=id).first()
    ct = Staff.query.filter_by(staff_number=cls_data.staff_number).first()
    if ct:
        ct.form_master = "no"
        ct.for_class = ""
    db.session.commit()
    cls_data.class_name = request.json["class_name"]
    cls_data.staff_number=request.json["staff_number"]
  
    st = Staff.query.filter_by(staff_number=staff_number).first()
   
    if st:
        st.form_master = "yes"
        st.for_class = request.json["class_name"]
       
    else: 
         st.for_class = "no"
        
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
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    subj = Scheme.query.filter_by(school_name=user.school_name)
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
        broadsheet_entries = Student.query.filter_by(school_name=user.school_name).all()
        for entry in broadsheet_entries:
            if (entry.class_name =="JHS 1A" or entry.class_name =="JHS 1B"):
                    c_name = entry.class_name[:5] 
                    
            elif (entry.class_name  =="JHS 2A" or entry.class_name =="JHS 2B"):
                    c_name = entry.class_name [:5] 
                    
            elif (entry.class_name  =="JHS 3A" or entry.class_name =="JHS 3B" or entry.class_name =="JHS 3C"):
                    c_name = entry.class_name [:5] 
            else:
                  c_name =entry.class_name
            name = entry.last_name +""+ entry.other_name +""+ entry.first_name
            new_entry = BroadSheet(
                student_number=entry.student_number, student_name=name, class_name=c_name,
                original_class_name=entry.class_name, year=year, term=term,
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
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first() 
    cls = FeesType.query.filter_by(school_name=user.school_name).all()
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
    # note =request.json["note"]
    role =  request.json["role"]
    if (role =="all"):
        rle ="admin,accountant,student,teacher"
        
    else:
        rle =role
        
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    ntc=Noticer(name=name,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
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
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
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
    if (role =="all"):
        rle ="admin,accountant,student,teacher"
        
    else:
        rle =role
    id = request.json["id"]
    sub_data=Noticer.query.filter_by(id=id).first()
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
    category =request.json["category"],
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
  
