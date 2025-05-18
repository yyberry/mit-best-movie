<template>
  <div id="wrapper">
    <nav :class="['navbar', { show: state.showNavbar }]">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Mit Best Movie</strong></router-link>

        <a 
          class="navbar-burger" 
          role="button" 
          aria-label="menu" 
          aria-expanded="false" 
          data-target="navbar-menu" 
          @click="showMobileMenu = !showMobileMenu"
        >
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

          <SearchBar />

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
import SearchBar from "./components/SearchBar.vue";
import { useRouter } from 'vue-router';

export default {
  components: {
    SearchBar
  },
  setup() {
    const showMobileMenu = ref(false);
    const showMovieCategories = ref(false);
    const showOtherCategories = ref(false);
    const categories = ref([])
    const state = reactive({
      lastScrollTop: 0, // last scroll position
      showNavbar: false, // control the display and hiding of the navbar
    });
    const store = useStore();
    const router = useRouter();

    const handleScroll = () => {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (currentScrollTop > state.lastScrollTop) {
        state.showNavbar = true; 
      } else if (currentScrollTop < state.lastScrollTop) {
        state.showNavbar = false; 
      }

      state.lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop; // prevent negative scroll values
    };

    // toggle the menu display state
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

    onBeforeMount(() => {
      store.commit('initializeStore');  

      const token = store.state.accessToken;

      if (!token) {
        router.push('/login');
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
  padding: 1vw; 
}

.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  opacity: 0; 
  visibility: hidden; 
  transition: opacity 0.5s ease, visibility 0.5s ease; 
  z-index: 10000; 
}

.navbar.show {
  opacity: 1; 
  visibility: visible; 
}

.navbar-dropdown {
  overflow-y: auto;  
  max-height: 30vh; 
}

</style>


