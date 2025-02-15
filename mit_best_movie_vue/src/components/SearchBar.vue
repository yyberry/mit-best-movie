<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="query"
      @input="searchMovies"
      placeholder="Search for a movie..."
      class="input is-primary"
    />
    <div v-if="results.length > 0" class="search-results">
      <div
        v-for="movie in results"
        :key="movie.id"
        @click="goToMovie(movie.slug)"
        class="search-item"
      >
        <img :src="getImage(movie.poster)" :alt="movie.title" class="poster" />
        <span>{{ movie.title }}, {{movie.slug}}</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
    setup(){
        const query = ref('');
        const results = ref([]);
        const router = useRouter();
        
        const searchMovies = async () => {
            if (query.value.length < 1) {
                results.value =[];
                return;
            }
            try {
                const response = await axios.get(`/api/v1/search/?q=${query.value}`);
                console.log(response.data);
                results.value = response.data || [];
            } catch (error) {
                console.log("searching for:", error);
            }
        };

        const goToMovie = async(movieSlug) => {
            console.log("movie slug: ", movieSlug)
            router.push(`/movie/${movieSlug}`);
        };

        // get the poster image URL
        const getImage = (_url) => {
            if (_url) {
                const _u = _url.replace(/^https?:\/\//, "");
                return `http://images.weserv.nl/?url=${_u}`;
            }
        };

        return {
            query,
            results,
            searchMovies,
            goToMovie,
            getImage,
        };
    },
};
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 100%;
  margin: auto;
}

.search-results {
  position: absolute;
  background: white;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
}

.search-item {
  display: flex;
  align-items: center;
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.search-item:hover {
  background: #f0f0f0;
}

.poster {
  width: 40px;
  height: 60px;
  margin-right: 10px;
}
</style>
