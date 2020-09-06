from django.shortcuts import render,redirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings
from . import views
from .forms import UserRegisterForm, EditProfileForm,EditScholarshipForm,PersonalInfoForm,EducationalInfoForm,AgreeInfoForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Support, ScholarshipDetails,Personal_Info,Educational_Info,Agree_Info,Applied_Scholarships,Events
from django.contrib.sessions.middleware import SessionMiddleware

# Create your views here.

def home(request):
    #dashboard of students
    govt_schdets = ScholarshipDetails.objects.filter(type = 'Government')
    pvt_schdets = ScholarshipDetails.objects.filter(type = 'Private')
    events = Events.objects.all().order_by('-date')
    args = {'user':request.user,'govt_schdets':govt_schdets,'pvt_schdets':pvt_schdets,'events':events}
    return render(request,'dashboard.html',args)

@login_required
def admin_dash(request):
    #admin dashboard
    applied = Applied_Scholarships.objects.filter(status = 'Applied')
    count = 0
    for applied in applied.iterator():
        count=count+1
    args = {'count':count}
    return render(request,'admin-dashboard.html',args)

@login_required
def admin_addscholarship(request):
    #for admin to add scholarship
    if request.method == 'POST':
        print('Scholarship added successfully')
        name = request.POST['sch_name']
        type = request.POST['sch_type']
        date = request.POST['sch_end_date']
        income = request.POST['income']
        qualification = request.POST['qualification']
        department = request.POST['sch_dept']
        category = request.POST['category']
        aim = request.POST['sch_aim']
        reward = request.POST['sch_reward']
        link = request.POST['sch_link']
        helpline = request.POST['sch_helpline']
        amount = request.POST['sch_amount']
        gender = request.POST['gender']

        if date:
            scholarship = ScholarshipDetails(name = name,type = type,end_date = date,income = income,qualification = qualification,
                                            department = department,aim = aim,link = link,helpline = helpline,
                                            category = category,reward = reward,amount = amount,gender = gender)
            if not ScholarshipDetails.objects.filter(name = name,type = type,department = department,category=category).exists():
                scholarship.save()
                messages.success(request,'You have successfully added a scholarship')

            elif ScholarshipDetails.objects.filter(name = name,type = type,department = department).exists():
                messages.warning(request,'Scholarship already exists')
                print('scholarship already exists') 
        else:
            messages.warning(request,'Please fill all the details properly')
            redirect('/admin/addscholarship')
       
                                

    return render(request,'admin-addscholarship.html')


def admin_editscholarship(request):
    schdets=None
    if request.method == 'POST':
        id = request.POST['sch_id']
        
        schdets = ScholarshipDetails.objects.filter(id = id)
        if schdets is not None:
            print('Scholarship found')

        else:
            schdets = None

    
        
    #to edit scholarships in database
    return render(request,'admin-editscholarship.html',{'schdets':schdets})

def admin_updatescholarship(request,pk=None):
    #can update the new data in the selectd scholarship
    if pk:
        sch = ScholarshipDetails.objects.get(pk = pk)
    
    
    if request.method == 'POST':
        form = EditScholarshipForm(request.POST,instance=sch)
        if form.is_valid():
            form.save()
            print('\nform saved')
            args = {'form' : form}

            messages.success(request,'Successfully updated')
            #return render(request,'admin-editscholarship.html',args)
 
            return redirect('/admin/editscholarship')
    else:
        form = EditScholarshipForm(instance=sch)
        args = {'form' : form}
        return render(request,'admin-updatescholarship.html',args)

def admin_students(request):
    #shows all the students
    val = 'False'
    
    user_details = User.objects.filter(is_superuser = val)
    # for user in users.iterator():
    #     users_.append(users)
    # print(users_)
    paginator = Paginator(user_details,10)
    page = request.GET.get('page')
    user_details = paginator.get_page(page)
    args = {'users':user_details}
    return render(request,'admin-students.html',args)

