# accounts/middlewares.py

from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.sessions.models import Session
import logging

logger = logging.getLogger(__name__)

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info("SessionCheckMiddleware activated.")
        
        # Only check for authenticated users
        if request.user.is_authenticated:
            logger.info(f"Checking session for user: {request.user.username}")
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            valid_session = any(
                data.get('_auth_user_id') == str(request.user.id)
                for session in sessions
                for data in [session.get_decoded()]
            )
            if not valid_session:
                logger.warning(f"Invalid session detected for user: {request.user.username}. Logging out.")
                logout(request)  # Log the user out
                # You may choose to redirect here, but it's usually handled in the view layer
        else:
            logger.info("User is not authenticated.")

        response = self.get_response(request)
        return response
