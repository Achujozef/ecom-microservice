from django.urls import path
from . import views
from .views import EditUserProfileView,ChangePasswordView

urlpatterns = [
    path('user_login',views.user_login,name="user_login"),
    path('req_singup',views.req_singup,name='req_singup'),
    path('otp_login', views.otp_login, name='otp_login'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
    path('user_detail',views.user_detail,name="user_detail"),
    path('userblock/', views.userblock, name='userblock'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('edituserprofile/', EditUserProfileView.as_view(), name='edituserprofile'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('updateprofileaddress/<int:id>', views.updateprofileaddress, name='updateprofileaddress'),
    path('addprofileaddress/', views.addprofileaddress, name='addprofileaddress'),
    path('user_logout/',views.user_logout,name="user_logout"),
]