from rest_framework import serializers
from .models import Card
from board.serializers import BoardSerializer
from contact.serializers import AccountSerializer
from organization.serializers import CompanySerializer


class CardSerializer(serializers.ModelSerializer):
    board = BoardSerializer()
    owner = AccountSerializer()
    company = CompanySerializer()

    class Meta:
        model = Card
        fields = '__all__'
