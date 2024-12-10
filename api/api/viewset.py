from api.models import Persons
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from api.api.serializers import PersonsSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly


class PersonsViewSet(ModelViewSet):
    serializer_class = PersonsSerializer
    queryset = Persons.objects.all()