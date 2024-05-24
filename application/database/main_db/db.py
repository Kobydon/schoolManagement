from application.extensions.extensions import *
from application.settings.setup import app
from application.settings.settings import *
from flask_migrate import Migrate



# from application.database.user.user_db import User

#========  Room database =================#
db = SQLAlchemy(app)
# with app.app_context():
#         db.create_all()
# 
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(255),unique=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    picture = db.Column(db.String(500000))
    email = db.Column(db.String(255))
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    school_name =  db.Column(db.String(400))
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    created_date = db.Column(db.String(255))
  

  
    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active





    student_by  = db.relationship('Student', 
    foreign_keys ='Student.created_by_id',
    backref = 'studie',
    lazy=True
    
    )
    nitcr_bff  = db.relationship('Noticer', 
    foreign_keys ='Noticer.created_by_id',
    backref = 'erflcw',
    lazy=True
    
    )
    




    subjectie_by  = db.relationship('Subject', 
    foreign_keys ='Subject.created_by_id',
    backref = 'subjectinga',
    lazy=True
    
    )
 
 

    subjectirre_by  = db.relationship('Subjectc', 
    foreign_keys ='Subjectc.created_by_id',
    backref = 'jsrrrjjsuu',
    lazy=True
    
    )
 
 
 
 
 
    rmarkie  = db.relationship('Remark', 
    foreign_keys ='Remark.created_by_id',
    backref = 'rmarka',
    lazy=True
    
    )
    
    genremarkie  = db.relationship('GeneralRemark', 
    foreign_keys ='GeneralRemark.created_by_id',
    backref = 'genremar',
    lazy=True
    
    )
 
    
    
    staff_by  = db.relationship('Staff', 
    foreign_keys ='Staff.created_by_id',
    backref = 'staffie',
    lazy=True
    
    )
    
        
    eventing_by  = db.relationship('Event', 
    foreign_keys ='Event.created_by_id',
    backref = 'evntng',
    lazy=True
    
    )
    
          
    holi_by  = db.relationship('Holiday', 
    foreign_keys ='Holiday.created_by_id',
    backref = 'holddyn',
    lazy=True
    
    )
    
              
    notcn_by  = db.relationship('Notice', 
    foreign_keys ='Notice.created_by_id',
    backref = 'noticn',
    lazy=True
    
    )
    
    
    mailiee_by  = db.relationship('MailSetup', 
    foreign_keys ='MailSetup.created_by_id',
    backref = 'mailiee',
    lazy=True
    
    )
    
        
    feess_by  = db.relationship('FeesType', 
    foreign_keys ='FeesType.created_by_id',
    backref = 'feesief',
    lazy=True
    
    )
    
    
    
    
    


    course_by  = db.relationship('Course', 
    foreign_keys ='Course.created_by_id',
    backref = 'coursie',
    lazy=True
    
    )
 
    
    pend_gra  = db.relationship('PendingGrade', 
    foreign_keys ='PendingGrade.created_by_id',
    backref = 'pendieee',
    lazy=True
    
    )
 
    
    
    depar_fby  = db.relationship('Departmentb', 
    foreign_keys ='Departmentb.created_by_id',
    backref = 'deparief',
    lazy=True)
    
        
    grade_by  = db.relationship('Grading', 
    foreign_keys ='Grading.created_by_id',
    backref = 'gradie',
    lazy=True)
    
    
            
    Refund_by  = db.relationship('Refund', 
    foreign_keys ='Refund.created_by_id',
    backref = 'refundie',
    lazy=True)
    
    
                
    Payment_by  = db.relationship('Payment', 
    foreign_keys ='Payment.created_by_id',
    backref = 'payie',
    lazy=True)
    
                    
    Attendance_by  = db.relationship('Attendance', 
    foreign_keys ='Attendance.created_by_id',
    backref = 'attendie',
    lazy=True)
    
                      
    schd_by  = db.relationship('Schedule', 
    foreign_keys ='Schedule.created_by_id',
    backref = 'schdddeie',
    lazy=True)
          
                    
    # Academic_by  = db.relationship('Academic_Calender', 
    # foreign_keys ='Academic_Calender.created_by_id',
    # backref = 'acadamecie',
    # lazy=True)
    
    Class_by  = db.relationship('Class', 
    foreign_keys ='Class.created_by_id',
    backref = 'classie',
    lazy=True)
    
    school_by  = db.relationship('School', 
    foreign_keys ='School.created_by_id',
    backref = 'schoolie',
    lazy=True)
    
    
    sch_byy  = db.relationship('Scheme', 
    foreign_keys ='Scheme.created_by_id',
    backref = 'schemiee',
    lazy=True)
    
     
    sch_byy  = db.relationship('Academic', 
    foreign_keys ='Academic.created_by_id',
    backref = 'academty',
    lazy=True)
    
         
    fpbuy  = db.relationship('FeesPayment', 
    foreign_keys ='FeesPayment.created_by_id',
    backref = 'fpby',
    lazy=True)
    
             
    expnses  = db.relationship('Expenses', 
    foreign_keys ='Expenses.created_by_id',
    backref = 'expnsss',
    lazy=True)
                 
    bdsht  = db.relationship('BroadSheet', 
    foreign_keys ='BroadSheet.created_by_id',
    backref = 'brodieshitie',
    lazy=True)

    exam_att  = db.relationship('ExamAttendance', 
    foreign_keys ='ExamAttendance.created_by_id',
    backref = 'e_atnd',
    lazy=True)
    
    
    
    
    income  = db.relationship('Income', 
    foreign_keys ='Income.created_by_id',
    backref = 'incm',
    lazy=True)
    
    
    



