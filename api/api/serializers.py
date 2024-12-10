from api.models import Persons
from rest_framework import serializers

class PersonsSerializer(serializers.ModelSerializer):
    #link = serializers.HyperlinkedIdentityField(view_name='api:persons_api_view_detail', lookup_field='pk')
    class Meta:
        model = Persons
        fields = "__all__"