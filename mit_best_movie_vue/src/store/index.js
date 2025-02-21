import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('refreshToken') && localStorage.getItem('accessToken')) {
        state.accessToken = localStorage.getItem('accessToken')
        state.refreshToken = localStorage.getItem('refreshToken')
        state.isAuthenticated = true
      } else {
        state.accessToken = ''
        state.refreshToken = ''
        state.isAuthenticated = false
      } 
    },
    setAccessToken(state, access) {
      state.accessToken = access;
    },
    setRefreshToken(state, refresh) {
      state.refreshToken = refresh;
    },
    removeToken(state) {
      state.accessToken = null
      state.refreshToken = null
      state.isAuthenticated = false
    },
  },
  actions: {
  },
  modules: {
  }
})
