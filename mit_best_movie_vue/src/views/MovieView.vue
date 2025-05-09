<template>
    <div class="columns page-movie-detail">
        <div v-if="loading" class="has-text-centered is-5">Loading...</div>
        <div v-else-if="error" class="notification is-danger">{{ error }}</div>
        <div v-else class="column is-4 is-offset-4">
            <div class="movie-poster m-5">
                <img :src="getImage(movie.poster)" :alt="movie.title" />
            </div>

            <div>
                <h1 class="title has-text-centered">{{ movie.title }}</h1>
                <div class="is-flex is-justify-content-center">
                  <button
                    class="button"
                    :class="isWatched ? 'is-danger m-3' : 'is-primary is-light m-3'"
                    @click="toggleWatched(movie.id)"
                  >
                    {{ isWatched ? "Remove from Watched" : "Watched" }}
                  </button>
                </div>
                <p class="has-text-centered"><strong>Rating:</strong> {{ movie.rating }}</p>
                <div class="has-text-centered m-3">
                  <strong>Genre: </strong>
                  <router-link 
                    :to="`/category/${category.slug}`" 
                    v-for="category in movie.categories" 
                    :key="category.slug"
                    class="category-link"
                  >
                      {{ category.slug }}&nbsp;
                  </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { toast } from 'bulma-toast';

export default {
  setup() {
    const route = useRoute(); 
    const router = useRouter(); 
    const movie = ref(null); 
    const loading = ref(true); 
    const error = ref(null); 
    const isWatched = ref(false);

    const fetchMovieDetails = async (movieSlug) => {
      try {
        const response = await axios.get(`/api/v1/movie/${movieSlug}/`);
        movie.value = response.data.movie; 
        isWatched.value = response.data.is_watched;
      } catch (err) {
        error.value = "Failed to fetch movie details. Please try again.";
      } finally {
        loading.value = false; // stop loading
      }
    };

    // Remove movie from watched list
    const removeFromWatched = async (movieId) => {
      try {
        const response = await axios.delete(`/api/v1/watched-movies/${movieId}/`);
        toast({
              message: response.data.message,
              type: 'is-success',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'top-center',
            });
      } catch (error) {
        console.error('Error removing movie:', error);
      }
    };

     const markAsWatched = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        // if the user is not logged in, redirect to the login page
        router.push("/log-in");
        toast({
              message: "Please log in to mark the movie as watched.",
              type: 'is-warning',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'top-center',
            });
        return;
      }
      try {
        const data = { movie: movie.value.id };
        console.log('Sending data:', data);  
        const response = await axios.post(
            "/api/v1/watched-movies/",
            data
        );
        toast({
              message: response.data.message,
              type: 'is-success',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'top-center',
            });
      } catch (err) {
        console.log('err:', err);
        error.value = "Failed to mark the movie. Please try again.";
      }
    };

    const toggleWatched = async (movieId) => {
      if (!isWatched.value) {
        await markAsWatched();
        isWatched.value = true;
      } else {
        await removeFromWatched(movieId);
        isWatched.value = false;
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
      error,
      isWatched,
      removeFromWatched,
      getImage,
      markAsWatched,
      toggleWatched,
    };
  },
};
</script>
<style scoped>
.page-movie-detail {
    height: 100vh; 
    margin-top: 50px;
}

.movie-poster {
  flex: 0.5; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
}

.movie-poster img {
  width: 80%;
  height: auto;
  border-radius: 1vw;
}

</style>
