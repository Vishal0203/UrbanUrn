import json

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import validate_schema
from Urn.models import Users, Status
from Urn.schema_validators.registration_validator import schema


@csrf_exempt
@validate_schema(schema)
def register(request):
    if request.method in ['POST']:
        body = json.loads(request.body.decode())
        try:
            User.objects.get(email=body['email'])
            request.session["Error"] = "Email already exists"
            return HttpResponse("Email already exists")
        except User.DoesNotExist:
            user = User.objects.create_user(body['username'], body['email'], body['password'],
                                            first_name=body['first_name'],
                                            last_name=body['last_name'])
            Users.objects.create(
                user_id=user.id,
                phone=body['phone'],
                status=Status.active.value
            )
            return HttpResponse("User is Created")
    else:
        return HttpResponseNotFound("Page Not Found")
