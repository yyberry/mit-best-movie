import requests 
from bs4 import BeautifulSoup
import random
import time
import pandas as pd

from web_crawler import get_agents_headers_proxies

# scrap targe movie information: name, storyline, release date, rating, tag, runtime, post    
def fetch_element_text(soup, selector, property_name=None):
    """Fetch text from a specified element or property."""
    if property_name:
        element = soup.find(selector, property=property_name)
    else:
        element = soup.find(selector)
    return element.text.strip() if element else ''

def fetch_multiple_elements_text(soup, selector, property_name=None):
    """Fetch text from multiple specified elements or properties."""
    elements = soup.find_all(selector, property=property_name)
    return ' '.join(element.text.strip() for element in elements)

def fetch_element_img(soup, selector, class_name):
    element = soup.find(selector, class_=class_name)
    image = element.find('img')['src']
    return image

def fetch_element_text_class(soup, selector, class_name=None):
    if class_name:
        element = soup.find(selector, class_=class_name)
    else:
        element = soup.find(selector)
    return element.text.strip() if element else ''

def scrap_movie_information(url):
    _, headers, proxies = get_agents_headers_proxies()

    # Anti-anti-crawling settings
    response = requests.get(url, headers=headers, proxies=proxies)
    time.sleep(random.random()*2)
    soup = BeautifulSoup(response.text, features='html.parser')
    name = fetch_element_text(soup, 'span', 'v:itemreviewed')
    year = fetch_element_text_class(soup, 'span', 'year')
    rating = fetch_element_text(soup, 'strong', 'v:average')
    if rating == '':
        rating = 0
    tags = fetch_multiple_elements_text(soup, 'span', 'v:genre')  # 根据豆瓣网页结构修改

    # print(fetch_element_text(soup, 'strong', 'v:average'))
    # Collect movie information
    movie_info = {
        'name': (name + ' ' + year),
        # 'storyline': fetch_element_text(soup, 'span', 'v:summary').replace(' ', ''),
        # 'release_date': fetch_multiple_elements_text(soup, 'span', 'v:initialReleaseDate'),
        'rate_score': rating,
        # 'rate_people_sum': fetch_element_text(soup, 'span', 'v:votes'),
        'tag': tags,
        # 'run_time': fetch_element_text(soup, 'span', 'v:runtime'),
        'img': fetch_element_img(soup, 'a', 'nbgnbg')
    }
    print(f"Scraping movie {movie_info.get('name')}")
    time.sleep(random.random()*3)
    # # Rating percentages from 1 to 5 stars
    # rate_per = {}
    # for i in range(5, 0, -1):
    #     rate_star_num = fetch_element_text(soup, 'span', f'stars{i} starstop')
    #     rate_star_num_per = fetch_element_text(soup, 'span', 'rating_per')
    #     if rate_star_num:  # Only add if the star number exists
    #         rate_per[rate_star_num] = rate_star_num_per

    # # Combine all information
    # movie_info.update(rate_per)

    # Create DataFrame
    df = pd.DataFrame.from_records([movie_info])  # Create DataFrame from single record
    # print(df)
    # df row: 'name', 'rate_score', 'tag', 'img'
    return df

# url = 'https://movie.douban.com/subject/36934908/'
# url = 'https://movie.douban.com/subject/3148694/'
# url = 'https://movie.douban.com/subject/35681325/'

# df = scrap_movie_information(url)
# print(df)
# z = df.iloc[0]['name']
# print(z)

