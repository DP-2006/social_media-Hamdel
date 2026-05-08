# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import OTP

User = get_user_model()


class PhoneSerializer(serializers.Serializer):
    """Serializer for phone number validation"""
    phone = serializers.CharField(
        max_length=15,
        required=True,
        help_text="User's phone number (e.g., 09123456789)"
    )
    
    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits")
        # Normalize phone number
        cleaned = ''.join(filter(str.isdigit, str(value)))
        if cleaned.startswith('0'):
            cleaned = cleaned[1:]
        if not cleaned.startswith('98') and len(cleaned) == 10:
            cleaned = '98' + cleaned
        return cleaned


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer for OTP verification"""
    phone = serializers.CharField(
        max_length=15,
        required=True,
        help_text="User's phone number"
    )
    code = serializers.CharField(
        max_length=6,
        min_length=4,
        required=True,
        help_text="OTP code received via SMS"
    )
    
    def validate(self, data):
        if not data.get('phone'):
            raise serializers.ValidationError({"phone": "Phone number is required"})
        if not data.get('code'):
            raise serializers.ValidationError({"code": "OTP code is required"})
        return data


class LogoutSerializer(serializers.Serializer):
    """Serializer for logout"""
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Refresh token to blacklist"
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = [
            'id', 'phone', 'username', 'email', 
            'date_joined', 'last_login', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserRegisterResponseSerializer(serializers.Serializer):
    """Serializer for user registration response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user_id = serializers.CharField()
    is_new = serializers.BooleanField()


class OTPSendResponseSerializer(serializers.Serializer):
    """Serializer for OTP send response"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    code_for_test = serializers.CharField(required=False, allow_null=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate_old_password(self, value):
        request = self.context.get('request')
        if request and request.user:
            if not request.user.check_password(value):
                raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        validate_password(data['new_password'])
        return data


class OTPSerializer(serializers.ModelSerializer):
    """Serializer for OTP model"""
    class Meta:
        model = OTP
        fields = ['id', 'phone', 'code', 'expires_at', 'is_used', 'created_at']
        read_only_fields = ['id', 'created_at']