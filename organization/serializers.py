from rest_framework import serializers
from organization.models import Organization


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')
