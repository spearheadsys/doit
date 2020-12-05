from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Card, Board
from .serializers import CardSerializer
from board.serializers import BoardSerializer
from django.db.models import Q
from django.utils import timezone
from card.models import Columntype
from django.core.cache import cache


# todo: enable more caching as per slabreached
today_date = timezone.now()

class CardViewSet(viewsets.ModelViewSet):
    # Todo: restrict to user object (i.e. admin sees all, operator sees all, customers see only their own)
    queryset = Card.objects.filter(closed=False)
    serializer_class = CardSerializer


class MyCardViewSet(viewsets.ModelViewSet):
    # queryset = Card.objects.all().filter(closed=False)
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(owner=self.request.user).filter(~Q(column__title="Backlog"))
        return queryset


class AllOpenIncidentsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    # TODO: limit this to incidents this user CAN view (i.e. is watcher, is operator,
    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(type="IN")
        return queryset


class MyOpenIncidentsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(type="IN").filter(owner=self.request.user)
        return queryset


class MyMajorCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(priority__title="Major").filter(owner=self.request.user)
        return queryset


class MyNormalCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(priority__title="Normal").filter(owner=self.request.user)
        return queryset


class MyMinorCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(priority__title="Minor").filter(owner=self.request.user)
        return queryset


class MyOverdueCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False, owner=self.request.user).filter(~Q(column__title="Backlog")).order_by('due_date').filter(due_date__lt=today_date)
        return queryset

class AllOverdueCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False).filter(~Q(column__title="Backlog")).order_by('due_date').filter(due_date__lt=today_date)
        return queryset


class MyOverdueBoardsViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.filter(archived=False, owner=self.request.user).filter(due_date__lt=today_date)

        return queryset


class AllOverdueBoardsViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.filter(archived=False).filter(due_date__lt=today_date)

        return queryset


class AllSlaBreached(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # TODO: looool
        if cache.get('all-open-cards'):
            cards = cache.get('all-open-cards')
        else:
            cards = Card.objects.all().filter(closed=False)

        if cache.get('default'):
            return cache.get('default')
        else:
            queryset = [x for x in cards if x.sla_breached()]
            cache.set('default', queryset, 900)
            return queryset


class NoOwnerOrCompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False).filter(
            Q(owner=None) | Q(company=None)
        ).distinct()

        return queryset


class CardsWatcherViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.filter(closed=False).filter(~Q(column__title="Backlog")).filter(Q(watchers__in=[self.request.user])).distinct()
        return queryset


class MyBacklogCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        backlog = Columntype.objects.all().filter(name="Backlog")
        queryset = Card.objects.filter(closed=False, owner=self.request.user).filter(Q(column__usage__exact=backlog[0].id))
        return queryset


class AllBacklogCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        backlog = Columntype.objects.all().filter(name="Backlog")
        # queryset = Card.objects.filter(closed=False).filter(Q(column__usage__exact=backlog[0].id))
        # return queryset

        if not cache.get('all-backlog-cards'):
            queryset = Card.objects.filter(closed=False).filter(Q(column__usage__exact=backlog[0].id))
            cache.set('all-backlog-cards', queryset, 900)
            return queryset
        else:
            return cache.get('all-backlog-cards')


class CardsWithoutDueDateViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(~Q(column__title="Backlog")).filter(due_date=None)
        return queryset


class OverdueTodayViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        if self.request.user.profile_user.is_operator or self.request.user.profile_user.is_superuser:
            queryset = Card.objects.filter(closed=False).filter(~Q(column__title="Backlog")).filter(due_date__year=today_date.year, due_date__month=today_date.month, due_date__day=today_date.day)
            return queryset



# TODO:create components for waiting/working/documentation/etc.
#  (some card asisignemtn stats), show on dashboard
class MyWaitingCardsViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = Card.objects.all().filter(closed=False).filter(column__usage__name="Waiting").filter(owner=self.request.user)
        return queryset