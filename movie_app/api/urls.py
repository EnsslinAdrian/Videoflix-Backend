from django.urls import path
from .views import MovieView, MovieDetailView, TrailerDetailView

urlpatterns = [
    # Movies
    path('', MovieView.as_view(), name='movie_list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),

    # Trailers
    path('trailer/<int:pk>/', TrailerDetailView.as_view(), name='trailer_detail'),
]