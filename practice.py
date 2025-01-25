# <template>
#   <div>
#     <div id="banner">
#       <div class="carousel">
#         <div
#           v-for="(movie, index) in movies"
#           :key="index"
#           class="carousel-item"
#           :style="getItemStyle(index)"
#         >
#           <img :src="getImage(movie.poster)" :alt="movie.title" />
#           <div class="image-info">
#             <p class="title">{{ movie.title }}</p>
#             <p class="rating">{{ movie.rating }}</p>
#           </div>
#         </div>
#       </div>
#     </div>

#     <div class="navigation-buttons">
#       <button @click="handleClick('prev')" class="nav-button left">
#         ←
#       </button>
#       <button @click="handleClick('next')" class="nav-button right">
#         →
#       </button>
#     </div>
#   </div>
# </template>

# <script>
# import axios from "axios";

# export default {
#   data() {
#     return {
#       movies: [], // 电影数据
#       currentIndex: 0, // 当前居中的索引
#     };
#   },
#   created() {
#     // 获取电影数据
#     axios.get("/api/v1/new-movies/").then((response) => {
#       this.movies = response.data;
#     });
#   },
#   methods: {
#     getImage(_url) {
#       if (_url) {
#         const _u = _url.replace(/^https?:\/\//, "");
#         return `https://images.weserv.nl/?url=${_u}`;
#       }
#     },
#     handleClick(direction) {
#       if (direction === "next") {
#         this.currentIndex = (this.currentIndex + 1) % this.movies.length;
#       } else if (direction === "prev") {
#         this.currentIndex =
#           (this.currentIndex - 1 + this.movies.length) % this.movies.length;
#       }
#     },
#     getItemStyle(index) {
#       const total = this.movies.length;
#       const offset = (index - this.currentIndex + total) % total;

#       // 确定图片的水平位置、缩放比例和堆叠层级
#       let translateX = 0;
#       let zIndex = 0;
#       let scale = 1;

#       if (offset === 0) {
#         // 当前图片：中心图片最大，层级最高
#         translateX = 0;
#         zIndex = 10;
#         scale = 1;
#       } else if (offset <= Math.floor(total / 2)) {
#         // 中心右侧图片：越靠近中心越大
#         translateX = offset * 150; // 每张图片的水平间距
#         zIndex = 10 - offset; // 层级递减
#         scale = 1 - offset * 0.1; // 缩放比例递减
#       } else {
#         // 中心左侧图片：越靠近中心越大（偏移到负方向）
#         translateX = (offset - total) * 150; // 反向偏移
#         zIndex = 10 - (total - offset); // 层级递减
#         scale = 1 - (total - offset) * 0.1; // 缩放比例递减
#       }

#       return {
#         transform: `translateX(${translateX}px) scale(${scale})`,
#         zIndex: zIndex,
#         transition: "transform 0.5s ease, z-index 0.5s ease",
#       };
#     },
#   },
# };
# </script>

# <style scoped>
# #banner {
#   display: flex;
#   justify-content: center;
#   align-items: center;
#   perspective: 1000px;
#   height: 70vh;
#   position: relative;
# }

# .carousel {
#   display: flex;
#   justify-content: center;
#   align-items: center;
#   position: relative;
#   width: 100%; /* 横向铺满屏幕 */
#   height: 100%;
# }

# .carousel-item {
#   position: absolute;
#   width: 18rem;
#   height: 24rem;
#   backface-visibility: hidden;
#   transition: transform 0.5s ease, z-index 0.5s ease;
# }

# .carousel-item img {
#   width: 100%;
#   height: 100%;
#   object-fit: cover;
#   border-radius: 8px;
#   box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
# }

# .image-info {
#   position: absolute;
#   bottom: 5%;
#   left: 50%;
#   transform: translateX(-50%);
#   font-size: 1rem;
#   color: white;
#   text-shadow: 0 0 5px rgba(0, 0, 0, 0.7);
# }

# .navigation-buttons {
#   position: absolute;
#   bottom: 5%;
#   width: 100%;
#   display: flex;
#   justify-content: center; /* 居中对齐 */
#   gap: 1rem; /* 设置按钮之间的间距 */
# }

# .nav-button {
#   background: white;
#   border: none;
#   cursor: pointer;
#   border-radius: 50%;
#   padding: 1rem;
#   display: flex;
#   justify-content: center;
#   align-items: center;
#   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
# }
# </style>

# const submitForm = async () => {
#       // 清除错误信息
#       errors.value = [];
#       axios.defaults.headers.common['Authorization'] = '';
#       localStorage.removeItem('token');

#       const formData = {
#         username: username.value,
#         password: password.value,
#       };

#       try {
#         const response = await axios.post('/api/v1/token/login/', formData);
#         const token = response.data.auth_token;

#         // 更新 Vuex Store
#         store.commit('setToken', token);

#         // 设置 Axios 请求头
#         axios.defaults.headers.common['Authorization'] = 'Token ' + token;

#         // 保存 Token 到本地存储
#         localStorage.setItem('token', token);
#         localStorage.setItem('username', usernameFromResponse);

#         // 跳转到指定页面
#         const toPath = route.query.to || '/my-account';
#         router.push(toPath);
#       } catch (error) {
#         if (error.response) {
#           for (const property in error.response.data) {
#             errors.value.push(`${property}: ${error.response.data[property]}`);
#           }
#         } else {
#           errors.value.push('Something went wrong. Please try again');
#           console.error(error);
#         }
#       }
#     };