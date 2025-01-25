import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import sqlite3

import traceback
import os

def get_soup(url, headers, proxies):
    """Fetch the content of the URL and return a BeautifulSoup object."""
    response = requests.get(url, headers=headers, proxies=proxies)
    return BeautifulSoup(response.text, features='html.parser')

# set Chrome options
def set_chrome_options(user_agents, proxies, setting=True):
    if setting:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        chrome_options.add_argument(f'--proxy-server={proxies}')
        return webdriver.Chrome(options = chrome_options)
    else:
        return webdriver.Chrome()

def extract_movies(movies, setting = 'soup'):
    """Extract movie names and links from a list of movie elements."""
    print("starting extracting data...")
    if setting == 'soup':
        movie_list = [
            {
                'name': movie.find('a').text.strip().replace('\n', '').replace(' ', ''),
                'link': movie.find('a')['href']
            }
            for movie in movies if movie.find('a')
        ]
        df = pd.DataFrame(movie_list)
        return df
    elif setting == 'selenium':
        movie_list = []
        seen_links = set()
        i = 1
        for movie in movies:
            # check if the movie element is visible
            if movie.is_displayed():
                try:
                    # //*[@id="content"]/div/div[1]/div[6]/div[1]/div/div/div[1]/span[1]/a
                    # //*[@id="content"]/div/div[1]/div[6]/div[2]/div/div/div[1]/span[1]/a
                    # //*[@id="content"]/div/div[1]/div[6]/div[40]/div/div/div[1]/span[1]/a
                    # print(movie.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div[6]/div[{i}]/div/div/div[1]/span[1]/a').text, 
                    #       movie.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div[6]/div[{i}]/div/div/div[1]/span[1]/a').get_attribute('href'))
                    name = movie.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div[6]/div[{i}]/div/div/div[1]/span[1]/a').text.replace('\n', '').replace(' ', '').strip()
                    link = movie.find_element(By.XPATH, f'//*[@id="content"]/div/div[1]/div[6]/div[{i}]/div/div/div[1]/span[1]/a').get_attribute('href')
                    
                    year = movie.find_element(By.CLASS_NAME, 'movie-misc').text.split(" / ")[0]
                    
                    score = movie.find_element(By.CLASS_NAME, 'rating_num').text
                    
                    img_element = movie.find_element(By.CLASS_NAME, 'movie-img')
                    img = img_element.get_attribute('src') or img_element.get_attribute('data-original')
                    # print(f"Movie {i} image source: {img}")
                    # Only append if we haven't seen this link before
                    if name and link and (link not in seen_links):
                        seen_links.add(link)
                        movie_list.append({'name': name+' '+year, 'link': link, 'rate_score':score, 'img':img})
                    i += 1
                except Exception as e:
                    print(f"Error extracting movie: {e}")
            
        df = pd.DataFrame(movie_list)
        return df


def scroll_down(driver, pause_time, max_scroll_attempts):
    # Track the last scroll height to detect if scrolling reaches the bottom
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    scroll_attempts = 0
    while scroll_attempts < max_scroll_attempts:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new items to load
        time.sleep(pause_time)
        
        # Get the new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            # If the height hasn't changed, assume we've reached the end of the page
            print(f"Reached the end of the page after {scroll_attempts} scrolls.")
            break
        
        # Log the current scroll height for debugging
        print(f"Scroll attempt {scroll_attempts + 1}, new height: {new_height}")
        
        last_height = new_height
        scroll_attempts += 1
    
'''
database operations
'''
def show_all_db(db_name):
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    c.execute(f"""
        SELECT * FROM {db_name} 
    """)
    items = c.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()

def delete_db(db_name):
    try:
        os.remove(f'{db_name}.db')
        print(f"Database '{db_name}.db'' deleted successfully.")
    except FileNotFoundError:
        print(f"Database '{db_name}.db'' not found.")
    except Exception as e:
        print(f"Error occurred while deleting database: {e}")

def delete_table(db_name, table_name):
    try:
        conn = sqlite3.connect(f'{db_name}.db')
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        print(f"Table '{table_name}' deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error occurred while deleting table: {e}")
    finally:
        conn.close()

