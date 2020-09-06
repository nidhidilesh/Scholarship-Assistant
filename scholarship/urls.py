from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('',views.home),
    path('accounts/login',views.login),
    path('accounts/register',views.register),
    path('dashboard',views.home),
    path('accounts/logout',views.logout),
    path('es',views.es),
    path('as',views.appsc,name='as'),
    url(r'^reapply/(?P<id>\d+)$',views.reapply,name='reapply'),
    path('sp',views.support),
    url(r'^scholarship/(?P<id>\d+)$',views.scholarship_details,name='scholarship'),
    path('profile',views.profile,name = 'profile'),
    path('editprofile',views.edit_profile,name = 'editprofile'),
    path('editpassword',views.edit_password,name = 'editpassword'),
    path('password_reset',PasswordResetView.as_view(template_name = 'password-reset.html'),name = 'password_reset'),
    path('password_reset/done',PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'),name = 'password_reset_done'),
    path('reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),name = 'password_reset_confirm'),
    path('reset/done/#',PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'),name = 'password_reset_complete'),

    #for admin
    path('admin/dashboard',views.admin_dash),
    path('admin/addscholarship',views.admin_addscholarship),
    path('admin/editscholarship',views.admin_editscholarship),
    url(r'^admin/updatescholarship/(?P<pk>\d+)$',views.admin_updatescholarship,name = 'updatescholarship'),
    path('admin/students',views.admin_students),
    path('admin/requests',views.admin_requests),
    path('admin/generate',views.generate),
    url(r'^admin/studentsinfo/(?P<enrol>\d+)$',views.admin_studentsinfo,name='studentsinfo'),
    path('admin/statistics',views.admin_statistics),
    path('admin/pdf_view',views.ViewPDF.as_view(),name="pdf_view"),
    path('admin/pdf_download',views.DownloadPDF.as_view(),name="pdf_downlaod"),
    path('admin/abcd',views.admin_abcd),
    path('admin/editpassword',views.admin_editpassword),
    path('admin/password_reset',PasswordResetView.as_view(template_name = 'password-reset.html'),name = 'password_reset'),
    path('admin/password_reset/done',PasswordResetDoneView.as_view(template_name = 'admin_password_reset_done.html'),name = 'password_reset_done'),
    path('admin/reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'),name = 'password_reset_confirm'),
    path('admin/reset/done/#',PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'),name = 'password_reset_complete'),
    path('admin/events',views.admin_events),
    path('admin/feedbacks',views.admin_feedbacks),




     #for dummy websites
    url(r'^government/home/(?P<sch_id>\d+)$',views.HomeGovt,name="home"),
    url(r'^government/register/(?P<sch_id>\d+)$',views.RegGovt,name="register"),
    # path('government/confirm',views.ConfGovt),
    path('government/done',views.DoneGovt)


]