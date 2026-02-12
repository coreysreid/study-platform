from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('study/<int:topic_id>/', views.study_session, name='study_session'),
    path('session/<int:session_id>/end/', views.end_study_session, name='end_study_session'),
    path('flashcard/<int:flashcard_id>/progress/', views.update_flashcard_progress, name='update_flashcard_progress'),
    path('statistics/', views.statistics, name='statistics'),
]
