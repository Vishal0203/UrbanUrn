from Urn.models import Users


class UrbanUrnAuthentication(object):

    def authenticate(self, username=None, password=None):
        user = Users.objects.get(email=username)
        pass
