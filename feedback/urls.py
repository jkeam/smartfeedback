from django.urls import path
app_name = 'feedback'

from . import views
urlpatterns = [
    path('', views.home, name='root'),
    path('all/', views.FeedbackListView.as_view(), name='feedback-listing'),
    path('new/', views.FeedbackCreateView.as_view(), name='feedback-new'),
    path('<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('<int:pk>/update/', views.FeedbackUpdateView.as_view(), name='feedback-update'),
    path('<int:pk>/delete/', views.FeedbackDeleteView.as_view(), name='feedback-delete'),
    path('profiles/', views.ProfileUpdateView.as_view(), name='profile-detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='profile-password'),
]
