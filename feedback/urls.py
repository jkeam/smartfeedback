from django.urls import path
app_name = 'todos'

from . import views
urlpatterns = [
    path('', views.home, name='root'),
]
