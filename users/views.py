from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from .utils import send_verification_email
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from products.models import Product
from .utils import build_frontend_link

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """ Handles user registration and sends verification email """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_verified = False  # Ensure user starts as unverified
        user.save()
        send_verification_email(self.request, user)  # Send email on signup
        return Response({"message": "Check your email to verify your account."}, status=status.HTTP_201_CREATED)

class VerifyEmailView(generics.GenericAPIView):
    """ Handles email verification """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_verified:
            raise AuthenticationFailed("Your account is not verified. Please check your email.", code="account_not_verified")

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class GetQuotationView(APIView):
    """ Sends an email when a user requests a quotation """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        # Validate if product exists
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure user has full name & phone number
        if not user.full_name or not user.phone_number:
            return Response({"error": "User details are missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Construct email message
        subject = f"Quotation Request from {user.full_name}"
        message = (
            f"The client {user.full_name} ({user.email}) is interested in the product below.\n\n"
            f"Phone Number: {user.phone_number}\n"
            f"The Product he's interested in: {product.name}\n\n"
            "Please contact the client as soon as possible."
        )

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Email sender from .env
            [settings.ADMIN_EMAIL],  # Your email in .env
            fail_silently=False,
        )

        return Response({"message": "Quotation request sent successfully!"}, status=status.HTTP_200_OK)
    
class RequestPasswordResetView(APIView):
    """ Sends a password reset email with a unique token """

    def post(self, request):
        email = request.data.get("email")
        user = get_object_or_404(User, email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Generate reset link using utility function
        reset_link = build_frontend_link(f"reset-password/{uid}/{token}")

        subject = "Reset Your Password"
        message = f"Click the link below to reset your password:\n\n{reset_link}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """ Handles the actual password reset """
    
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            new_password = request.data.get("new_password")
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password successfully updated!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)