def admin_studentsinfo(request,enrol = None):
    if enrol:
        print(enrol)
    personal_ = []
    education_ = []
    sch_ = []
    applied_ = []
    user = None
    zipped_data = None
    sch_dets = None
    if Personal_Info.objects.filter(enrolment = enrol).exists():
        personal = Personal_Info.objects.get(enrolment = enrol)
        user_id = personal.user_id
        personal_.append(personal)
        education = Educational_Info.objects.get(user_id = user_id)
        education_.append(education)
        if Applied_Scholarships.objects.filter(user_id = user_id):
            applied = Applied_Scholarships.objects.filter(user_id = user_id)
            
            for applied in applied.iterator():
                applied_.append(applied)
                sch_id = applied.scholarship_id
                sch = ScholarshipDetails.objects.get(id = sch_id)
                print(sch)
                sch_.append(sch)
            sch_dets = zip(applied_,sch_)
            
        zipped_data = zip(personal_,education_)
    else:
        user = User.objects.get(username = enrol)


    args = {'zipped_data' : zipped_data,'user_details':user,'sch_dets':sch_dets}
    return render(request,'admin-studentsinfo.html',args)

def admin_requests(request):
    
    id = request.user.id
    print(id)
    schdets_ = []
    applied_ = []
    
    applied = Applied_Scholarships.objects.filter(status = 'Applied')
    args={'applied':applied}

    for applied in applied.iterator():
        user_id = applied.user_id
        applied_.append(applied)
        sch_id = applied.scholarship_id
        print(sch_id)
        schdets = ScholarshipDetails.objects.get(id = sch_id)
        schdets_.append(schdets)
        

    if applied:  
        zipped_data = zip(applied_,schdets_)
    else:
        zipped_data = None
    
    args = {'zipped_data':zipped_data}

    if request.method=='POST':
        if 'approve' in request.POST:
            val = request.POST.get('approve')
            print(val)
            applied = Applied_Scholarships.objects.get(id = val)
            
            applied.status = 'Approved'
            applied.save()

            print('saved')
            return redirect('/admin/requests')
        elif 'reject' in request.POST:
            val = request.POST.get('reject')
            print(val)
            applied = Applied_Scholarships.objects.get(id = val)
            
            applied.status = 'Rejected'
            applied.save()

            print('saved')
            return redirect('/admin/requests')
    return render(request,'admin-requests.html',args)

def admin_feedbacks(request):
    feedbacks = Support.objects.all()
    args = {'feedback':feedbacks}

    return render(request,'admin-feedbacks.html',args)

def admin_statistics(request):
    sum=0
    num=0
    applied = Applied_Scholarships.objects.filter(status = 'Approved')
    for applied in applied.iterator():
        print(applied)
        num = num + 1
        id = applied.scholarship_id
        sch = ScholarshipDetails.objects.get(id = id)
        sum = sum + sch.amount
        print(sum)

    applied_num = 0
    applied = Applied_Scholarships.objects.all()
    for applied in applied.iterator():
        applied_num = applied_num + 1

    reg_users = 0
    register = User.objects.filter(is_superuser = 'False')
    for register in register.iterator():
        reg_users = reg_users + 1

    student_num = set()
    applied = Applied_Scholarships.objects.filter(status = 'Approved')
    print(applied)
    for applied in applied.iterator():
        id = applied.user_id
        student_num.add(id)
    print(student_num)
    num = len(student_num)
    print('length of set = ',num)

    args = {'total_amount':sum,'approved_sch_num':num,'applied_sch_num':applied_num,'reg_users':reg_users,'num':num}
    return render(request,'admin-statistics.html',args)

def admin_events(request):
    if request.method == 'POST':
        name = request.POST['event']
        event = Events(name = name)
        event.save()
        
        messages.success(request,'You have successfully added an event')
        recipient_list = []
        u = User.objects.all()
        for u in u.iterator():
            email = u.email
            recipient_list.append(email)

        
        subject = 'New Events'
        msg = 'Dear User, Have a look at all the updated events'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject,msg,from_email,recipient_list,fail_silently=False)


    return render(request,'admin-events.html')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    else:
        return None

