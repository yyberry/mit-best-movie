import os
import django
from django.conf import settings

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mit_best_movie_django.settings')
    django.setup()

from db_initializer import initialize_movie

from datetime import datetime

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

    print("All dynamic categories updated successfully!")

def update_last_run_time():
    """record last update time"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = os.path.join(settings.BASE_DIR, "last_update.txt")
    with open(file_path, "w") as f:
        f.write(timestamp)

if __name__ == "__main__":
    fetch_dynamic_movies()