def save_link_to_db(df, db_name, table_name, name_title, model, ):
    # connect to database
    conn = sqlite3.connect(f'{db_name}.db')
    c = conn.cursor()
    # create table
    # need to write different SQL for different table structure
    if model=="Category":
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {name_title} TEXT,
                link TEXT,
                is_dynamic INTEGER,
                slug TEXT
        """)
        # save data to db
        for _, row in df.iterrows():
            c.execute(f"""INSERT INTO {table_name} ({name_title}, link, is_dynamic, slug) 
                      VALUES (?, ?, ?, ?)""", 
                      (row['name'], row['link'], row['is_dynamic'], row['slug']))
    conn.commit()
    conn.close()

'''
crawl categories' names and their links
'''
def crawl_top250(url):
    _, headers, proxies = get_agents_headers_proxies()

    # anti-anti-crawling setting
    soup = get_soup(url, headers, proxies)

    # crawl top250 page link
    top250 = soup.find('div', class_ = 'douban-top250-hd').find('h2')
    link = top250.find('a')['href']
    top250.find('span').decompose()
    title = top250.get_text().replace('\n', '').replace(' ','').strip()
    df = pd.DataFrame([{'name':title, 'link': link}])
    # print(df)
    return df

def crawl_movie_types(url):
    _, headers, proxies = get_agents_headers_proxies()

    # anti-anti-crawling setting
    soup = get_soup(url, headers, proxies)

    # get all movie genre and revelent links
    genre = soup.find('div', class_='types').find_all('span')
    df = extract_movies(genre)
    df['link'] = 'https://movie.douban.com' + df['link']
    df['is_dynamic'] = 0
    name_slug_dic = {
        '剧情':'drama', '喜剧':'comedy', '动作':'action', '爱情':'romance', '科幻':'sci-fi', 
        '动画':'animation', '悬疑':'mystery', '惊悚':'thriller', '恐怖':'horror', '纪录片':'documentary', 
        '短片':'short-film', '情色':'erotic', '音乐':'music', '歌舞':'musical', '家庭':'family', 
        '儿童':'children', '传记':'biography', '历史':'history', '战争':'war', '犯罪':'crime', 
        '西部':'western', '奇幻':'fantasy', '冒险':'adventure', '灾难':'disaster', '武侠':'martial-arts', 
        '古装':'costume drama', '运动':'sports', '黑色电影':'film-noir'
    }
    for index, row in df.iterrows():
        key = row['name']
        df.at[index, 'slug'] = name_slug_dic.get(key)
    
    # get top250 link
    top250_link = crawl_top250(url).iloc[0]['link']
    new_top250_row = pd.DataFrame([{'name': 'Top250', 'link': top250_link, 'is_dynamic': True, 'slug': 'top-250'}])
    df = pd.concat([df, new_top250_row], ignore_index=True)

    # add new movies' row
    # new_link = 'https://movie.douban.com/chart'
    new_new_row = pd.DataFrame([{'name': 'New', 'link': url, 'is_dynamic': True, 'slug': 'new'}])
    df = pd.concat([df, new_new_row], ignore_index=True)

    return df

'''
 crawl movie names & their links
'''
def crawl_new_movies(url):
    _, headers, proxies = get_agents_headers_proxies()

    # anti-anti-crawling setting
    soup = get_soup(url, headers, proxies)

    # get all new movies' names & links
    movies = soup.find_all('div', class_ = 'pl2')

    df = extract_movies(movies)
    # print(df)
    # save_link_to_db(df, db_name = 'link', table_name = 'hot_movies', name_title = 'movie_name')
    return df

def crawl_top_movies(url):
    _, headers, proxies = get_agents_headers_proxies()

    # anti-anti-crawling setting
    soup = get_soup(url, headers, proxies)

    #get all top movies' names & links
    movies = soup.find_all('li', class_='clearfix')
    df = extract_movies(movies)
    # print(df)
    # save_link_to_db(df, db_name = 'link', table_name = 'hot_movies', name_title = 'movie_name')
    return df

def crawl_type_movies(url):
    user_agents, _, proxies = get_agents_headers_proxies()
    driver = set_chrome_options(user_agents, proxies, setting=False)
    driver.get(url)
     # Scroll down to load more content
    scroll_down(driver, pause_time=10, max_scroll_attempts=15)
    
    try:
        # Wait for the movies to be visible after scrolling
        movies = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'movie-content'))
        )
        print(f"Found {len(movies)} movies")
    except TimeoutException:
        print("Timed out waiting for page to load")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()  

    # Extract movies
    df = extract_movies(movies, setting='selenium')
    # print(df)
    # save_link_to_db(df, db_name = 'link', table_name = 'type_movies', name_title = 'movie_name')
    return df

def crawl_top250_movies(url):
    _, headers, proxies = get_agents_headers_proxies()

    #get all top movies' names & links
    movie_list = []
    for n in range(10):
        start_num = n*25
        page_url = f'?start={start_num}'
        # anti-anti-crawling setting
        soup = get_soup(url+page_url, headers, proxies)
        
        movies =  soup.find_all('div', class_='item')
        i = 1
        for movie in movies:
            name_elements = movie.find_all('span', class_ = 'title')
            name = ' '.join(element.text.strip() for element in name_elements)
            link = movie.find('a')['href']
            year_text = movie.find('p', class_="").get_text()
            match = re.search(r'\b\d{4}\b', year_text)
            if match:
                year = match.group(0)
                # print(f"Year: {year}")
            else:
                print("Cannot find a year")
            score = movie.find('sapn', class_="rating_num", property="v:average")
            img = movie.find('img')['src']
            # print(f"Movie {i} image source: {img}")
            item = {'name': name+' '+year,
                    'link': link,
                    'rate_score': score,
                    'img': img}
            movie_list.append(item)
            i += 1
    df = pd.DataFrame(movie_list)
    # print(df)
    # save_link_to_db(df, db_name = 'link', table_name = 'top250_movies', name_title = 'movie_name')
    return df

def get_agents_headers_proxies():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    proxies = {
        'http': 'http://47.121.183.107:8443'
        # 'https': 'https://47.121.183.107:8443'
    }
    return user_agents, headers, proxies

# url = 'https://movie.douban.com/chart'

# new_movies_df = crawl_new_movies(url)
# print(new_movies_df)

# top_movies_df = crawl_top_movies(url)
# print(top_movies_df)

# movie_types_df = crawl_movie_types(url)
# print(movie_types_df.iloc[0]['link'])

# url = 'https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action='
# type_movies_df = crawl_type_movies(url)
# print(type_movies_df)
# print(type_movies_df.iloc[0]['img'])

# url = 'https://movie.douban.com/chart'
# top250_df = crawl_top250(url)
# print(top250_df)

# url = 'https://movie.douban.com/top250'
# top250_movies_df = crawl_top250_movies(url)
# print(top250_movies_df)

