from django.urls import path 
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'base'

urlpatterns = [

    # HomePage View
    path(r'', login_required(views.HomePageView.as_view()), name='home'),

    # Search
    path(r'search/', login_required(views.SearchView.as_view()), name='search'),
]


