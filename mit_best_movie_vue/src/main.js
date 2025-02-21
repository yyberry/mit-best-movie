import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'bulma/css/bulma.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000/'

// 添加请求拦截器，检查是否有 access_token
axios.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

axios.interceptors.response.use(
    response => response, // 如果响应正常，直接返回
    async (error) => {
      const originalRequest = error.config;
      
      // 如果是 Token 过期的错误 (401)
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
  
        try {
          const refreshToken = localStorage.getItem('refreshToken');
          const response = await axios.post('api/v1/token/refresh/', { refresh: refreshToken });
  
          const newAccessToken = response.data.access;
          localStorage.setItem('accessToken', newAccessToken); // 更新新的 access_token
  
          // 重新发送原始请求
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
          return axios(originalRequest);
        } catch (refreshError) {
          console.error('Token refresh failed:', refreshError);
          // 可以在这里处理过期后的清理操作，如登出用户
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          // 或者重定向到登录页
        }
      }
      
      return Promise.reject(error);
    }
);

createApp(App).use(store).use(router, axios).mount('#app')