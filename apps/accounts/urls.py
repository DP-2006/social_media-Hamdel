# apps/accounts/urls.py

# from django.urls import path
# from .views import (
#     RegisterSendOTPView,
#     VerifyOTPView,
#     LoginSendOTPView,
#     LogoutView
# )

# urlpatterns = [
#     # ثبت‌نام
#     path('register/send-otp/', RegisterSendOTPView.as_view(), name='register-send-otp'),
#     path('register/verify/', VerifyOTPView.as_view(), name='register-verify'),
#     #path('api/accounts/', include('accounts.urls')),      # ← باید اینطوری باشه

    
#     # ورود
#     path('login/send-otp/', LoginSendOTPView.as_view(), name='login-send-otp'),
#     path('login/verify/', VerifyOTPView.as_view(), name='login-verify'),
    
#     # خروج
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]



from django.urls import path
from .views import (
    RegisterSendOTPView,
    VerifyOTPView,
    LoginSendOTPView,
    LogoutView,
)

urlpatterns = [
    path('register/send-otp/', RegisterSendOTPView.as_view(), name='register-send-otp'),
    path('register/verify/', VerifyOTPView.as_view(), name='register-verify'),
    path('login/send-otp/', LoginSendOTPView.as_view(), name='login-send-otp'),
    path('login/verify/', VerifyOTPView.as_view(), name='login-verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]