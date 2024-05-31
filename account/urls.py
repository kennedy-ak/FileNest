from django.urls import path
from . import views

urlpatterns = [  
    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-upload/', views.upload_file, name='upload_file'),
    path('admin-stats/', views.file_statistics, name='file_statistics'),
    path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('send-file/<int:file_id>/', views.send_file_via_email, name='send_file'),
    path("",views.user_login,name='login'),
    path("register/",views.user_register,name='register'),
    path('logout',views.user_logout,name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_change/',views.change_password,name ='password_change'),
    path('password_change_done/',views.change_password_done,name='password_changed'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('files/download/<int:file_id>/', views.download_file, name='download_file'),
    path('dashboard',views.dashboard,name="dashboard"),
    # path("",views.homepage,name='homepage'),
   
]