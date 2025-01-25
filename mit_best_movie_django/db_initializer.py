import pandas as pd


'''
crawl_movie_types: 爬取类别信息(return name(类别名), link, is_dynamic, slug)
crawl_new_movies: 爬取新电影信息(return name(电影名), link(电影详细信息页link))
crawl_top_movies: 爬取新电影信息(return name(电影名), link(电影详细信息页link))
crawl_top250_movies: 爬取top250电影信息(return name(电影名), link(电影详细信息页link)) 
crawl_type_movies: 爬取各类别电影信息(return name(电影名), link(电影详细信息页link)) 
scrap_movie_information: 爬取电影的详细信息(return name(电影名), rate_score, img)
'''
from web_crawler import crawl_movie_types
from web_crawler import crawl_new_movies, crawl_top_movies, crawl_top250_movies, crawl_type_movies
from web_scraper import scrap_movie_information
import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mit_best_movie_django.settings')
    django.setup()

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
                        'slug': f"{category.slug.lower().replace(' ', '-')}-{idx + 1}",  # 使用类别名和递增数字生成slug
                        'rating': movie_details_df.iloc[0]['rate_score'],
                        'poster': movie_details_df.iloc[0]['img'],
                    }
                )

                tags = movie_details_df.iloc[0]['tag'].split()  # 按空格拆分成标签列表

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
                        'slug': f"{category.slug.lower().replace(' ', '-')}-{idx + 1}",  # 使用类别名和递增数字生成slug
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
                        'slug': f"{category.slug.lower().replace(' ', '-')}-{idx + 1}",  # 使用类别名和递增数字生成slug
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


