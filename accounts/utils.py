from abc import ABC
from rest_framework_simplejwt.tokens import RefreshToken


class Tokens(ABC):
    @classmethod
    def genarate_tokens(cls ,user):
        refresh = RefreshToken.for_user(user)
        return {"refresh" : str(refresh),
                "access":str(refresh.access_token)}