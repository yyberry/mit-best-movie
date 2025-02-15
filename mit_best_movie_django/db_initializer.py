import pandas as pd
import random
import string

'''
crawl_movie_types: crawl category info(return name(category name), link, is_dynamic, slug)
crawl_new_movies: crawl new movies info(return name(movie name), link(movie details page link))
crawl_top_movies: crawl new movies info(return name(movie name), link(movie details page link))
crawl_top250_movies: crawl top250 movies info(return name(movie name), link(movie details page link)) 
crawl_type_movies: crawl movie information for each category(return name(movie name), link(movie details page link)) 
scrap_movie_information: scrap movie details(return name(movie name), rate_score, img)
'''
from web_crawler import crawl_movie_types
from web_crawler import crawl_new_movies, crawl_top_movies, crawl_top250_movies, crawl_type_movies
from web_scraper import scrap_movie_information
import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mit_best_movie_django.settings')
    django.setup()

def generate_unique_slug(category_slug, movie_idx):
    from movies.models import Category, Movie
    """
    Generates a unique slug using category slug, movie index, and a random suffix.
    """
    base_slug = f"{category_slug.lower().replace(' ', '-')}-{movie_idx + 1}"
    # Check if the slug already exists
    if Movie.objects.filter(slug=base_slug).exists():
        # Append a random string to ensure uniqueness
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        base_slug = f"{base_slug}-{random_suffix}"
    return base_slug

def initialize_category(url):
    from movies.models import Category, Movie
    category_df = crawl_movie_types(url)
    category_objs = []
    for _, row in category_df.iterrows():
        category, created = Category.objects.get_or_create(
            name = row['name'],
            defaults = {
                'url': row['link'],
                'is_dynamic': row['is_dynamic'],
                'slug': row['slug'],
            },
        )
        category_objs.append(category)
        if not created:
            # Update existing category if needed
            category.url = row['link']
            category.is_dynamic = row['is_dynamic']
            category.slug = row['slug']
            category.save()
    return category_objs

def initialize_movie(category_objs):
    print(category_objs)
    from movies.models import Category, Movie
    for category in category_objs:

        # only when scraping New movies it goes into movie detail webpage

        if category.name == 'New':
            print(f"Category name: {category.name}")
            new_movie_df = crawl_new_movies(category.url)
            top_movie_df = crawl_top_movies(category.url)
            movie_df = pd.concat([new_movie_df, top_movie_df], ignore_index=True).drop_duplicates(subset=['link'])

            for idx, row in movie_df.iterrows():
                movie_details_df = scrap_movie_information(row['link'])
                if movie_details_df.empty:
                    print(f"Warning: No details found for movie at {row['link']}")
                    continue
                
                movie, created = Movie.objects.get_or_create(
                    url=row['link'],
                    defaults={
                        'title': movie_details_df.iloc[0]['name'],
                        'slug': generate_unique_slug(category.slug, idx),  # generate a slug using the category name and an incremental number
                        'rating': movie_details_df.iloc[0]['rate_score'],
                        'poster': movie_details_df.iloc[0]['img'],
                    }
                )

                tags = movie_details_df.iloc[0]['tag'].split() 

                for c_name in tags:
                    print(f'c_name: {c_name}')
                    try:
                        c_obj = Category.objects.get(name=c_name)
                    except Category.DoesNotExist:
                        continue
                    movie.categories.add(c_obj)

                movie.categories.add(category)

                if not created:
                    # Update existing category if needed
                    movie.rating = movie_details_df.iloc[0]['rate_score']
                    category.save()
                
                print(f"Movie: {movie.title} - Category: {category.slug}")

            print(f"All movies in {category.slug} saved succesfully! ")

        elif category.name == 'Top250':
            print(f"Category name: {category.name}")
            movie_df = crawl_top250_movies(category.url)

            for idx, row in movie_df.iterrows():
                if movie_df.empty:
                    print(f"Warning: No details found for movie at {row['link']}")
                    continue

                movie, created = Movie.objects.get_or_create(
                    url=row['link'],
                    defaults={
                        'title': row['name'],
                        'slug': generate_unique_slug(category.slug, idx),  # generate a slug using the category name and an incremental number
                        'rating': row['rate_score'],
                        'poster': row['img'],
                    }
                )
                movie.categories.add(category)

                if not created:
                    # Update existing category if needed
                    movie.rating = row['rate_score']
                    category.save()

                print(f"Movie: {movie.title} - Category: {category.slug}")

            print(f"All movies in {category.slug} saved succesfully! ")
        else: # Genre 
            print(f"Category name: {category.name}")
            movie_df = crawl_type_movies(category.url)

            for idx, row in movie_df.iterrows():
                print("index:", idx)
                if movie_df.empty:
                    print(f"Warning: No details found for movie at {row['link']}")
                    continue

                movie, created = Movie.objects.get_or_create(
                    url=row['link'],
                    defaults={
                        'title': row['name'],
                        'slug': f"{category.slug.lower().replace(' ', '-')}-{idx + 1}",  # generate a slug using the category name and an incremental number
                        'rating': row['rate_score'],
                        'poster': row['img'],
                    }
                )
                movie.categories.add(category)

                if not created:
                    # Update existing category if needed
                    movie.rating = row['rate_score']
                    category.save()

                print(f"Movie: {movie.title} - Category: {category.slug}")

            print(f"All movies in {category.slug} saved succesfully! ")

if __name__ == "__main__":
    setup_django()
    url = 'https://movie.douban.com/chart'
    category_objects = initialize_category(url)
    print(category_objects)
    # print(len(category_objects))
    # initialize_movie(category_objects[3:])
    print("Done!")