class Departmentb(db.Model):
          id =db.Column(db.Integer,primary_key=True)
          department_name =db.Column(db.String(400))
          department_head =db.Column(db.String(400))
          total_teachers =db.Column(db.String(400))
          total_subjects =db.Column(db.String(400))
          
          
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
     
          
         
         
          created_date =db.Column(db.String(400))
        
class Student(db.Model):
          id= db.Column(db.Integer,primary_key=True)
          school_name = db.Column(db.String(400))
          other_name = db.Column(db.String(400))
          first_name= db.Column(db.String(400))
          student_number= db.Column(db.String(400))
          last_name= db.Column(db.String(400))
          admitted_year= db.Column(db.String(400))
          parent_name= db.Column(db.String(400))
          email= db.Column(db.String(400))
          address= db.Column(db.String(400))
          password= db.Column(db.String(400))
          parent_phone= db.Column(db.String(400))
          admitted_year= db.Column(db.String(400))
          form= db.Column(db.String(400))
          residential_status= db.Column(db.String(400))
          admission_number= db.Column(db.String(400))
          school_name = db.Column (db.String(400))
          created_date = db.Column(db.String(400))
          picture = db.Column(db.String(1000000))
          class_name = db.Column(db.String(400))
          pos =  db.Column(db.String(400))
          dob =  db.Column(db.String(400))
          all_total =  db.Column(db.String(400))
          gender=db.Column(db.String(400))

          
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
              
        #   student_pay  = db.relationship('Payment', 
        #     foreign_keys ='Payment.student_name',
        #     backref = 'studiepay',
        #     lazy=True
            
        #     )
     

         


