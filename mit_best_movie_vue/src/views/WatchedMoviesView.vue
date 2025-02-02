<template>
  <div>
    <div v-if="isLoading" class="overlay">
      <div class="loading-message">Loading...</div>
    </div>

    <!-- title -->
    <div class="page-title">
      <h1 class="title is-1">Watched Movies</h1>
    </div>

    <!-- movie list -->
    <div class="movies-list">
      <div v-for="(watchedMovie, index) in watchedMovies" :key="index" class="card">
        <div class="card-image">
          <figure class="image is-2by3">
            <router-link :to="`/movie/${watchedMovie.movie.slug}`">
              <img :src="getImage(watchedMovie.movie.poster)" :alt="watchedMovie.movie.title" />
            </router-link>
          </figure>
        </div>

        <div class="card-content">
          <h3 class="title is-4">{{ watchedMovie.movie.title }}</h3>
          <p class="content"><strong>Watched on:</strong> {{ formatDate(watchedMovie.watched_at) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const watchedMovies = ref([]);
    const isLoading = ref(false);

    const fetchWatchedMovies = async () => {
      isLoading.value = true;
      try {
        const response = await axios.get('/api/v1/watched-movies/');
        watchedMovies.value = response.data;
      } catch (error) {
        console.error('Error fetching watched movies:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // get the poster image URL
    const getImage = (url) => {
      if (url) {
        const _url = url.replace(/^https?:\/\//, "");
        return `http://images.weserv.nl/?url=${_url}`;
      }
    };

    const formatDate = (datetime) => {
      const date = new Date(datetime);
      return date.toISOString().split('T')[0]; // return 'YYYY-MM-DD' 
    };

    onMounted(() => {
      fetchWatchedMovies();
    });

    return {
      watchedMovies,
      isLoading,
      getImage,
      formatDate
    };
  }
};
</script>

<style scoped>
.page-title {
  text-align: center;
  margin-top: 20px;
}

.movies-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.card:hover {
  transform: translateY(-5px);
}

/* mask (overlay) */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* ensure the mask (overlay) appears on the topmost layer */
}

/* loading message */
.loading-message {
  color: white;
  font-size: 2rem;
  font-weight: bold;
}
</style>
