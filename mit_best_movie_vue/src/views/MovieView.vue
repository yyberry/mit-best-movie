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
    const route = useRoute(); // 获取路由参数
    const router = useRouter(); // 路由实例
    const movie = ref(null); // 电影详情数据
    const loading = ref(true); // 加载状态
    const error = ref(null); // 错误消息

    const fetchMovieDetails = async (movieSlug) => {
      try {
        const response = await axios.get(`/api/v1/movie/${movieSlug}/`);
        movie.value = response.data; // 保存返回的数据
        console.log('Fetched movie:', movie.value); 
      } catch (err) {
        error.value = "Failed to fetch movie details. Please try again.";
      } finally {
        loading.value = false; // 停止加载
      }
    };

    const markAsWatched = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        // 用户未登录，跳转到登录页面
        router.push("/log-in");
        return;
      }
      try {
        const data = { movie: movie.value.id };
        console.log('Sending data:', data);  // 打印请求数据
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
      const movieSlug = route.params.movie_slug; // 从路由中获取 movie_slug
      if (movieSlug) {
        fetchMovieDetails(movieSlug); // 获取电影详情
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
    height: 100vh; /* 让页面高度为视口高度 */
}

/* 加载和错误提示样式 */
.loading,
.error {
  text-align: center;
  font-size: 18px;
  color: #333;
}


/* 左边海报样式 */
.movie-poster {
  flex: 0.5; /* 固定宽度 */
  display: flex; /* 设置为 Flexbox 容器 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}

.movie-poster img {
  margin: 20px;
  width: 70%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 右边信息样式 */
.movie-info {
  flex: 0.5;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
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
