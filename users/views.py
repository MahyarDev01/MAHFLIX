import random
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterSendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        if User.objects.filter(phone_number=phone).exists():
            return Response({"error": "این شماره قبلا ثبت نام کرده است."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = random.randint(100000, 999999)
        cache.set(f"register_otp_{phone}", otp, timeout=120)
        print(f"🎯 Register OTP for {phone}: {otp}") 
        return Response({"message": "کد تایید ثبت‌نام ارسال شد."})

class RegisterVerifyAndSetPasswordView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        otp_input = request.data.get('otp')
        password = request.data.get('password')
        email = request.data.get('email', '')

        
        cached_otp = cache.get(f"register_otp_{phone}")
        if cached_otp and str(cached_otp) == str(otp_input):
            user = User(phone_number=phone)
            user.set_password(password) 
            user.email = email
            user.save()
            cache.delete(f"register_otp_{phone}")
            tokens = get_tokens_for_user(user)
            return Response({"message": "ثبت‌نام موفقیت‌آمیز بود.", "tokens": tokens})
            
        return Response({"error": "کد نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        login_id = request.data.get('login_id')   
        password = request.data.get('password')
        user = User.objects.filter(phone_number=login_id).first() or User.objects.filter(email=login_id).first()
        if user and user.check_password(password):
            tokens = get_tokens_for_user(user)
            return Response({"message": "با موفقیت وارد شدید.", "tokens": tokens})
            
        return Response({"error": "نام کاربری یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordSendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        if not User.objects.filter(phone_number=phone).exists():
            return Response({"error": "کاربری با این شماره یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        otp = random.randint(100000, 999999)
        cache.set(f"forgot_otp_{phone}", otp, timeout=120)
        print(f"🔑 Forgot Password OTP for {phone}: {otp}")
        return Response({"message": "کد بازیابی ارسال شد."})

class ResetPasswordView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        otp_input = request.data.get('otp')
        new_password = request.data.get('new_password')
        cached_otp = cache.get(f"forgot_otp_{phone}")
        
        if cached_otp and str(cached_otp) == str(otp_input):
            user = User.objects.get(phone_number=phone)
            user.set_password(new_password)
            user.save()
            cache.delete(f"forgot_otp_{phone}")
            return Response({"message": "رمز عبور با موفقیت تغییر کرد."})
            
        return Response({"error": "کد نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            "phone_number": user.phone_number,
            "email": user.email if user.email else "ثبت نشده",
            "wallet_balance": f"{int(user.wallet_balance):,} تومان",
            "is_premium": user.is_premium
        })