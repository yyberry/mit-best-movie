from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

class Category(models.Model):
    # Represents a category or tag for movies, such as "Action", "New", etc.
    name = models.CharField(max_length=255, unique=True) # category name
    url = models.URLField(unique=True) # category url
    is_dynamic = models.BooleanField(default=False)  # tag “New” is dynamic 
    slug = models.SlugField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
class Movie(models.Model):
    # Represents detailed information about a movie
    title = models.CharField(max_length=255) # movie title
    url = models.URLField(unique=True)  # movie detail page url
    rating = models.FloatField(null=True, blank=True)   # movie score
    poster = models.URLField(null=True, blank=True) # movie poster url
    categories = models.ManyToManyField(Category, related_name='movies') 
    slug = models.SlugField()

    class Meta:
        ordering = ('-rating', )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/{self.slug}'
    
class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Prevent a user from marking the same movie multiple times
        ordering = ['-watched_at']  # Latest watched movies appear first

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title} at {self.watched_at}"

# class Ranking(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     url = models.URLField(unique=True)
#     slug = models.SlugField()

#     def __str__(self):
#         return self.name
    
#     def get_absolute_url(self):
#         return f'/{self.slug}/'
    

# class MovieRanking(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)   
#     ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE) 
    
#     def __str__(self):
#         return f"{self.movie.title} in {self.ranking.name}"

# class Movie(models.Model):
#     # Represents a movie's basic information
#     title = models.CharField(max_length=255)
#     url = models.URLField(unique=True)
#     categories = models.ManyToManyField(Category, related_name='movies')

#     def __str__(self):
#         return self.title
