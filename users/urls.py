from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, VerifyEmailView, CustomTokenObtainPairView, GetQuotationView, RequestPasswordResetView, ResetPasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # ✅ Use custom login view
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("get-quotation/", GetQuotationView.as_view(), name="get-quotation"),
    path("request-password-reset/", RequestPasswordResetView.as_view(), name="request-password-reset"),
    path("reset-password/<uidb64>/<token>/", ResetPasswordView.as_view(), name="reset-password"),
]
