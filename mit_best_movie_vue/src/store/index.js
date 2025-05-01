import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    user: null,
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('refreshToken') && localStorage.getItem('accessToken')) {
        state.accessToken = localStorage.getItem('accessToken')
        state.refreshToken = localStorage.getItem('refreshToken')
        state.user = localStorage.getItem('username')
        state.isAuthenticated = true
      } else {
        state.accessToken = ''
        state.refreshToken = ''
        state.user = null
        state.isAuthenticated = false
      } 
    },
    setAccessToken(state, access) {
      state.accessToken = access;
      state.isAuthenticated = true;
    },
    setRefreshToken(state, refresh) {
      state.refreshToken = refresh;
    },
    setUser(state, username) {
      state.user = username;
    },
    removeToken(state) {
      state.accessToken = null
      state.refreshToken = null
      state.user = null
      state.isAuthenticated = false
    },
  },
  actions: {
  },
  modules: {
  }
})