class Staff(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      firstname = db.Column(db.String(400))
      other_name = db.Column(db.String(400))
      staff_id = db.Column(db.String(400))
      lastname = db.Column(db.String(400))
      email = db.Column(db.String(400))
      phone = db.Column(db.String(400))
      address = db.Column(db.String(400))
      department = db.Column(db.String(400))
      dob = db.Column(db.String(400))
      n =db.Column(db.String(400))
      school_name =db.Column(db.String(400))
      staff_number = db.Column(db.String(400))
      national_id = db.Column(db.String(400))
      subject_name = db.Column(db.String(400))
      bank_name = db.Column(db.String(400))
      bank_account_number = db.Column(db.String(400))
      bank_branch = db.Column(db.String(400))
      course_name = db.Column(db.String(400))
      residential_status = db.Column(db.String(400))
      appointment_date = db.Column(db.String(400))
      year_joined = db.Column(db.String(400))
      subject = db.Column(db.String(400))
      created_date = db.Column(db.String(400))
    #   staff = db.Column(db.String(400))
      job_grade =db.Column(db.String(400))
      ssn = db.Column(db.String(400))
      ges_number = db.Column(db.String(400))
      promotional_status = db.Column(db.String(400))
      current_management_unit =db.Column(db.String(400))
      payroll_status =db.Column(db.String(400))
      at_post =db.Column(db.String(400))
      onleave_type=db.Column(db.String(400))
      gender=db.Column(db.String(400))
      form_master=db.Column(db.String(400))
      for_class=db.Column(db.String(400))
      created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
      

     


 
         


class Course(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          course_name = db.Column(db.String(400))
          course_id = db.Column(db.String(400),unique=True)
          department_name = db.Column(db.String(400))
          form = db.Column(db.String(400))    
     
          
          created_date =db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
        




class Signature(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          image = db.Column(db.String(1000000))
          school_name = db.Column(db.String(400),unique=True)
         
        

class Signaturer(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          image = db.Column(db.String(1000000))
          school_name = db.Column(db.String(400),unique=True)

class FeesType(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    fees_type = db.Column(db.String(5000))
    note = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))
    total_amount = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
  
class GeneralRemark(db.Model):
        id =db.Column(db.Integer,primary_key=True)
        attitude = db.Column(db.String(5000))
        conduct = db.Column(db.String(5000))
        attendance =db.Column(db.String(5000))
        interest =db.Column(db.String(5000))
        student_number =db.Column(db.String(5000))
        headmaster_remark= db.Column(db.String(5000))
        teacher_remark=db.Column(db.String(5000))
        first_name= db.Column(db.String(5000))
        last_name=db.Column(db.String(5000))
        term= db.Column(db.String(5000))
        year = db.Column(db.String(5000))
        created_date =db.Column(db.String(5000))
        class_name = db.Column(db.String(5000))
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
        

class FeesPayment(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    fees_type = db.Column(db.String(5000))
    student = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))
    amount = db.Column(db.String(400))
    cls = db.Column(db.String(400))
    method = db.Column(db.String(400))
    paid_by = db.Column(db.String(400))
    date = db.Column(db.String(400))
    balance = db.Column(db.String(400))
    student_number = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    

class ExamAttendance(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    class_name = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    subject_name = db.Column(db.String(5000))
    student_number = db.Column(db.String(400))
    status = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    exam_name = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    term = db.Column(db.String(400))
    year = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  

class Schedule(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    class_name = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    from_time = db.Column(db.String(5000))
    to_time = db.Column(db.String(400))
    date = db.Column(db.String(400))
    section = db.Column(db.String(400))
    exam_name = db.Column(db.String(400))
    subject_name = db.Column(db.String(400))
   
    room = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
class Expenses(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    amount = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400)) 
    school_name = db.Column(db.String(400))
    user = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
      
class Income(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    amount = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  


class Event(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  



class Holiday(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  


class Notice(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    role = db.Column(db.String(400))
    school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  


class Noticer(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    role = db.Column(db.String(400))
    school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  


class Subject(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(5000),unique =True)
    department_name = db.Column(db.String(5000))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
class Subjectc(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(5000))
    department_name = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    


class Class(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    class_name =db.Column(db.String(500))
    staff_number = db.Column(db.String(500))
    course_name=db.Column(db.String(500))
    subject_name=db.Column(db.String(500))
    created_date =db.Column(db.String(5000))
    class_size =db.Column(db.String(400))
    school_name = db.Column(db.String(400))
    roll_number = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    



class Payment(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        transaction_id= db.Column(db.String(5000),unique=True)
        amount_paid=db.Column(db.String(5000))

    
        balance=db.Column(db.String(5000))
        paid_by=db.Column(db.String(5000))
        payent_date=db.Column(db.String(5000))
        payment_method=db.Column(db.String(5000))
        student_name= db.Column(db.String(5000))
        pay_refund = db.relationship('Refund',
                                    foreign_keys='Refund.payment_id',
                                     backref = 'refundpayie',
                                     lazy=True  )
       
      
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))


class Attendance(db.Model):
          id =db.Column(db.Integer,primary_key=True)
          attendace_date =db.Column(db.String(400))
          attendance_counter =db.Column(db.String(400))
          name =db.Column(db.String(400))
          role =  db.Column(db.String(400))
       
        
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))

      
      



class School(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        school_name= db.Column(db.String(400))
        school_anthem= db.Column(db.String(400))
        established_year= db.Column(db.String(400))
        logo= db.Column(db.String(1000000))
       
        mail= db.Column(db.String(400))
        level= db.Column(db.String(400))
        address = db.Column(db.String(400))
        region = db.Column(db.String(5000))
        population = db.Column(db.String(400))
        motto= db.Column(db.String(5000))

        headmaster= db.Column(db.String(400))
        color_one= db.Column(db.String(400))
        color_two= db.Column(db.String(400))
        color_three= db.Column(db.String(400))
        username = db.Column(db.String(400))
        password = db.Column(db.String(400))
        district = db.Column(db.String(400))
        circuit = db.Column(db.String(400))
        phone = db.Column(db.String(400))
        created_date = db.Column(db.String(400))
       
  
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



       


class Refund(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          refund_amount =  db.Column(db.String(400))  
          student_name = db.Column(db.String(400))
          status  = db.Column(db.String(400))
          refund_time = db.Column(db.String(400))
          
          payment_id =  db.Column(db.Integer,db.ForeignKey('payment.id'))
          reason  = db.Column(db.String(400))
          authorized_by  = db.Column(db.String(400))
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))

       




class PendingGrade(db.Model):
           
          id = db.Column(db.Integer,primary_key=True)
       
          subject_name=  db.Column(db.String(400))
     
          term  = db.Column(db.String(400))
          class_score = db.Column(db.String(400))
          class_name = db.Column(db.String(400))
          total = db.Column(db.String(5000))
          exams_score =  db.Column(db.String(400))
         
          created_date  = db.Column(db.String(400))
          grade_id = db.Column(db.String(400))
          school_name = db.Column(db.String(5000))
          staff_number = db.Column(db.String(5000))
          student_number = db.Column(db.String(5000))

          status =   db.Column(db.String(400))
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))



class BroadSheet(db.Model):
           
          id = db.Column(db.Integer,primary_key=True)
          student_name = db.Column(db.String(400))
         
          english  = db.Column(db.String(400))
          math  = db.Column(db.String(400))
          science = db.Column(db.String(400))
          socialstudies = db.Column(db.String(400))
          ghanalanguage = db.Column(db.String(400))
          creativeart = db.Column(db.String(400))
          social = db.Column(db.String(400))
          rme = db.Column(db.String(5000))
          careertech =  db.Column(db.String(400))
          pos =  db.Column(db.String(400))
          created_date  = db.Column(db.String(400))
          all_total =  db.Column(db.String(400))
          computing=db.Column(db.Integer)
          school_name = db.Column(db.String(5000))
          original_class_name =db.Column(db.String(5000))
          french = db.Column(db.String(5000))
          student_number = db.Column(db.String(5000))
          year = db.Column(db.String(5000))
          term = db.Column(db.String(5000))
          pos =  db.Column(db.String(400))
          class_name =db.Column(db.String(400))
         
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))





class Grading(db.Model):
           
          id = db.Column(db.Integer,primary_key=True)
          rank = db.Column(db.String(400))
          subject_name=  db.Column(db.String(400))
          remark  = db.Column(db.String(400))
          term  = db.Column(db.String(400))
          class_score = db.Column(db.String(400))
          class_name = db.Column(db.String(400))
          original_class_name =db.Column(db.String(5000))
          total = db.Column(db.String(5000))
          exams_score =  db.Column(db.String(400))
          pos =  db.Column(db.String(400))
          created_date  = db.Column(db.String(400))
          all_total =  db.Column(db.String(400))
          name=db.Column(db.String(400))
          school_name = db.Column(db.String(5000))
          grade = db.Column(db.String(5000))
          student_number = db.Column(db.String(5000))
          year = db.Column(db.String(5000))
          pos =  db.Column(db.String(400))
          change_request =  db.Column(db.String(400))
         
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))


