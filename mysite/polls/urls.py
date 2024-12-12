from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', views.authenticated_index, name='index'),
    path('', views.index, name='index'),
    path('authenticated_index/', views.authenticated_index, name='authenticated_index'),
    path('create_question/', views.create_question, name='create_question'),
    path('create_question/', views.create_question, name='create_question'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),
    path('logout/', views.logout_view, name='logout'),
]