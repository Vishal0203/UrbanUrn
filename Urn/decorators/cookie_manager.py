from django.http import HttpResponse
from UrbanUrn import settings


def manage_cookie(original_function):
    def check_or_set_cookie(request_arg):
        if request_arg.COOKIES.get(settings.ANONYMOUS_SESSION_NAME, None) is None:
            session_id = request_arg.session._get_or_create_session_key()
            response = original_function(request_arg)
            response.set_cookie(settings.ANONYMOUS_SESSION_NAME, session_id)
        else:
            response = original_function(request_arg)

        return response

    return check_or_set_cookie