sum=0
num = 0
applied = Applied_Scholarships.objects.filter(status = 'Approved')
for applied in applied.iterator():
    print(applied)
    num = num + 1
    id = applied.scholarship_id
    sch = ScholarshipDetails.objects.get(id = id)
    sum = sum + sch.amount
    print(sum)

    applied_num = 0
    applied = Applied_Scholarships.objects.all()
    for applied in applied.iterator():
        applied_num = applied_num + 1

    reg_users = 0
    register = User.objects.filter(is_superuser = 'False')
    for register in register.iterator():
        reg_users = reg_users + 1

    student_num = set()
    applied = Applied_Scholarships.objects.filter(status = 'Approved')
    print(applied)
    for applied in applied.iterator():
        id = applied.user_id
        student_num.add(id)
    print(student_num)
    num = len(student_num)
    print('length of set = ',num)


data = {'total_amount':sum,'approved_sch_num':num,'applied_sch_num':applied_num,'reg_users':reg_users,'num':num}

class ViewPDF(View):
    def get(self,request,*args, **kwargs):
        
        pdf = render_to_pdf('abcd.html',data)
        return HttpResponse(pdf,content_type='application/pdf')

class DownloadPDF(View):
    def get(self,request,*args,**kwargs):
        pdf = render_to_pdf('abcd.html',data)
        response = HttpResponse(pdf,content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("Report")
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response

def admin_abcd(request):
    sum=0
    num=0
    applied = Applied_Scholarships.objects.filter(status = 'Approved')
    for applied in applied.iterator():
        print(applied)
        num = num + 1
        id = applied.scholarship_id
        sch = ScholarshipDetails.objects.get(id = id)
        sum = sum + sch.amount
        print(sum)

    applied_num = 0
    applied = Applied_Scholarships.objects.all()
    for applied in applied.iterator():
        applied_num = applied_num + 1

    reg_users = 0
    register = User.objects.filter(is_superuser = 'False')
    
    print(register)

    student_num = set()
    applied = Applied_Scholarships.objects.filter(status = 'Approved')
    print(applied)
    for applied in applied.iterator():
        id = applied.user_id
        student_num.add(id)
    print(student_num)
    num = len(student_num)
    print('length of set = ',num)

    args = {'total_amount':sum,'approved_sch_num':num,'applied_sch_num':applied_num,'reg_users':reg_users,'num':num}
    return render(request,'abcd.html',args)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username,password=password)

        if user is not None:
            if username == 'admin':
                auth.login(request,user)
                id = user.id
                print(id)
                return redirect('/admin/dashboard')
            else:
                auth.login(request,user)
                id = user.id
                print(id) 

                
                
                return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('/accounts/login')

    else:
        return render(request,'pages-login.html')


def register(request):
    print("reg")
    if request.method == 'POST':
        print("post")
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            enrolment = form.cleaned_data.get('enrolment')
            print('user created')
            #send_mail(subject,msg,from email,to list,fail silently=true)
            subject = 'Thankyou for registering'
            message = 'Welcome to this website'
            from_email = settings.EMAIL_HOST_USER
            to_list = [form.cleaned_data.get('email') ,settings.EMAIL_HOST_USER]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            messages.success(request,f'Account created for {first_name}!')
           
            print("valid")
            
            return redirect('/accounts/login')
    else:    
        print("invalid")
        form = UserRegisterForm()
    return render(request,'pages-register.html',{'form':form})

def logout(request):
    auth.logout(request)
    return render(request,'pages-logout.html')


