from django.urls import path
from .views import (
    RegisterSendOTPView, RegisterVerifyAndSetPasswordView,
    LoginView, 
    ForgotPasswordSendOTPView, ResetPasswordView , UserProfileView
)

urlpatterns = [
    path('register/send-otp/', RegisterSendOTPView.as_view(), name='register-send-otp'),
    path('register/verify/', RegisterVerifyAndSetPasswordView.as_view(), name='register-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/send-otp/', ForgotPasswordSendOTPView.as_view(), name='forgot-send-otp'),
    path('forgot-password/reset/', ResetPasswordView.as_view(), name='forgot-reset'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]