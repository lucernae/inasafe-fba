from django.conf.urls import url
from fba.api_views.recent_hazard import RecentHazardList


urlpatterns = [
    url(r'^recent-hazard-events/$',
        RecentHazardList.as_view(),
        name='recent-hazard-list-api')
]
