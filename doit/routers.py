from rest_framework import routers
from card.viewsets import CardViewSet, MyCardViewSet, AllOpenIncidentsViewSet, MyOpenIncidentsViewSet, \
    MyOverdueCardsViewSet, MyOverdueBoardsViewSet, NoOwnerOrCompanyViewSet, CardsWatcherViewSet, \
    MyBacklogCardsViewSet, AllBacklogCardsViewSet

router = routers.SimpleRouter()
router.register(r'cards', CardViewSet)
router.register(r'mycards', MyCardViewSet, basename="mycards")
router.register(r'allopenincidents', AllOpenIncidentsViewSet, basename="allopenincidents")
router.register(r'myopenincidents', MyOpenIncidentsViewSet, basename="myopenincidents")
router.register(r'myoverduecards', MyOverdueCardsViewSet, basename="myoverduecards")
router.register(r'myoverdueboards', MyOverdueBoardsViewSet, basename="myoverdueboards")
router.register(r'noownerorcompany', NoOwnerOrCompanyViewSet, basename="noownerorcompany")
router.register(r'cardswatcher', CardsWatcherViewSet, basename="cardswatcher")
router.register(r'mybacklog', MyBacklogCardsViewSet, basename="mybacklog")
router.register(r'allbacklog', AllBacklogCardsViewSet, basename="allbacklog")
