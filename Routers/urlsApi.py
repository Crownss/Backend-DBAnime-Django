from Controllers.views import *
from rest_framework import routers
from ViewSets.views_set import *

app_name='api'

router = routers.DefaultRouter()
# router.register('list-users', UsersViewSet, basename='list-users')


urlpatterns = router.urls