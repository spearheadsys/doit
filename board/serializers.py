from rest_framework import serializers
from .models import Board
from organization.serializers import CompanySerializer


class BoardSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()

    class Meta:
        model = Board
        fields = ('id', 'name', 'company')
