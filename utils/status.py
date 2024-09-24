from abc import ABC
from rest_framework import status 

class Status(ABC):
    
    CREATED = status.HTTP_201_CREATED
    OK = status.HTTP_200_OK
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    FORBIDDEN  = status.HTTP_403_FORBIDDEN 