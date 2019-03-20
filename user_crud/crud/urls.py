from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.users, name='users'),
    path('user/<int:id>/', views.get_user, name='get_user'),
    path('user/new', views.new_user, name='new_user'),
    path('user/update/<int:id>', views.update_user, name='update_user'),
    path('user/delete/<int:id>', views.delete_user, name='delete_user'),
    path('role/<int:id>/', views.get_role, name='get_role'),
]
