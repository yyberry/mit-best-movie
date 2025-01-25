<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log in</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark">Log in</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/sign-up">click here</router-link> to sign up!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  name: 'LogIn',
  setup() {
    // 定义响应式变量
    const username = ref('');
    const password = ref('');
    const errors = ref([]);
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    // 表单提交逻辑
    const submitForm = async () => {
        // 清除错误信息
        errors.value = [];
        axios.defaults.headers.common['Authorization'] = '';
        localStorage.removeItem('token');

        const formData = {
            username: username.value,
            password: password.value,
        };

        try {
            const response = await axios.post('/api/v1/token/login/', formData, {
            headers: {
                'Content-Type': 'application/json'
            }
            });

            console.log(response.data);  // 输出响应数据
            const token = response.data.auth_token;

            // 存储用户名
            localStorage.setItem('username', username.value);  // 或者 Cookies.set('username', username.value)

            // 更新 Vuex Store
            store.commit('setToken', token);

            // 设置 Axios 请求头
            axios.defaults.headers.common['Authorization'] = 'Token ' + token;

            // 保存 Token 到本地存储
            localStorage.setItem('token', token);

            // 跳转到指定页面
            const toPath = route.query.to || '/my-account';
            router.push(toPath);

            } catch (error) {
                console.log(error);  // 输出完整的错误信息
                if (error.response) {
                    // 输出来自后端的错误信息
                    for (const property in error.response.data) {
                        errors.value.push(`${property}: ${error.response.data[property]}`);
                    }
                } else {
                errors.value.push('Something went wrong. Please try again');
                }
            }
    };


    // 返回响应式数据和方法
    return {
      username,
      password,
      errors,
      submitForm,
    };
  },
};
</script>

<style scoped>
.page-log-in {
  margin-top: 50px;
}

</style>