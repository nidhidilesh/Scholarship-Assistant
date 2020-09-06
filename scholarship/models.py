from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
# make classes here


class Support(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    

class ScholarshipDetails(models.Model):
    name = models.CharField(max_length=2000)
    updated_name = models.CharField(max_length=2000,null = True)
    type = models.CharField(max_length=200)
    end_date = models.DateField(null=False)
    updated_end_date = models.DateField(null=True)
    income = models.CharField(max_length=200)
    qualification = models.CharField(max_length=2000)
    category = models.CharField(max_length=2000)
    reward = models.CharField(max_length=2000)
    department = models.CharField(max_length=2000)
    aim = models.CharField(max_length=2000)
    link = models.CharField(max_length=2000)
    updated_link = models.CharField(max_length=2000,null=True)
    helpline = models.CharField(max_length=200)
    updated_helpline = models.CharField(max_length=200,null = True)
    amount = models.IntegerField()
    gender = models.CharField(max_length=300)

    def __str__(self):
        return self.name



  

class Personal_Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT)
    enrolment = models.CharField(max_length=150,null=True)
    first_name = models.CharField(max_length=200,null=True)
    middle_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=200,null=True)
    address = models.TextField(max_length=2000,null=True)
    family_income = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True)
    highest_qualification = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.first_name

class Educational_Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT)
    ssc_marks = models.IntegerField()
    ssc_percentage = models.IntegerField(max_length = 100)
    ssc_board = models.CharField(max_length=200)
    hsc_marks = models.IntegerField(null=True)
    hsc_percentage = models.IntegerField(max_length=100,null=True)
    hsc_board = models.CharField(max_length=200,null=True)
    college_name = models.CharField(max_length=500)
    university = models.CharField(max_length=200)
    semester = models.IntegerField()

    def __str__(self):
        return self.user

class Agree_Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT)
    agree = models.BooleanField()


    

class Applied_Scholarships(models.Model):
    scholarship_id = models.IntegerField()
    user =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.PROTECT)
    first_name = models.CharField(max_length=200)
    last_name =  models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    dob = models.DateField(null=True)
    address = models.TextField(max_length=2000,null=True)
    phone  = models.BigIntegerField()
    enrolment = models.BigIntegerField()
    ssc_marks = models.IntegerField()
    hsc_marks = models.IntegerField()
    college_name = models.CharField(max_length=500)
    board = models.CharField(max_length=200)
    semester = models.IntegerField()
    department = models.CharField(max_length=200)
    income_certificate = models.ImageField(upload_to='certificate')
    caste_certificate = models.ImageField(upload_to='certificate')
    passport_photo = models.ImageField(upload_to='certificate')
    status = models.CharField(max_length=200)

class Events(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)

class Student_num(models.Model):
    student_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    