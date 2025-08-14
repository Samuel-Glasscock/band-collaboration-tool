from django.urls import path
from . import views

app_name = 'bands'

urlpatterns = [
    path("post-login/", views.post_login_router, name="post_login_router"),
    path("create/", views.create_band, name="create"), # new band form
    path("switch/<slug:slug>/", views.band_home, name="band_home"),
    path("default/<slug:slug>/", views.set_default_band, name="set_default_band"),
    path("join/<str:token>/", views.join_via_invite, name="join_via_invite"),

    path("", views.my_bands, name="switcher"), # list & choose
    path("<slug:slug>/", views.dashboard, name="dashboard"), # catch all view last
]