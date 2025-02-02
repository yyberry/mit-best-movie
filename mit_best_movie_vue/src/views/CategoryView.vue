<template>
  <div>
    <div v-if="isLoading" class="overlay">
      <div class="loading-message">Loading...</div>
    </div>

    <!-- 标题 -->
    <div class="category-title">
        <h1 class="title is-1">{{ categorySlug.toUpperCase() }} Movies</h1>
        <button 
            v-if="isDynamic" 
            class="button is-primary is-small" 
            @click="refreshCategory"
            :disabled="isLoading"
        >
            Refresh
        </button>
    </div>

    <!-- 电影列表 -->
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

    const route = useRoute(); // 获取当前路由对象

    // 获取电影数据
    const fetchMoviesByCategory = async (cSlug) => {
      try {

        const response = await axios.get(`/api/v1/category/${cSlug}/`);
        movies.value = response.data;

        // 获取所有类别数据并找到对应的类别
        const categoryResponse = await axios.get(`/api/v1/categories/`);
        const category = categoryResponse.data.find((c) => c.slug === cSlug);

        // 如果找到对应的类别，设置 isDynamic
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

    // 刷新类别电影
    const refreshCategory = async () => {
      isLoading.value = true; 
      try {
        await axios.post(`/api/v1/category/${categorySlug.value}/refresh/`);
        await fetchMoviesByCategory(categorySlug.value); // 刷新后重新获取数据
      } catch (error) {
        console.error('Error refreshing category:', error);
      } finally {
        isLoading.value = false; // 关闭等待提示
      }
    };

    // 获取海报图片 URL
    const getImage = (_url) => {
      if (_url) {
        const _u = _url.replace(/^https?:\/\//, "");
        return `http://images.weserv.nl/?url=${_u}`;
      }
    };

    // 获取类别 slug 并请求数据
    onMounted(() => {
      const cSlug = route.params.category_slug; // 从 URL 获取类别 slug
      fetchMoviesByCategory(cSlug);
    });

    // 使用 watch 来监听路由参数变化
    watch(
      () => route.params.category_slug, // 监听路由参数的变化
      (newSlug, oldSlug) => {
        // 当 category_slug 变化时重新加载数据
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

/* 遮罩层样式 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 确保遮罩层在最上层 */
}

/* 等待提示文字样式 */
.loading-message {
  color: white;
  font-size: 2rem;
  font-weight: bold;
}
</style>
