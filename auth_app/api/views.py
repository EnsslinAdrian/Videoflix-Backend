from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate
from django.utils import timezone

from datetime import timedelta, timezone as dt_timezone

from .serializers import RegisterSerializer
from auth_app.models import CustomUser

signer = TimestampSigner()
User = get_user_model()

class RegisterView(APIView):
    """
    Handles user registration:
    - Validates input
    - Creates a new user
    - Sends a verification email
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = signer.sign(user.email)
            verify_url = f"{settings.FRONTEND_VERIFY_URL}?token={token}"

            html_content = render_to_string('verify_email.html', {
                'verify_url': verify_url
            })

            email = EmailMultiAlternatives(
                subject="Please confirm your email address",
                body=f"Please confirm your email here: {verify_url}",  
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Please check your email to activate your account."}, status=201)
        return Response(serializer.errors, status=400)

class VerifyEmailView(APIView):
    """
    Handles email verification for user accounts.

    Methods:
        get(request):
            Verifies the email using a token from query parameters.
            Activates the user account if the token is valid.
    """
    def get(self, request):
        token = request.query_params.get("token")
        try:
            email = signer.unsign(token, max_age=60*60*24)
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({"message": "Email confirmed. You can now log in."})
        except (BadSignature, SignatureExpired):
            return Response({"message": "The confirmation link is invalid or has expired."}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"message": "No user found with this email."}, status=404)
        except Exception as e:
            return Response({"message": f"Internal server error: {str(e)}"}, status=500)

class PasswordResetConfirmView(APIView):
    """
    Handles password reset confirmation requests.
    Methods:
        post(request):
            Validates the provided UID and token, and updates the user's password if valid.
    """
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"message": "The link is invalid or has expired."}, status=400)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Your password has been successfully changed."})
        except Exception:
            return Response({"message": "Error resetting the password."}, status=400)

class PasswordResetRequestView(APIView):
    """
    Handles password reset requests by sending a reset email to the user.
    Methods:
        post(request):
            Processes the password reset request, generates a reset token,
            and sends an email with the reset link to the provided email address.
    """
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{settings.FRONTEND_RESET_URL}?uid={uid}&token={token}"

            html = render_to_string('password_reset_email.html', {
                'reset_url': reset_url
            })

            email_obj = EmailMultiAlternatives(
                subject="Reset your Password",
                body=f"Reset your Password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email_obj.attach_alternative(html, "text/html")
            email_obj.send()

            return Response({"message": "Password reset email has been sent."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"message": "No account is associated with this email address."}, status=400)

class CustomLoginView(TokenObtainPairView):
    """
    Custom login view for handling user authentication and token generation.
    Methods:
        post(request, *args, **kwargs):
            Handles POST requests for user login, validates credentials, 
            generates access and refresh tokens, and sets the refresh token 
            as an HTTP-only cookie.
    """
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "Your account is not active. Please verify your email address."}, status=403)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken.for_user(user)
        refresh["auth_method"] = "password"
        refresh["re_auth_until"] = (timezone.now() + timedelta(minutes=1)).timestamp()  

        access = refresh.access_token
        access["auth_method"] = "password"
        access["re_auth_until"] = refresh["re_auth_until"]

        response = Response({
            "access": str(access),
            "message": "Login successful."
        }, status=200)

        response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="None",  
                # max_age=7 * 24 * 60 * 60,
            )

        return response

class RefreshAccessTokenView(APIView):  
    """
    Handles the generation of a new access token using a refresh token.
    Methods:
        post(request):
            Validates the refresh token from cookies and generates a new access token.
            Returns an error response if the refresh token is invalid or expired.
    """
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "No refresh token found."}, status=401)

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            auth_method = refresh.get("auth_method")

            if auth_method:
                access["auth_method"] = auth_method

            re_auth_until = refresh.get("re_auth_until")
            if re_auth_until:
                access["re_auth_until"] = re_auth_until

            return Response({'access': str(access)})

        except Exception:
            return Response({'detail': 'Invalid or expired refresh token.'}, status=401)

class LogoutView(APIView):
    """
    Handles user logout by deleting the refresh token cookie.

    Methods:
        post(request):
            Deletes the 'refresh_token' cookie and returns a success message.
    """
    def post(self, request):
        response = Response({"message": "Successfully logged out"})
        response.delete_cookie("refresh_token", path="/", samesite="None")
        return response

class AuthStatusView(APIView):
    """
    View to check the authentication status of a user.
    Methods:
        get(request):
            Handles GET requests to verify if the user is authenticated
            based on the presence and validity of a refresh token in cookies.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"authenticated": False}, status=200)

        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh.payload.get("user_id")
            return Response({
                "authenticated": True,
                "user_id": user_id
            }, status=200)
        except Exception:
            return Response({"authenticated": False}, status=200)
        
class MeUserView(APIView):
    """
    API view to handle operations related to the authenticated user.
    Methods:
        get(request):
            Retrieve the authenticated user's details including id, email, first name, and last name.
        put(request):
            Update the authenticated user's first name and/or last name if provided in the request data.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
        return Response(data)

    def put(self, request):
        fields = ["first_name", "last_name"]
        for field in fields:
            if field in request.data:
                setattr(request.user, field, request.data[field])
        request.user.save()
        return Response({"message": "User updated successfully."})