#open this when you use forms
@login_required
def es(request):
    id = request.user.id
    print(request.user.username)
    username = request.user.username

    if not request.method == 'POST' :
        
        if Personal_Info.objects.filter(user_id = id).exists():
            print('registration done')
            args = None
            family_income = Personal_Info.objects.get(user_id = id).family_income
            print(family_income)
            highest_qualification = Personal_Info.objects.get(user_id = id).highest_qualification
            print(highest_qualification)
            category = Personal_Info.objects.get(user_id = id).category
            print(category)
            

            if ScholarshipDetails.objects.filter(income = family_income,qualification=highest_qualification,
                                                    category=category).exists():
                eligible = ScholarshipDetails.objects.filter(income = family_income,qualification=highest_qualification,
                                                    category=category)
                eligible_scholarships_ = []
                count_ =[]
                count = 0
                
                for eligible in eligible.iterator():
                    el_id = (eligible.id)
                    count = count + 1
                    count_.append(count)
                    print('id of scholarship ',el_id)
                    if Applied_Scholarships.objects.filter(user_id = id,scholarship_id = eligible.id).exists():
                        print('hi')
                    else:
                        eligible_scholarships_.append(eligible)
                
                    if eligible_scholarships_:
                        zipped_data = zip(eligible_scholarships_,count_)
                    else:
                        zipped_data = 0
                
                    temp = {'zipped_data':zipped_data}
                    print(zipped_data)
                 
            if not zipped_data:
                temp = {'not_eligible':'not eligible'}
                print(temp)   

            return render(request,'eligible-scholarships.html',temp)

        
        else:
            print('post request',id)
            personal_form = PersonalInfoForm()
            educational_form = EducationalInfoForm()
            agree_form = AgreeInfoForm()
            args = {'personal_form':personal_form,'educational_form':educational_form,'agree_form':agree_form}
            return render(request,'eligible-scholarships.html',args)

    
    else:
        id = request.user.id


        if not Personal_Info.objects.filter(user_id = id).exists():
            if not Educational_Info.objects.filter(user_id = id).exists():
                if not Agree_Info.objects.filter(user_id = id).exists():
 
                    print('inside post')
                    enrolment = username
                    first_name = request.POST['first_name']
                    middle_name = request.POST['middle_name']
                    last_name = request.POST['last_name']
                    date_of_birth = request.POST['date_of_birth']
                    gender = request.POST['gender']
                    address = request.POST['address']
                    family_income = request.POST['family_income']
                    request.session['family_income'] = family_income
                    category = request.POST['category']
                    request.session['category'] = category
                    highest_qualification = request.POST['highest_qualification']
                    request.session['highest_qualification'] = highest_qualification


                    personal = Personal_Info(enrolment=enrolment,first_name=first_name,middle_name=middle_name,last_name=last_name,
                                            date_of_birth=date_of_birth,gender=gender,address=address,user_id = id,
                                            family_income=family_income,category=category,highest_qualification=highest_qualification )
                    personal.save()
                    

                    ssc_marks = request.POST['ssc_marks']
                    ssc_percentage = request.POST['ssc_percentage']
                    ssc_board = request.POST['ssc_board']
                    hsc_marks = request.POST['hsc_marks']
                    hsc_percentage = request.POST['hsc_percentage']
                    hsc_board = request.POST['hsc_board']
                    college_name = request.POST['college_name']
                    university = request.POST['university']
                    semester = request.POST['semester']

                    educational = Educational_Info(user_id = id,ssc_marks=ssc_marks,ssc_percentage=ssc_percentage,ssc_board=ssc_board,
                                                        hsc_marks = hsc_marks,hsc_percentage=hsc_percentage,hsc_board=hsc_board,
                                                        college_name=college_name,university=university,semester=semester)
                            
                    educational.save()
                    agree = request.POST['agree']
                    if agree == 'on':
                        agree = 'True'
                        print(agree)
                        agree = Agree_Info(user_id = id,agree = agree)
                        agree.save()
                    else:
                        agree = 'False'
                else:
                    print('agree details already exists')
            else:
                print('educational details already exists')
        else:
            print('personal details already exists')
        print('all details saved successfully')
        return redirect('/dashboard')

    
    return render(request,'eligible-scholarships.html')

def scholarship_details(request,id=None):
    scholarship = ScholarshipDetails.objects.get(id = id)
    args = {'scholarship':scholarship}
    return render(request,'scholarship_details.html',args)

