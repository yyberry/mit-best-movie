import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import CategoryView from '../views/CategoryView.vue'
import MovieView from '../views/MovieView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogInView from '../views/LogInView.vue'
import MyAccountView from '../views/MyAccountView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Mit Best Movie', 
    },
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/category/:category_slug',
    name: 'category',
    component: CategoryView
  },
  {
    path:'/movie/:movie_slug',
    name: 'movie',
    component: MovieView
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUpView,
    meta: {
      title: 'Signup | Mit Best Movie',
    },
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogInView,
    meta: {
      title: 'Login | Mit Best Movie',
    },
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccountView,
    meta: {
      requireLogin: true,
      title: 'My account | Mit Best Movie',
      isMyAccountPage: true,
  }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Mit Best Movie'; // 默认标题
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
