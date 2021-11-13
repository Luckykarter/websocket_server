from rest_framework.permissions import BasePermission
from authentication.models import ApiToken
import logging
logger = logging.getLogger(__name__)

class HasToken(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        token = request.headers.get('token')
        print(f"HasToken: {token}")
        logger.info(token)

        if not token:
            return False
        try:
            ApiToken.objects.get(token=token)
        except Exception as e:
            return False
        return True
