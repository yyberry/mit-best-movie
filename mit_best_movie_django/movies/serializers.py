from rest_framework import serializers
from .models import Category, Movie, WatchedMovie
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                  'name',  
                  'slug', 
                  'is_dynamic',
                  "get_absolute_url",
                  ]


class MovieSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)  

    class Meta:
        model = Movie
        fields = [
                  'id',
                  'title', 
                  'rating', 
                  'poster', 
                  'categories', 
                  'slug',
                  'get_absolute_url']
        
class WatchedMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = WatchedMovie
        fields = [
                  'user',
                  'movie', 
                  'watched_at']

class AddWatchedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedMovie
        fields = ['movie']


