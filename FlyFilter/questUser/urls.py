from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from questUser import views

urlpatterns = [
    url(r'^filters/weather/$', views.weatherFilters.as_view()),
    url(r'^filters/initial/$', views.initialFilter.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
