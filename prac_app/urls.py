from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('process_register', views.process_register, name='process_register'),
    path('process_login', views.process_login, name='process_login'),
    path('wishes', views.wishes, name='wishes'),
    path('wishes/new', views.wishes_new, name='wishes_new'),
    path('wishes/remove/<int:wish_id>', views.wishes_remove, name='wishes_remove'),
    path('wishes/edit/<int:wish_id>', views.wishes_edit, name='wishes_edit'),
    path('process_wishes_edit', views.process_wishes_edit, name='process_wishes_edit'),
    path('wishes/granted/<int:wish_id>', views.wishes_granted, name='wishes_granted'),
    path('wishes/like/<int:wish_id>', views.wishes_like, name='wishes_like'),
    path('wishes/stats', views.wishes_stats, name='wishes_stats'),


    path('process_new_wish', views.process_new_wish, name='process_new_wish'),
    path('logout', views.logout, name='logout'),
]