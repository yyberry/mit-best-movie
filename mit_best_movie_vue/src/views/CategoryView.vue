<template>
  <div>
    <div v-if="isLoading" class="overlay">
      <div class="loading-message">Loading...</div>
    </div>

    <!-- title -->
    <div class="category-title">
        <h1 class="title is-1 m-2">{{ categorySlug.toUpperCase() }} Movies</h1>
        <button 
            v-if="isDynamic" 
            class="button is-primary is-small m-5" 
            @click="refreshCategory"
            :disabled="isLoading"
        >
            Refresh
        </button>
    </div>

    <!-- movies list -->
    <div class="movies-list">
      <div v-for="(movie, movieIndex) in movies" :key="movieIndex" class="card">
        <div class="card-image">
          <figure class="image is-2by3">
            <router-link :to="`/movie/${movie.slug}`">
                <img :src="getImage(movie.poster)" :alt="movie.title" />
            </router-link>
          </figure>
        </div>
        
        <div class="card-content">
          <h3 class="title is-4">{{ movie.title }}</h3>
          <p class="content">Rating: {{ movie.rating }}</p>
          <p class="content">
            Genre: 
            <router-link 
              :to="`/category/${category.slug}`" 
              v-for="category in movie.categories" 
              :key="category.slug"
            >
              {{ category.slug }},
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref, onMounted } from 'vue';
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

export default {
  setup() {
    const movies = ref([]);
    const categorySlug = ref('');
    const isDynamic = ref(false);
    const isLoading = ref(false);

    const route = useRoute(); // get the current route object

    // get movie data
    const fetchMoviesByCategory = async (cSlug) => {
      try {

        const response = await axios.get(`/api/v1/category/${cSlug}/`);
        movies.value = response.data;

        // get all tags and find the corresponding category
        const categoryResponse = await axios.get(`/api/v1/categories/`);
        const category = categoryResponse.data.find((c) => c.slug === cSlug);

        // f the corresponding category is found, set the value of isDynamic
        if (category) {
            isDynamic.value = category.is_dynamic;
        } else {
            console.error(`Category with slug "${cSlug}" not found.`);
            if (cSlug == 'new' || cSlug == 'top-250'){
                isDynamic.value = true //manually set the value to true for the known cases
            } else {
                
            }
            
        }

        categorySlug.value = cSlug;
      } catch (error) {
        console.error('Error fetching movies:', error);
      }
    };

    // refresh movies
    const refreshCategory = async () => {
      isLoading.value = true; 
      try {
        await axios.post(`/api/v1/category/${categorySlug.value}/refresh/`);
        await fetchMoviesByCategory(categorySlug.value); // re-fetch the data after the page refresh
      } catch (error) {
        console.error('Error refreshing category:', error);
      } finally {
        isLoading.value = false; // close the loading indicator
      }
    };

    // get the poster image URL
    const getImage = (_url) => {
      if (_url) {
        const _u = _url.replace(/^https?:\/\//, "");
        return `http://images.weserv.nl/?url=${_u}`;
      }
    };

    // get the category slug and request the data
    onMounted(() => {
      const cSlug = route.params.category_slug; // get the category slug from the URL
      fetchMoviesByCategory(cSlug);
    });

    watch(
      () => route.params.category_slug, 
      (newSlug, oldSlug) => {
        // reload the data when the category_slug changes
        if (newSlug !== oldSlug) {
          fetchMoviesByCategory(newSlug);
        }
      }
    );

    return {
      movies,
      categorySlug,
      isDynamic,
      isLoading,
      refreshCategory,
      getImage
    };
  }
};
</script>

<style scoped>
.category-title {
  text-align: center;
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
