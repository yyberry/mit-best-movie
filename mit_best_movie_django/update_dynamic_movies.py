import random
import string

import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mit_best_movie_django.settings')
    django.setup()

from db_initializer import initialize_movie

from datetime import datetime

def update_last_run_time():
    """record last update time"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = os.path.join(settings.BASE_DIR, "last_update.txt")
    with open(file_path, "w") as f:
        f.write(timestamp)

def generate_unique_slug_when_find_duplicate_slugs(base_slug):
    from movies.models import Movie
    """
    Generates a unique slug by adding a random suffix if the base slug already exists in the database.
    """
    # Check if the base slug already exists
    if Movie.objects.filter(slug=base_slug).exists():
        # Generate a random suffix to append to the base_slug to make it unique
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        base_slug = f"{base_slug}-{random_suffix}"
    return base_slug

def check_and_update_duplicate_slugs():
    from movies.models import Movie
    """
    Checks for movies with duplicate slugs and modifies one of the duplicates to ensure uniqueness.
    """
    # Query all movies with their slugs
    movies = Movie.objects.all()
    
    # Create a dictionary to keep track of slugs and their count
    slug_count = {}
    
    for movie in movies:
        slug = movie.slug
        if slug in slug_count:
            slug_count[slug].append(movie)
        else:
            slug_count[slug] = [movie]

    # Iterate through the slug_count dictionary to find duplicates
    for slug, movie_list in slug_count.items():
        if len(movie_list) > 1:
            print(f"Found duplicate slug: {slug}")
            for i, movie in enumerate(movie_list):
                # Skip the first movie, only modify the others
                if i > 0:
                    new_slug = generate_unique_slug_when_find_duplicate_slugs(slug)
                    print(f"Updating movie '{movie.title}' slug from '{movie.slug}' to '{new_slug}'")
                    movie.slug = new_slug
                    movie.save()
            print(f"Updated duplicate slugs for: {slug}")
        
    print("All slugs are unique now!")

def fetch_dynamic_movies():
    from movies.models import Category
    """Periodically update movie data for all categories with is_dynamic=True"""
    # get all dynamic categories
    dynamic_categories = Category.objects.filter(is_dynamic=True)

    if not dynamic_categories.exists():
        print("No dynamic categories found. Exiting...")
        return

    for category in dynamic_categories:
        print(f"Updating category: {category.slug}")

        movies = category.movies.all()

        for movie in movies:
            if movie.categories.count() == 1:
                print(f"Deleting movie: {movie.title}")
                movie.delete()
            else:
                print(f"Removing category '{category.slug}' from movie: {movie.title}")
                movie.categories.remove(category)

        # update the dynamic movies data 
        initialize_movie([category])
    
    # record update time
    update_last_run_time()

    check_and_update_duplicate_slugs()

    print("All dynamic categories updated successfully!")

if __name__ == "__main__":
    fetch_dynamic_movies()