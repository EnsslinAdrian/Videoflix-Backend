from django.urls import path
from .views import RegisterView, VerifyEmailView, PasswordResetRequestView, \
PasswordResetConfirmView, CustomLoginView, RefreshAccessTokenView, \
MeUserView, AuthStatusView, LogoutView


urlpatterns = [
    # User registration and email verification
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    # Authentication
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('status/', AuthStatusView.as_view(), name='auth_status'),
    path('refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'),

    # Password reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Logout and user info
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeUserView.as_view(), name='me_user'),
]
