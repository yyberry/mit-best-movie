from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

from rest_framework.exceptions import ValidationError

from .serializers import MovieSerializer, CategorySerializer, WatchedMovieSerializer, AddWatchedMovieSerializer
from .models import Movie, Category, WatchedMovie
from db_initializer import initialize_movie

# Create your views here.


class NewMovies(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # 获取 New 类别的最新电影
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
    authentication_classes = [authentication.TokenAuthentication]
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
    authentication_classes = [authentication.TokenAuthentication]
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
        if not movie:
            return Response([])
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

class WatchedMoviesView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        watched_movies = WatchedMovie.objects.filter(user=request.user)[:5]
        serializer = WatchedMovieSerializer(watched_movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddWatchedMovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = serializer.validated_data['movie']
            WatchedMovie.objects.get_or_create(user=request.user, movie=movie)
            return Response({'message': 'Movie marked as watched!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RefreshDynamicCategoryView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取对应类别
        category = get_object_or_404(Category, slug=kwargs.get('category_slug'), is_dynamic=True)
        print(f"updating category: {category}")
        
        # 获取该类别下的所有电影
        movies = category.movies.all()

        for movie in movies:
            # 检查该电影是否仅有当前类别的标签
            if movie.categories.count() == 1:
                # raise ValidationError(
                #     {"error": f"The movie '{movie.title}' only belongs to this category and cannot be untagged."}
                # )
                movie.delete()
            
            # 移除该电影的当前类别标签
            else:
                movie.categories.remove(category)

        # 爬取新数据并存储到数据库中
        initialize_movie([category]) 
        
        return Response({"message": "Category refreshed successfully"}, status=status.HTTP_200_OK)
    