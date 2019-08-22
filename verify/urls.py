from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^code.png/$',views.verify_code)
]