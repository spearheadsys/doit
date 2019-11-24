from rest_framework import viewsets
from .models import Card, Board
from .serializers import CardSerializer
from board.serializers import BoardSerializer
from organization.serializers import CompanySerializer
from django.db.models import Q
from django.utils import timezone
from card.models import Columntype

today_date = timezone.now()


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all().filter(closed=False)
    serializer_class = CardSerializer


class MyCardViewSet(viewsets.ModelViewSet):
    # queryset = Card.objects.all().filter(closed=False)
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(owner=self.request.user).filter(~Q(column__title="Backlog"))

        # another_param = self.request.GET.get('another_param')
        # if another_param:
        #     queryset = queryset.filter(another_field=another_param)

        return queryset


class AllOpenIncidentsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    # TODO: limit this to incidents this user CAN view (i.e. is watcher, is operator,
    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(type="IN")
        return queryset


class MyOpenIncidentsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(type="IN").filter(owner=self.request.user)
        return queryset


class MyOverdueCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False, owner=self.request.user).filter(~Q(column__title="Backlog")).order_by('due_date').filter(due_date__lt=today_date)
        return queryset


class MyOverdueBoardsViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.filter(archived=False, owner=self.request.user).filter(due_date__lt=today_date)

        return queryset


class NoOwnerOrCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False).filter(
            Q(owner=None) | Q(company=None)
        ).distinct()

        return queryset


class CardsWatcherViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False).filter(Q(watchers__in=[self.request.user])).distinct()
        return queryset


class MyBacklogCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        backlog = Columntype.objects.all().filter(name="Backlog")
        queryset = Card.objects.filter(closed=False, owner=self.request.user).filter(Q(column__usage__exact=backlog))
        return queryset


class AllBacklogCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        backlog = Columntype.objects.all().filter(name="Backlog")
        queryset = Card.objects.filter(closed=False).filter(Q(column__usage__exact=backlog))
        return queryset