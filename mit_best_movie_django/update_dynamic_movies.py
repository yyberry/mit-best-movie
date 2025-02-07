import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mit_best_movie_django.settings')
django.setup()

from movies.models import Category
from db_initializer import initialize_movie
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

def fetch_dynamic_movies():
    """定期更新所有 is_dynamic=True 的类别的电影数据"""
    # 获取所有动态类别
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

        # 调用你的爬虫来爬取新的电影数据
        initialize_movie([category])
    
    # 记录更新时间
    update_last_run_time()

    print("All dynamic categories updated successfully!")

def update_last_run_time():
    """记录上次更新的时间"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_path = os.path.join(settings.BASE_DIR, "last_update.txt")
    with open(file_path, "w") as f:
        f.write(timestamp)

if __name__ == "__main__":
    fetch_dynamic_movies()