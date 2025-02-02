<template>
  <div class="columns page-movie-detail">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="column is-4 is-offset-4">
      <div class="movie-poster">
        <img :src="getImage(movie.poster)" :alt="movie.title" />
      </div>

      <div class="movie-info">
        <h1 class="title">{{ movie.title }}</h1>
        
        <!-- Watched button -->
        <button 
          class="button is-primary" 
          @click="markAsWatched"
        >
          Watched
        </button>

        <p><strong>Rating:</strong> {{ movie.rating }}</p>
        <p>
          <strong>Genre:</strong>
          <router-link 
            :to="`/category/${category.slug}`" 
            v-for="category in movie.categories" 
            :key="category.slug"
            class="category-link"
          >
            {{ category.slug }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";

export default {
  setup() {
    const route = useRoute(); 
    const router = useRouter(); 
    const movie = ref(null); 
    const loading = ref(true); 
    const error = ref(null); 

    const fetchMovieDetails = async (movieSlug) => {
      try {
        const response = await axios.get(`/api/v1/movie/${movieSlug}/`);
        movie.value = response.data; 
        console.log('Fetched movie:', movie.value); 
      } catch (err) {
        error.value = "Failed to fetch movie details. Please try again.";
      } finally {
        loading.value = false; // stop loading
      }
    };

    const markAsWatched = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        // if the user is not logged in, redirect to the login page
        router.push("/log-in");
        return;
      }
      try {
        const data = { movie: movie.value.id };
        console.log('Sending data:', data);  
        const response = await axios.post(
            "/api/v1/watched-movies/",
            data
        );
        alert("Movie marked as watched!");
      } catch (err) {
        console.log(err);
        alert("Failed to mark the movie. Please try again.");
      }
    };

    const getImage = (_url) => {
      if (_url) {
        const _u = _url.replace(/^https?:\/\//, "");
        return `http://images.weserv.nl/?url=${_u}`;
      }
    };

    onMounted(() => {
      const movieSlug = route.params.movie_slug; // get the movie_slug from the route
      if (movieSlug) {
        fetchMovieDetails(movieSlug); 
      } else {
        error.value = "Movie slug is missing in the URL.";
        loading.value = false;
      }
    });

    return {
      movie,
      loading,
      getImage,
      error,
      markAsWatched,
    };
  },
};
</script>
<style scoped>
.page-movie-detail {
    margin-top: 50px;
    height: 100vh; 
}

.loading,
.error {
  text-align: center;
  font-size: 18px;
  color: #333;
}

.movie-poster {
  flex: 0.5; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.movie-poster img {
  margin: 20px;
  width: 70%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.movie-info {
  flex: 0.5;
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;
  padding-left: 20px;
}

.title {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.category-link {
  color: #3273dc;
  text-decoration: none;
  margin-right: 5px;
}

.category-link:hover {
  text-decoration: underline;
}
</style>
