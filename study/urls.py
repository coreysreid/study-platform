from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Course URLs
    path('my-courses/', views.course_list, name='course_list'),
    path('courses/', views.course_list, name='course_list_legacy'),  # Backward compatibility
    path('catalog/', views.course_catalog, name='course_catalog'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('course/<int:course_id>/status/', views.update_enrollment_status, name='update_enrollment_status'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    
    # Topic URLs
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topic/create/', views.topic_create, name='topic_create'),
    path('topic/create/<int:course_id>/', views.topic_create, name='topic_create_for_course'),
    path('topic/<int:topic_id>/edit/', views.topic_edit, name='topic_edit'),
    
    # Flashcard URLs
    path('flashcard/create/', views.flashcard_create, name='flashcard_create'),
    path('flashcard/create/<int:topic_id>/', views.flashcard_create, name='flashcard_create_for_topic'),
    path('flashcard/<int:flashcard_id>/edit/', views.flashcard_edit, name='flashcard_edit'),
    
    # Study Session URLs
    path('study/<int:topic_id>/', views.study_session, name='study_session'),
    path('session/<int:session_id>/end/', views.end_study_session, name='end_study_session'),
    path('flashcard/<int:flashcard_id>/progress/', views.update_flashcard_progress, name='update_flashcard_progress'),
    
    # Statistics
    path('statistics/', views.statistics, name='statistics'),
    
    # Study Mode Preferences
    path('study-mode/update/', views.update_study_mode, name='update_study_mode'),
]
