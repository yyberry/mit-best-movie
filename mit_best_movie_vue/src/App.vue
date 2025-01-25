<template>
  <div id="wrapper">
    <nav :class="['navbar', { show: state.showNavbar }]">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Mit Best Movie</strong></router-link>

        <a class="navbar-burger" role="button" aria-label="menu" aria-expanded="false" data-target="navbar-menu" @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" :class="{ 'is-active': showMobileMenu }">
        <div class="navbar-end">
          <router-link to="/" class="navbar-item">Home</router-link>

          <div class="navbar-item has-dropdown" :class="{ 'is-active': showMovieCategories }">
            <div class="navbar-link" @click="toggleDropdown('showMovieCategories')">Movies</div>
            <ul class="navbar-dropdown" v-show="showMovieCategories">
              <li><router-link to="/category/new" class="navbar-item">New movies</router-link></li>
              <li><router-link to="/category/top-250" class="navbar-item">Top 250</router-link></li>
              <li class="navbar-link navbar-item" @click="toggleDropdown('showOtherCategories')">Movie Genre</li>
              <div class="navbar-item has-dropdown" :class="{ 'is-active': showOtherCategories }">
                <div class="navbar-dropdown" v-show="showOtherCategories">
                  <router-link 
                    :to="`/category/${category.slug}`" 
                    class="navbar-item"
                    v-for="category in categories"
                    :key="category.slug"
                  >
                    {{category.slug}}
                  </router-link>
                </div>
              </div>
            </ul>
          </div>

          <router-link to="/about" class="navbar-item">About</router-link>

          <div class="navbar-item">
            <template v-if="$store.state.isAuthenticated">
                <router-link to="/my-account" class="button is-primary is-light">My account</router-link>
              </template>

              <template v-else>
                <router-link to="/log-in" class="button is-primary is-light">Log in</router-link>
              </template>

          </div>

        </div>
      </div>
    </nav>

    <section class="section">
      <router-view></router-view>
    </section>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, onBeforeMount } from "vue";
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  setup() {
    // 响应式数据
    const showMobileMenu = ref(false);
    const showMovieCategories = ref(false);
    const showOtherCategories = ref(false);
    const categories = ref([])
    const state = reactive({
      lastScrollTop: 0, // 上次滚动位置
      showNavbar: false, // 控制 navbar 显示与隐藏
    });
    const store = useStore();


    // 处理滚动事件
    const handleScroll = () => {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (currentScrollTop > state.lastScrollTop) {
        state.showNavbar = true; // 向下滚动并且距离大于 50 时，显示 navbar
      } else if (currentScrollTop < state.lastScrollTop) {
        state.showNavbar = false; // 向上滚动或滚动距离小于等于 50，隐藏 navbar
      }

      state.lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop; // 防止负值
    };

    // 切换菜单显示状态
    const toggleDropdown = (menu) => {
      if (menu === "showMovieCategories") {
        showMovieCategories.value = !showMovieCategories.value;
      } else if (menu === "showOtherCategories") {
        showOtherCategories.value = !showOtherCategories.value;
      }
    };

    const fetchData =  async () =>{
      try {
        const response = await axios.get("/api/v1/categories/");
        categories.value = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error.response);
      }
    }

    // 生命周期钩子
    // 在组件挂载之前执行
    onBeforeMount(() => {
      store.commit('initializeStore');  // 初始化 store

      const token = store.state.token;

      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Token ' + token;
      } else {
        axios.defaults.headers.common['Authorization'] = '';
      }
    });

    onMounted(() => {
      window.addEventListener("scroll", handleScroll);
      fetchData()
    });

    onUnmounted(() => {
      window.removeEventListener("scroll", handleScroll);
    });

    return {
      showMobileMenu,
      showMovieCategories,
      showOtherCategories,
      state,
      categories,
      toggleDropdown,
    };
  },
};
</script>

<style scoped>
.section {
  padding: 1px; /* 或者设置为你需要的内边距 */
}

.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  opacity: 0; /* 默认隐藏 navbar */
  visibility: hidden; /* 隐藏 navbar */
  transition: opacity 0.5s ease, visibility 0.5s ease; /* 设置透明度和可见性的渐变效果 */
  z-index: 1000; /* 保证 navbar 显示在其他内容上面 */
}

.navbar.show {
  opacity: 1; /* 显示 navbar */
  visibility: visible; /* 设置 navbar 为可见 */
}

/* 设置 Movie 下拉框的样式 */
.navbar-dropdown {
  overflow-y: auto;  /* 启用垂直滚动条 */
  position: absolute;  /* 改为绝对定位 */
  top: 100%; /* 让下拉框显示在父元素下方 */
  left: 0;  /* 对齐父元素的左边 */
  z-index: 1000;  /* 确保下拉框显示在其他元素之上 */
  width: auto;  /* 自动宽度，根据内容调整 */
  height: auto;
  max-height: 300px; /* 设置最大高度，避免过长 */
}

.navbar-item.has-dropdown {
  position: relative; /* 使下拉菜单相对于此元素定位 */
}

</style>


