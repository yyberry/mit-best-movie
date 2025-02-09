# Mit Best Movie:  A **personalized** movie **management** and **tracking** website.

For a movie enthusiast like me, one of the most frustrating experiences is getting spoiled by plot summaries when searching for a movie to watch. Additionally, even after watching a movie, it often remains on the homepage, making it harder to discover new films efficiently. To solve these problems, I built this website to help users find great, unwatched movies. All the data used on this site is scraped from the internet and is intended for personal learning purposes only. Commercial use is strictly prohibited. 

## User Operations

1. **User Registration**: Users can register an account by setting a username and password.
2. **User Login**: Registered users can log in using their credentials. Upon login, they are redirected to the "My Account" page, where up to five movies marked as watched are displayed.
3. **User Logout**: After logging in, a "Log Out" button is available next to the username on the "My Account" page. Clicking it will log the user out and redirect them to the homepage.

## Movie Operations

1. **For Guests**:
   - **Browsing Movies**: Guests can explore the top six highest-rated movies on the homepage, along with the top seven highest-rated movies for each genre. Clicking on a movie poster leads to the movie details page, which displays the poster, rating, and genres. Clicking on a genre redirects to the category page, showing all movies in that category.
   - **Navigation Bar**: The navigation bar can be summoned by scrolling down on any page, allowing easy access to different sections of the website.
   - **Movie Refresh**: I have categorized movies into two types based on whether they are dynamic. Dynamic categories are automatically updated every week, while non-dynamic categories must be updated manually. Additionally, I have added a 'Trigger Update' button in Django Admin for manual updates.
2. **For Logged-in Users**:
   - **Marking Movies as Watched**:
     Logged-in users can mark movies as watched from the movie details page. Once marked, the movie will be hidden from other pages and will only appear on the user's **"My Account"** page. If a user has more than five watched movies, they can visit the **"Watched Movies"** page to view the full list.
   
     On the **"Watched Movies"** page, users can also remove the 'Watched' label. Once removed, the movie will reappear on other pages as usual.
