# Mit Best Movie:  A **personalized** movie **management** and **tracking** website.

For a movie enthusiast like me, one of the most frustrating experiences is getting spoiled by plot summaries when searching for a movie to watch. Additionally, even after watching a movie, movies often remain on the homepage, making it harder to discover new films efficiently.

To solve these problems, I built this website to help users find great, unwatched movies. All data used on this site is scraped from the internet and is intended **for personal learning purposes only**. **Commercial use is strictly prohibited.**

You can visit the website at [https://mitbestmovie.info](https://mitbestmovie.info).

## 📌 Features  

### 🍿 User Operations 

1. **User Registration**: Create an account with a username and password.
2. **User Login**: Log in to access personalized features. The "My Account" page displays watched movies.
3. **User Logout**: Click the "Log Out" button to securely log out and return to the homepage.

###  🎬 Movie Operations

1. - #### 🔹 For Guests
   
     - **Browse Movies**:
       - The homepage highlights the **top six highest-rated movies** and the **top seven highest-rated movies per genre**.
       - Clicking a movie poster leads to a **movie details page** with rating, genre, and a link to browse similar films.
     - **Navigation Bar**: Scroll down to reveal the navbar for quick access to different sections.
     - **Dynamic Movie Updates**:
       - Movies are categorized as **dynamic** (updated automatically every week) or **non-dynamic** (manual updates via Django Admin).
     - **Search Movies**:
       - Use the navbar search bar to find movies by title. Search results update **dynamically** as you type.
       - Clicking a search result navigates to the corresponding movie details page.
   
2. **For Logged-in Users**:
   - **Mark Movies as Watched**:
     - Users can mark movies as **"Watched"** from the **movie details page**.
     - Watched movies will be **hidden from other pages** and appear only in the **"My Account"** section.
   - **Unmark Watched Movies**:
     - From the **"Watched Movies"** page or **movie details page**, users can remove the "Watched" label.
     - Once removed, the movie will **reappear in listings** as usual.

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your_username/mit_best_movie.git
cd mit_best_movie
```

### 2️⃣ Backend Setup (Django)

#### 🔹 Install Backend Dependencies

```
pip install -r requirements.txt
```

#### 🔹 Start the Server

```
python manage.py runserver
```

### 3️⃣ Frontend Setup (Vue.js)

#### 🔹 Navigate to Frontend Directory & Install Frontend Dependencies

```
npm install
```

#### 🔹 Start the Vue Development Server

```
npm run serve
```

## 🛠 Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: Vue.js
- **Database**: PostgreSQL
- **Scraping**: BeautifulSoup & Selenium

## 
