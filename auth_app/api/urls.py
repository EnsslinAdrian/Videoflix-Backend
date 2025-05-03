from django.urls import path
from .views import RegisterView, VerifyEmailView, PasswordResetRequestView, \
PasswordResetConfirmView, CustomLoginView, RefreshAccessTokenView, \
MeUserView, AuthStatusView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),

    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('status/', AuthStatusView.as_view(), name='auth_status'),
    path('refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'),

    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('me/', MeUserView.as_view(), name='me_user'),
]
