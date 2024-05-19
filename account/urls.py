from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.user_login,name='login'),
    path("register/",views.user_register,name='register'),
    path('logout',views.user_logout,name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_change/',views.change_password,name ='password_change'),
    path('password_change_done/',views.change_password_done,name='password_change_done'),
    # path('password_reset',views.password_reset,name='password_reset'),
    # path('reset/<uidb64>/<token>',views.passwordResetConfirm, name='password_reset_confirm',),
   path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Other paths...
        
    
    path('',views.dashboard,name="dashboard")
]
