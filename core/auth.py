from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.authentication import get_authorization_header


# write custom auth class that if view requires authentication, it will check if token is valid, if view does not
# require authentication, it should not give any errors

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the view that is being accessed
        view = request.resolver_match.func.cls

        # Check if the view has IsAuthenticated permission
        if IsAuthenticated in getattr(view, 'permission_classes', []):
            return super().authenticate(request)

        # If the view does not require authentication, return None
        return None