class MailSetup(db.Model):
           
          id = db.Column(db.Integer,primary_key=True)
          working_mail = db.Column(db.String(400))
          push_notification=  db.Column(db.String(400))
          bulk_message  = db.Column(db.String(400))
          status = db.Column(db.String(400))
          school_name = db.Column(db.String(400))
          created_date = db.Column(db.String(400))
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))


class Remark(db.Model):
           
          id = db.Column(db.Integer,primary_key=True)
          teacher_remark = db.Column(db.String(400))
          year = db.Column(db.String(400))
          attitude=  db.Column(db.String(400))
          interest  = db.Column(db.String(400))
          attendance = db.Column(db.String(400))
          class_name = db.Column(db.String(400))
          class_term = db.Column(db.String(400))
        #   term = db.Column(db.String(400))
         
          created_date  = db.Column(db.String(400))
          school_name = db.Column(db.String(5000))
          
          student_number = db.Column(db.String(5000))
          created_by_id  = db.Column(db.Integer,db.ForeignKey('user.id'))
          

class Scheme(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(5000))
    midterm_score = db.Column(db.String(5000))
    exams_score = db.Column(db.String(5000))
    class_score = db.Column(db.String(5000))
    school_name = db.Column(db.String(5000))
    created_date  = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
  
  
  
  

class Academic(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    year =db.Column(db.String(500))
    term=db.Column(db.String(500))
    closing_date=db.Column(db.String(500))
    created_date =db.Column(db.String(5000))
    reopening_date =db.Column(db.String(400))
    status =db.Column(db.String(400))
    school_name = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
