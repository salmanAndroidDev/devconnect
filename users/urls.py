from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_user, name='register'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('account/', views.user_account, name='account'),
    path('edit-account', views.edit_account, name='edit_account'),
    path('create-skill/', views.create_skill, name='create_skill'),
    path('update-skill/<pk>/', views.update_skill, name='update_skill'),
    path('delete-skill/<pk>/', views.delete_skill, name='delete_skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<pk>/', views.view_message, name='view_message'),
    path('send-message/<pk>/', views.send_message, name='send_message'),
]