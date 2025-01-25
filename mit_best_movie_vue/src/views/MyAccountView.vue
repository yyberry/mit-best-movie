<template>
    <div class="page-my-account">
        <div class="columns">
            <div class="column is-4">
                <h1 class="title">Welcome {{ username }}</h1>
            </div>

            <div class="column is-4">
                <button @click="logout" class="button is-danger">Log out</button>
            </div>
                
        </div>

        <hr>

        <div class="columns">
            <div class="column is-12">
                <h2
                    class="subtitle has-text-weight-bold has-text-primary is-clickable"
                    @click="goToWatchedMovies"
                >
                    Watched Movies
                </h2>
            </div>
        </div>
        
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else>
            <div class="columns is-multiline">
                <div 
                    v-for="watchedmovie in watchedMovies" 
                    :key="watchedmovie.movie.id" 
                    class="column is-2"
                >
                    <div class="card">
                        <div class="card-image">
                            <figure class="image is-2by3">
                                <router-link :to="`/movie/${watchedmovie.movie.slug}`">
                                    <img :src="getImage(watchedmovie.movie.poster)"  :alt="watchedmovie.movie.title"/>
                                </router-link>
                                
                            </figure>
                        </div>
                        <div class="card-content">
                            <h3 class="title is-4">{{ watchedmovie.movie.title }}</h3>
                            <p class="content"><strong>Watched on:</strong> {{ formatDate(watchedmovie.watched_at) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <hr>
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

        // 获取用户名
        const username = ref('');
        const watchedMovies = ref([]);
        const loading = ref(true);
        const error = ref(null);

        const fetchWatchedMovies = async () => {
            try {
                const token = localStorage.getItem("token");
                const response = await axios.get("/api/v1/watched-movies/");
                watchedMovies.value = response.data;
                console.log("watched movies: ",watchedMovies.value)
            } catch (err) {
                error.value = "Failed to fetch watched movies.";
            } finally {
                loading.value = false;
            }
        };

        // 登出功能
        const logout = () => {
            axios.defaults.headers.common['Authorization'] = '';

            localStorage.removeItem('token');
            localStorage.removeItem('username');
            localStorage.removeItem('userid');

            store.commit('removeToken');
            router.push('/');
        };

        // 跳转到 Watched Movies 页面
        const goToWatchedMovies = () => {
            router.push('/watched-movies');
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
            return date.toISOString().split('T')[0]; // 返回 'YYYY-MM-DD' 格式
        };


        onMounted(() => {
            // 从 localStorage 或 Vuex 获取用户名
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
            getImage,
            formatDate
        };
    },
};
</script>

<style scoped>
.page-my-account {
    margin-top: 50px;
    height: 100vh; /* 让页面高度为视口高度 */
}

</style>
