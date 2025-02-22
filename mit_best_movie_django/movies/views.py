from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MovieSerializer, CategorySerializer, WatchedMovieSerializer, AddWatchedMovieSerializer
from .models import Movie, Category, WatchedMovie
from db_initializer import initialize_movie

# Create your views here.


class NewMovies(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        new_category = Category.objects.filter(name='New').first()
        if not new_category:
            return Response([])
        if  request.user.is_authenticated:
            print(f"User: {request.user}")
            print(f"Watched Movie : {list(WatchedMovie.objects.filter(user=request.user))}")
            watched_movie_ids = WatchedMovie.objects.filter(user=request.user).values_list('movie__id', flat=True)
            print(f"Watched Movie IDs: {list(watched_movie_ids)}")
            new_movies = Movie.objects.filter(categories=new_category).exclude(id__in=watched_movie_ids).order_by('-rating')[:6]
        else:
            new_movies = Movie.objects.filter(categories=new_category).order_by('-rating')[:6]
        serializer = MovieSerializer(new_movies, many=True)
        return Response(serializer.data)

class TopRatedMoviesByCategoryList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # get all categories
        category_objs = Category.objects.all()
        result = []

        for category in category_objs:
            # get the top 7 movies in each category
            if  request.user.is_authenticated:
                watched_movie_ids = WatchedMovie.objects.filter(user=request.user).values_list('movie__id', flat=True)
                top_movies = Movie.objects.filter(categories=category).exclude(id__in=watched_movie_ids).order_by('-rating')[:7]
            else:
                top_movies = Movie.objects.filter(categories=category).order_by('-rating')[:7]
            serializer = MovieSerializer(top_movies, many=True)

            # return category name and movie details
            result.append({
                'category': category.slug,
                'movies': serializer.data,
            })

        return Response(result)
    
class AllMoviesByCategory(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        category = Category.objects.filter(slug=kwargs.get('category_slug')).first()
        if not category:
            return Response([])
        if  request.user.is_authenticated:
            watched_movie_ids = WatchedMovie.objects.filter(user=request.user).values_list('movie__id', flat=True)
            movies = Movie.objects.filter(categories=category).exclude(id__in=watched_movie_ids).order_by('-rating')
        else:
            movies = Movie.objects.filter(categories=category).order_by('-rating')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
class AllGenre(APIView):
    def get(self, request, *args, **kwargs):
        category_objs = Category.objects.all()[:len(Category.objects.all())-2]
        serializer = CategorySerializer(category_objs, many=True)
        return Response(serializer.data)   
    
class MovieDetail(APIView):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.filter(slug=kwargs.get('movie_slug')).first()
        if request.user.is_authenticated:
            is_watched = WatchedMovie.objects.filter(user=request.user, movie=movie).exists()
        else:
            is_watched = False
        if not movie:
            return Response([])
        serializer = MovieSerializer(movie)
        return Response({"movie":serializer.data, "is_watched": is_watched})

class WatchedMoviesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        recent = request.query_params.get("recent", "false").lower() == "true"
        if recent:
            watched_movies = WatchedMovie.objects.filter(user=request.user)[:5]
        else:
            watched_movies = WatchedMovie.objects.filter(user=request.user)
        serializer = WatchedMovieSerializer(watched_movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddWatchedMovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.validated_data['movie']
            WatchedMovie.objects.get_or_create(user=request.user, movie=movie)
            return Response({'message': 'Movie marked as watched!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RefreshDynamicCategoryView(APIView):
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('category_slug'), is_dynamic=True)
        print(f"updating category: {category}")
        
        movies = category.movies.all()

        for movie in movies:
            # check if the movie only has tags for the current category
            if movie.categories.count() == 1:
                # raise ValidationError(
                #     {"error": f"The movie '{movie.title}' only belongs to this category and cannot be untagged."}
                # )
                movie.delete()
            
            # remove the current category tag from the movie
            else:
                movie.categories.remove(category)

        # scrape new data and store it in the database.
        initialize_movie([category]) 
        
        return Response({"message": "Category refreshed successfully"}, status=status.HTTP_200_OK)
    
class RemoveWatchedMovie(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, movie_id):
        # Get the watched movie by user and movie ID
        watched_movie = get_object_or_404(WatchedMovie, user=request.user, movie_id=movie_id)

        # Delete the watched movie entry
        watched_movie.delete()

        return Response({"message": "Movie removed from watched list!"}, status=status.HTTP_200_OK)

def last_update(request):
    try:
        with open("last_update.txt", "r") as f:
            last_update_time = f.read()
        return JsonResponse({"last_update": last_update_time})
    except FileNotFoundError:
        return JsonResponse({"last_update": "Not available"})

class SearchMoviesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")  # get input key words
        if query:
            movies = Movie.objects.filter(title__icontains=query)  # search in movie titles
        else:
            movies = Movie.objects.all()  # get all movies

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)