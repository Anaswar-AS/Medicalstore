
from django.urls import path
from shop import views

urlpatterns = [
path('', views.index, name='home'),
path('add/', views.add_medicine, name='add_medicine'),
path('edit/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
path('delete/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
path('list/', views.medicine_list, name='medicine_list'),
path('search/', views.search_medicine, name='search_medicine'),
path('signup/',views.signup,name='signup'),
path('login/',views.user_login,name='login'),
path('logout/',views.user_logout,name='logout'),

]