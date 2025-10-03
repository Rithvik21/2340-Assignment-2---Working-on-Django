from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies_index'),
    path('<int:id>/', views.show, name='movies_show'),
    path('<int:id>/reviews/create/', views.create_review, name='movies_create_review'),
    path('<int:id>/reviews/<int:review_id>/edit/', views.edit_review, name='movies_edit_review'),
    path('<int:id>/reviews/<int:review_id>/delete/', views.delete_review, name='movies_delete_review'),
    
    # Petition URLs
    path('petitions/', views.petition_list, name='petition_list'),
    path('petitions/create/', views.petition_create, name='petition_create'),
    path('petitions/<int:id>/', views.petition_detail, name='petition_detail'),
    path('petitions/<int:id>/vote/', views.petition_vote, name='petition_vote'),
    path('petitions/<int:id>/vote-ajax/', views.petition_vote_ajax, name='petition_vote_ajax'),
]
