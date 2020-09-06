from django import forms
from django.contrib.auth.models import User
from .models import ScholarshipDetails, Personal_Info, Educational_Info, Agree_Info,Events
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    enrolment = forms.IntegerField(max_value=200000000000)
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ['first_name','last_name','enrolment','email','password1','password2']

    def save(self,commit = True):
        user = super(UserRegisterForm,self).save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['enrolment']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    # def __init__(self,*args,**kwargs):
    #     super(EditProfileForm,self).__init__(*args,**kwargs)
    #     del self.fields['password']

        #or to remove password,
        # just set 'password = None' just before Meta and without the init

    password = None
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name'
        ]
        #exclude = ['password']        to exclude the fields




class DateInput(forms.DateInput):
    input_type = 'date'

class IntegerField(forms.DateInput):
    input_type = "number"



# NEEDS REVIEW
class EditScholarshipForm(ModelForm):
    updated_helpline = forms.IntegerField(max_value=200000000000,required = False)
    updated_end_date = forms.DateField(widget=DateInput,required = False)
    updated_name = forms.CharField(max_length=200,required = False)
    updated_link = forms.CharField(max_length=2000,required = False)
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    end_date = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    income = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    qualification = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    aim = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    link = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    helpline = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    reward = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = ScholarshipDetails
        fields = [
            'name',
            'type',
            'end_date',
            'income',
            'qualification',
            'department',
            'aim',
            'link',
            'helpline',
            'amount',
            'gender',
            'category',
            'reward',
            'updated_name',
            'updated_end_date',
            'updated_link',
            'updated_helpline'
        ]

class PersonalInfoForm(ModelForm):

    CHOICES = [('--Select one--','--Select one--'),('Female','Female'),('Male','Male'),('Transgender','Transgender')]
    DROPDOWN = [('--Select one--','--Select one--'),('<1 lakh','<1 lakh'),('between 1 lakh-2 lacs','between 1 lakh-2 lacs'),
                ('between 2 lacs-3 lacs','between 2 lacs-3 lacs'),('between 3 lacs-4 lacs','between 3 lacs-4 lacs'),
                ('between 4 lacs-8 lacs','between 4 lacs-8 lacs'),('>8 lacs','>8 lacs')]
    CATEGORY = [('--Select one--','--Select one--'),('ST','ST'),('SC','SC'),('OBC','OBC'),('Minority','Minority'),('SEBC','SEBC'),('General','General')]
    QUALIFICATION = [('--Select one--','--Select one--'),('10th','10th'),('12th','12th'),('Pursuing a course from a board/university','Pursuing a course from a board/university'),
                    ('Diploma','Diploma')]


    enrolment = forms.IntegerField(widget=forms.HiddenInput)
    family_income = forms.ChoiceField(choices=DROPDOWN,widget=forms.Select)
    category = forms.ChoiceField(choices=CATEGORY,widget=forms.Select)
    date_of_birth = forms.DateField(widget=DateInput)
    highest_qualification = forms.ChoiceField(choices=QUALIFICATION,widget=forms.Select)
    gender = forms.ChoiceField(choices=CHOICES,widget=forms.Select)
    class Meta:
        model = Personal_Info
        fields = [
            'enrolment',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
            'address',
            'family_income',
            'category',
            'highest_qualification'
        ]

class EducationalInfoForm(ModelForm):
    username = forms.IntegerField(widget=forms.HiddenInput())
    hsc_marks = forms.IntegerField(required = False)
    hsc_percentage = forms.IntegerField(required = False)
    hsc_board = forms.CharField(required=False)
    class Meta:
        model = Educational_Info
        fields = [
            'ssc_marks',
            'ssc_percentage',
            'ssc_board',
            'hsc_marks',
            'hsc_percentage',
            'hsc_board',
            'college_name',
            'university',
            'semester'
        ]

class AgreeInfoForm(ModelForm):
    agree = forms.BooleanField(initial=False)
    username = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Agree_Info
        fields = [
            'agree'
        ]




