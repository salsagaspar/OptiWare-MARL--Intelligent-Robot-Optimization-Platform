from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('robots/', views.robot_list, name='robot_list'),
    path('simulation/', views.rl_simulation, name='simulation'),
    path('copilot/', views.copilot_chat, name='copilot'),
    path('api/copilot/', views.api_copilot_response, name='api_copilot'),
]
