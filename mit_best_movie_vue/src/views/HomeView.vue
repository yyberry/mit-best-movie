<template>
  <div>
    <div :class="['main-container', { show: showMainContainer }]">
    <!-- <div class="main-container" v-show="showMainContainer"> -->
      <div class="content">
        <div class="text-section">
          <h1>A Movie Website Built for Me, by Me!</h1>
          <strong>Tailored Features</strong>
          <strong>Track & Update with Ease</strong>
          <strong>Built for My Preferences</strong>
        </div>
        <div class="poster-section">
          <div
            class="poster"
            v-for="(newMovie, newIndex) in newMovies"
            :key="newIndex"
            :style="getPosterStyle(newIndex)"
            @mouseover="onHover(newIndex)"
            @mouseleave="onLeave(newIndex)"
          >
            <router-link :to="`/movie/${newMovie.slug}`">
                <img :src="getImage(newMovie.poster)" :alt="newMovie.title" />
            </router-link>
            <div class="movie-info">
              <h3>{{ newMovie.title }}</h3>
              <p>rating: {{ newMovie.rating }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-for="(category, categoryIndex) in categories" :key="categoryIndex" class="category-section">
      <router-link :to="`/category/${category.category}`">
        <h2 class="category-title">{{ category.category || 'No Title' }}</h2>
      </router-link>
      <div id="banner">
        <div class="carousel">
          <div
            v-for="(movie, index) in category.movies"
            :key="index"
            class="carousel-item"
            :style="getItemStyle(index, categoryIndex)"
          >
            <router-link :to="`/movie/${movie.slug}`">
              <img :src="getImage(movie.poster)" :alt="movie.title" />
            </router-link>
            
            <div class="image-info has-text-white">
              <h3>{{ movie.title }}</h3>
              <p>rating: {{ movie.rating }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="navigation-buttons">
        <button @click="handleClick('prev', categoryIndex)" class="nav-button left">
          <strong>←</strong> 
        </button>
        <button @click="handleClick('next', categoryIndex)" class="nav-button right">
          <strong>→</strong>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

export default {
  setup() {
    const newMovies = ref([]); // new电影数据
    const categories = ref([]);
    const currentIndexMap = reactive({}); // 每个类别当前显示的电影索引
    const hoveredIndex = ref(null); // 当前悬停的海报索引
    const currentIndex = ref(0); // 当前居中的索引
    const lastScrollTop = ref(0); // 上次滚动的位置
    const showMainContainer = ref(false);

    const getImage = (_url) => {
      if (_url) {
        const _u = _url.replace(/^https?:\/\//, "");
        return `http://images.weserv.nl/?url=${_u}`;
      }
    };

    const getPosterStyle = (index) => {
      const isHovered = hoveredIndex.value === index;
      const isLeftColumn = index % 2 === 0;
      const offsetX = isLeftColumn ? "10%" : "45%"; 
      const offsetY = Math.floor(index / 2) * 30;
      const tiltAngle = 25;

      return {
        position: "absolute",
        top: `${offsetY}%`,
        left: `${offsetX}`,
        transform: isHovered ? `scale(1.2) rotate(0deg)` : `rotate(${tiltAngle}deg)`,
        zIndex: isHovered ? 100 : 1,
        transition: "transform 0.3s ease, z-index 0.3s ease",
      };
    };

    const onHover = (index) => {
      hoveredIndex.value = index;
    };

    const onLeave = () => {
      hoveredIndex.value = null;
    };

    const handleClick = (direction, categoryIndex) => {
      if (direction === "next") {
        currentIndexMap[categoryIndex] = (currentIndexMap[categoryIndex] + 1) % categories.value[categoryIndex].movies.length;
      } else if (direction === "prev") {
        currentIndexMap[categoryIndex] = (currentIndexMap[categoryIndex] - 1 + categories.value[categoryIndex].movies.length) % categories.value[categoryIndex].movies.length;
      }
    };

    const getItemStyle = (index,categoryIndex) => {
      const total = categories.value[categoryIndex].movies.length;
      const offset = (index - currentIndexMap[categoryIndex] + total) % total;
      let translateX = 0;
      let zIndex = 0;
      let scale = 1;

      if (offset === 0) {
        translateX = 0;
        zIndex = 10;
        scale = 1;
      } else if (offset <= Math.floor(total / 2)) {
        translateX = offset * 150;
        zIndex = 10 - offset;
        scale = 1 - offset * 0.1;
      } else {
        translateX = (offset - total) * 150;
        zIndex = 10 - (total - offset);
        scale = 1 - (total - offset) * 0.1;
      }

      return {
        transform: `translateX(${translateX}px) scale(${scale})`,
        zIndex: zIndex,
        transition: "transform 0.5s ease, z-index 0.5s ease",
      };
    };

    const handleScroll = () => {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (currentScrollTop > lastScrollTop.value && currentScrollTop > 1) {
        showMainContainer.value = true;
      } else if (currentScrollTop < lastScrollTop.value || currentScrollTop <= 1) {
        showMainContainer.value = false;
      }

      lastScrollTop.value = currentScrollTop <= 0 ? 0 : currentScrollTop;
    };

    // 获取数据
    const fetchData = () => {
      axios.get("/api/v1/new-movies/").then((response) => {
        newMovies.value = response.data;
      });
      axios.get("/api/v1/top-movies/").then((response) => {
        categories.value = response.data;
        categories.value.forEach((_, index) => {
          currentIndexMap[index] = 0;
        });
      });
    };

    // 生命周期钩子
    onMounted(() => {
      window.addEventListener("scroll", handleScroll);
      fetchData();
    });

    onBeforeUnmount(() => {
      window.removeEventListener("scroll", handleScroll);
    });

    return {
      newMovies,
      categories,
      currentIndexMap,
      hoveredIndex,
      currentIndex,
      showMainContainer,
      getImage,
      getPosterStyle,
      onHover,
      onLeave,
      handleClick,
      getItemStyle,
      handleScroll,
    };
  },
};
</script>

<style scoped>

.main-container {
  position: relative;
  width: 100%;
  height: 100vh; /* 全屏高度 */
  margin: 0;
  background-size: cover;
  background-position: top center;
  background-attachment: fixed; /* 背景图固定不随滚动 */
  overflow: hidden;

  opacity: 1;
  visibility: visible;
  transition: opacity 2s ease, visibility 2s ease;

}

.main-container.show{
  opacity: 0;
  visibility: hidden;
}

.content {
  display: flex;
  justify-content: flex-start; /* 内容靠左排列 */
  align-items: flex-start;
  height: 100%;
}

.text-section {
  position: relative;
  flex: 0.5; /* 减小文字区域 */
  /* padding-left: 5%; */
  color: black;
  font-size: 1vw;
  line-height: 2vw;
  display: flex;
  justify-content: center; /* 文字居中 */
  align-items: center;
  height: 100vh;
  flex-direction: column;
}

.poster-section {
  position: relative;
  flex: 0.5; /* 增大海报区域 */
  height: 100%; /* 保证海报占满区域 */
  width: 100%;
  overflow: hidden; /* 限制超出区域的海报不可见 */
  padding: 0%;
}

.poster {
  position: relative;
  transition: transform 0.3s ease-in-out;
}

.poster:hover {
  z-index: 100; /* 让悬停的海报位于最上层 */
}

.poster img {
  width: 240px; /* 增大海报尺寸 */
  height: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); /* 阴影效果 */
  border-radius: 6px; /* 圆角边框 */
  transition: opacity 0.3s ease-in-out; /* 添加海报透明度过渡效果 */
}

.poster:hover img {
  opacity: 0.8; /* 鼠标悬停时海报变透明 */
}

.movie-info {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) ; 
  text-align: center;
  color: white;
  visibility: hidden;
  opacity: 0;
  transition: visibility 0.3s, opacity 0.3s;
}

.movie-info h3 {
  color: white !important;
}

.poster:hover .movie-info {
  visibility: visible;
  opacity: 1;
}

.movie-info h3,
.movie-info p {
  margin: 0;
}

/* 类别标题样式 */
.category-title {
  text-align: center;
  margin: 4rem 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: bold;
}

/* 每个类别的容器样式 */
.category-section {
  margin-bottom: 2rem;
}


#banner {
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1000px;
  height: 50vh;
  position: relative;
}

.carousel {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%; /* 横向铺满屏幕 */
  height: 80%;
}

.carousel-item {
  position: absolute;
  width: 18rem;
  height: 24rem;
  backface-visibility: hidden;
  transition: transform 0.5s ease, z-index 0.5s ease;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.image-info {
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1rem;
  color: white;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.7);
}

.navigation-buttons {
  position: relative;
  bottom: 5%;
  width: 100%;
  display: flex;
  justify-content: center; /* 居中对齐 */
  gap: 1rem; /* 设置按钮之间的间距 */
}

.nav-button {
  /* background: white; */
  border: white;
  border: 1px solid white;
  cursor: pointer;
  border-radius: 50%;
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

</style>
