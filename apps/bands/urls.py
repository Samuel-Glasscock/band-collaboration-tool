from django.urls import path
from . import views

app_name = 'bands'

urlpatterns = [
    path("", views.my_bands, name="switcher"), # list & choose
    path("create/", views.create_band, name="create"), # new band form
    path("<slug:band_slug>/", views.dashboard, name="dashboard"),
]