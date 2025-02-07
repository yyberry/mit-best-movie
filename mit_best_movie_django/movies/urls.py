from django.urls import path, include
from movies import views

urlpatterns = [
    path('new-movies/', views.NewMovies.as_view()),
    path('top-movies/', views.TopRatedMoviesByCategoryList.as_view()),
    path('category/<slug:category_slug>/', views.AllMoviesByCategory.as_view()),
    path('categories/', views.AllGenre.as_view()),
    path('movie/<slug:movie_slug>/', views.MovieDetail.as_view()),
    path('watched-movies/', views.WatchedMoviesView.as_view()),
    path('watched-movies/<int:movie_id>/', views.RemoveWatchedMovie.as_view()),
    path('category/<slug:category_slug>/refresh/', views.RefreshDynamicCategoryView.as_view()),
    path('last-update/', views.last_update),
]