@login_required
def appsc(request):

    # if id:
    #     applied = Applied_Scholarships.objects.get(scholarship_id = id,user_id = request.user.id)
    #     applied.delete()
    #     return redirect('/es')
    
        allapplied = Applied_Scholarships.objects.filter(user_id = request.user.id)
        list_ = []
        status_ = []
        for applied in allapplied.iterator():
            print('hi')
            sch_id = applied.scholarship_id
            queryset = list(ScholarshipDetails.objects.filter(id = sch_id))
            status = applied.status
            print(status)
            status_.append(status)
            print(queryset[0])
            list_.append(queryset[0])

        if list_:
            zipped_data = zip(list_,status_)
        else:
            zipped_data = None
        context = {'zipped_data':zipped_data} 
        return render(request,'applied-scholarships.html',context)

def reapply(request,id=None):
    if id:
        print(id)
        applied = Applied_Scholarships.objects.get(user_id = request.user.id,scholarship_id = id)
        print(applied)
        applied.delete()
    return redirect('/as')

def support(request):
    if request.method == 'POST':
        print("form is submitted")
        if request.user.is_authenticated:
            name = request.user.first_name
            email = request.user.email
        else:
            name = request.POST['name'] 
            email = request.POST['email']
        message = request.POST['message']

        support =  Support(name = name,email=email,message=message)

        support.save()
        messages.success(request,'You have successfully submitted your message')
        
    return render(request,'support.html')

@login_required
def profile(request):
    args = {'user' : request.user}
    return render(request,'profile.html',args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form  = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form' : form}
        return render(request,'edit_profile.html',args)

def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST,user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return redirect('editpassword')
    else:
        form = PasswordChangeForm(user = request.user)

        args = {'form':form}
        return render(request, 'edit-password.html',args)


def admin_editpassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST,user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/admin/profile')
        else:
            return redirect('/admin/editpassword')
    else:
        form = PasswordChangeForm(user = request.user)

        args = {'form':form}
        return render(request, 'admin-editpassword.html',args)

#Dummy websites
def HomeGovt(request,sch_id=None):
    if sch_id:
        args = {'sch_id':sch_id}
    return render(request, 'HomeGovt.html',args)

def RegGovt(request,sch_id=None):
   
    if not Applied_Scholarships.objects.filter(user_id = request.user.id,scholarship_id = sch_id).exists():
        
        if request.method == 'POST':
            scholarship_id = sch_id 
            id = request.user.id
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            print(phone)
            EnrolmentNumber = request.POST.get('EnrolmentNumber')
            print(EnrolmentNumber)
            SSCmarks = request.POST.get('SSCmarks')
            print(SSCmarks)
            HSCmarks = request.POST.get('HSCmarks')
            print(HSCmarks)
            College = request.POST.get('CollegeName')
            Board = request.POST.get('Board')
            Semester = request.POST.get('Semester')
            dept = request.POST.get('dept')
            icerti = request.POST.get('icerti')
            ccerti = request.POST.get('ccerti')
            pp = request.POST.get('pp')
            status = 'Applied'

            applied = Applied_Scholarships(scholarship_id = scholarship_id,user_id = id,first_name = fname,last_name = lname,gender = gender,dob = dob,address = address,
                                            phone = phone,enrolment = EnrolmentNumber,ssc_marks = SSCmarks,hsc_marks = HSCmarks,
                                            college_name = College,board = Board,semester = Semester,department = dept,
                                            income_certificate = icerti,caste_certificate = ccerti,passport_photo = pp,status = status)
            
            
            applied.save()
            return redirect('/government/done')
    
   
    
    else:
        print('scholarship already applied')
    return render(request, 'RegGovt.html')

# def ConfGovt(request):
#     args = request.session.get('applied_scholarship')
#     if request.method == 'POST':
       
#         return redirect('/government/done')
#     return render(request,'ConfGovt.html')

def DoneGovt(request):
    return render(request,'DoneGovt.html')
    

def generate(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100,100,"Hello world.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=True,filename = 'hello.pdf')