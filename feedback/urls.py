from django.urls import path
app_name = 'feedback'

from . import views
urlpatterns = [
    path('', views.home, name='root'),
]
