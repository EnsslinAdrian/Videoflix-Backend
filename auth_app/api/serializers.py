from rest_framework import serializers
from auth_app.models import CustomUser
from django.contrib.auth.password_validation import validate_password

class MeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, providing all fields for serialization.
    Marks 'user' and 'created_at' fields as read-only.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Fields:
        email (str): User's email address.
        password (str): User's password (write-only, validated).
        first_name (str, optional): User's first name.
        last_name (str, optional): User's last name.
    Methods:
        create(validated_data):
            Creates a new user with the provided data, sets the user as inactive, and saves it.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.is_active = False
        user.save()
        return user
