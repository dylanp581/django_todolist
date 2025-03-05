from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("view/", views.view, name="view"),
    path("profile/", views.profile, name="profile"),
    path('schedule/create/', views.create_schedule_item, name='create_schedule'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/delete/<int:item_id>/', views.delete_schedule_item, name='delete_schedule_item'),
    path('schedule/toggle/<int:item_id>/', views.toggle_schedule_item, name='toggle_schedule_item'),
]