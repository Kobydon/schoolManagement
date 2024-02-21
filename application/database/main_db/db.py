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
    email = db.Column(db.String(255),unique=True)
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
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
 
    
    
    staff_by  = db.relationship('Staff', 
    foreign_keys ='Staff.created_by_id',
    backref = 'staffie',
    lazy=True
    
    )
    
    
    
    


    course_by  = db.relationship('Course', 
    foreign_keys ='Course.created_by_id',
    backref = 'coursie',
    lazy=True
    
    )
 
    
    
    depar_by  = db.relationship('Department', 
    foreign_keys ='Department.created_by_id',
    backref = 'deparie',
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
    
                    
    Attendance_by  = db.relationship('Attendace', 
    foreign_keys ='Attendace.created_by_id',
    backref = 'attendie',
    lazy=True)
          
                    
    Academic_by  = db.relationship('Academic_Calender', 
    foreign_keys ='Academic_Calender.created_by_id',
    backref = 'acadamecie',
    lazy=True)
    
    Class_by  = db.relationship('Class', 
    foreign_keys ='Class.created_by_id',
    backref = 'classie',
    lazy=True)
    
    school_by  = db.relationship('School', 
    foreign_keys ='School.created_by_id',
    backref = 'schoolie',
    lazy=True)
    
    
    
    
    



class Student(db.Model):
          id= db.Column(db.Integer,primary_key=True)
          first_name= db.Column(db.String(400))
          student_number= db.Column(db.String(400),unique=True)
          last_name= db.Column(db.String(400))
          admitted_year= db.Column(db.String(400))
          parent_name= db.Column(db.String(400))
          email= db.Column(db.String(400),unique=True)
          address= db.Column(db.String(400))
          password= db.Column(db.String(400))
          parent_phone= db.Column(db.String(400))
          admitted_year= db.Column(db.String(400))
          form= db.Column(db.String(400))
          residential_status= db.Column(db.String(400))
          created_date = db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
              
        #   student_pay  = db.relationship('Payment', 
        #     foreign_keys ='Payment.student_name',
        #     backref = 'studiepay',
        #     lazy=True
            
        #     )
     

         


class Staff(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      firtname = db.Column(db.String(400))
      lastname = db.Column(db.String(400))
      email = db.Column(db.String(400),unique=True)
      phone = db.Column(db.String(400))
      address = db.Column(db.String(400))
      department = db.Column(db.String(400))
      staff_number = db.Column(db.String(400),unique=True)
      national_id = db.Column(db.String(400),unique=True)
      subject_name = db.Column(db.Integer,db.ForeignKey('subject.name'))
      bank_name = db.Column(db.String(400))
      bank_account_number = db.Column(db.String(400))
      bank_branch = db.Column(db.String(400))
      course_name = db.Column(db.String(400))
      residential_status = db.Column(db.String(400))
      appointment_date = db.Column(db.String(400))
      year_joined = db.Column(db.String(400))
      subject = db.Column(db.String(400))
      created_date = db.Column(db.String(400))
      created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
      
      staff_class  = db.relationship('Class', 
            foreign_keys ='Class.staff_id',
            backref = 'classStaffie',
            lazy=True
            
            )
     


class Department(db.Model):
          id =db.Column(db.Integer,primary_key=True)
          department_name =db.Column(db.String(400),unique=True)
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
     
          
         
         
          created_date =db.Column(db.String(400))
                
          depa_couse  = db.relationship('Course', 
            foreign_keys ='Course.department_name',
            backref = 'studie',
            lazy=True
            
            )
 
         


class Course(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          course_name = db.Column(db.String(400))
          course_id = db.Column(db.String(400),unique=True)
          department_name = db.Column(db.Integer,db.ForeignKey('Department.name'))
          form = db.Column(db.String(400))    
     
          
          created_date =db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
        
          course_class  = db.relationship('Class', 
            foreign_keys ='Class.course_name',
            backref = 'clascoursie',
            lazy=True
            
            )




class Subject(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    subject_name = db.Column(db.String(5000))
    course_subj  = db.relationship('Grading', 
            foreign_keys ='Grading.subject_name',
            backref = 'gradie',
            lazy=True
            
            )
    staff_sub  = db.relationship('Staff', 
            foreign_keys ='Staff.subject_name',
            backref = 'gradie',
            lazy=True
            
            )
 
    
    



class Class(db.Model):
    id =db.Column(db.Integer,primary_key=True)
 
    staff_id = db.Column(db.ForeignKey('staff.staff_id'))
    course_name=db.Column(db.ForeignKey('course.course_name'))
   
    created_date =db.Column(db.String(5000))
   

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
        location = db.Column(db.String(5000))
        population = db.Column(db.String(400))
        motto= db.Column(db.String(5000))

        headmaster= db.Column(db.String(400))
        color_one= db.Column(db.String(400))
        color_two= db.Column(db.String(400))
        color_three= db.Column(db.String(400))
  
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



       


class Refund(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          refund_amount =  db.Column(db.String(400))  
          student_name = db.Column(db.String(400))
          status  = db.Column(db.String(400))
          refund_time = db.Column(db.String(400))
          
          payment_id =  db.Column(db.ForeignKey('payment.id'))
          reason  = db.Column(db.String(400))
          authorized_by  = db.Column(db.String(400))
