<template>
    <div class="page-my-account">
        
        <h1 class="title">Welcome {{ username }}</h1>

        <hr>
        <h2
            class="subtitle has-text-weight-bold has-text-primary is-clickable"
            @click="goToWatchedMovies"
        >
            Watched Movies >>
        </h2>
        
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else>
            <div v-if="watchedMovies.length === 0" class="columns is-fullwidth">
                <div class="column is-6 has-text-centered">
                    <p><strong class="m-3">No watched movies yet.</strong></p>
                    <button @click="goToBrowseMovies" class="button is-primary is-light m-3">
                        Browse Movies
                    </button>
                </div>
            </div>
            <div class="watched-movies-container">
                <div 
                    v-for="watchedmovie in watchedMovies" 
                    :key="watchedmovie.movie.id" 
                    class="card"
                >
                    <div class="card-image">
                        <figure class="image is-2by3">
                            <router-link :to="`/movie/${watchedmovie.movie.slug}`">
                                <img :src="getImage(watchedmovie.movie.poster)"  :alt="watchedmovie.movie.title"/>
                            </router-link>
                            
                        </figure>
                    </div>
                    <div class="card-content has-text-centered">
                        <h3 class="title is-6">{{ watchedmovie.movie.title }}</h3>
                        <p class="content"><strong>Watched on:</strong> {{ formatDate(watchedmovie.watched_at) }}</p>
                    </div>
                </div>
                
            </div>
        </div>
        <hr>
        <div>
            <button @click="logout" class="button is-danger m-5">Log out</button>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
    name: 'MyAccount',
    
    setup() {
        const store = useStore();
        const router = useRouter();

        const username = ref('');
        const watchedMovies = ref([]);
        const loading = ref(true);
        const error = ref(null);

        const fetchWatchedMovies = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await axios.get("/api/v1/watched-movies");
                watchedMovies.value = response.data;
                console.log("watched movies: ",watchedMovies.value)
            } catch (err) {
                error.value = "Failed to fetch watched movies.";
            } finally {
                loading.value = false;
            }
        };

        // log out function
        const logout = () => {
            axios.defaults.headers.common['Authorization'] = '';

            localStorage.removeItem('token');
            localStorage.removeItem('username');
            localStorage.removeItem('userid');

            store.commit('removeToken');
            router.push('/');
        };

        // redirect to Watched Movies page
        const goToWatchedMovies = () => {
            router.push('/watched-movies');
        };

        // redirect to Home page
        const goToBrowseMovies = () => {
            router.push('/'); // 
        };

        const getImage = (_url) => {
            console.log("image:", _url)
            if (_url) {
                const _u = _url.replace(/^https?:\/\//, "");
                return `http://images.weserv.nl/?url=${_u}`;
            }
        };

        const formatDate = (datetime) => {
            const date = new Date(datetime);
            return date.toISOString().split('T')[0]; // return 'YYYY-MM-DD' 
        };


        onMounted(() => {
            username.value =  localStorage.getItem('username') || 'Guest';
            fetchWatchedMovies();
        });


        return {
            username,
            watchedMovies,
            loading,
            error,
            logout,
            goToWatchedMovies,
            goToBrowseMovies,
            getImage,
            formatDate
        };
    },
};
</script>

<style scoped>
.page-my-account {
    margin-top: 50px;
    height: 100vh; 
}

.watched-movies-container {
  display: flex;
  overflow-x: auto; 
  gap: 20px; 
  padding-bottom: 15px; 
}

.card {
  flex-shrink: 0; 
  width: 200px; 
  height: 500px;
  overflow-y: auto;
  max-height: 500px;
}

</style>
