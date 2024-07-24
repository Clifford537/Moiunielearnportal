# courses/urls.py
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_topic/<int:course_id>/', views.add_topic, name='add_topic'),
    path('course_list/', views.course_list, name='course_list'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('rate_course/<int:course_id>/', views.rate_course, name='rate_course'),
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),
]
