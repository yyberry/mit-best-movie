<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign up</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control is-flex">
                            <input
                                :type="showPassword ? 'text' : 'password'"
                                class="input"
                                v-model="password"
                            >
                            <button
                                type="button"
                                class="button is-light ml-2"
                                @click="togglePasswordVisibility"
                                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                            >
                                <span v-if="showPassword">🙈</span>
                                <span v-else>👁️</span>
                            </button>
                        </div>
                    </div>

                    <div class="field">
                        <label>Repeat password</label>
                        <div class="control is-flex">
                            <input
                                :type="showPassword ? 'text' : 'password'"
                                class="input"
                                v-model="password2"
                            >
                            <button
                                type="button"
                                class="button is-light ml-2"
                                @click="togglePasswordVisibility"
                                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                            >
                                <span v-if="showPassword">🙈</span>
                                <span v-else>👁️</span>
                            </button>
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-dark" type=“submit”>Sign up</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/log-in">click here</router-link> to log in!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, reactive } from 'vue';
import axios from 'axios';
import { toast } from 'bulma-toast';
import { useRouter } from 'vue-router';

export default {
  name: 'SignUp',
  setup() {
    const username = ref('');
    const password = ref('');
    const password2 = ref('');
    const showPassword = ref(false); // 控制密码显示
    const errors = ref([]);
    const router = useRouter();

    // 切换密码显示状态
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value;
    };

    // 提交表单逻辑
    const submitForm = () => {
      errors.value = []; // 重置错误信息

      if (username.value === '') {
        errors.value.push('The username is missing');
      }

      if (password.value === '') {
        errors.value.push('The password is too short');
      }

      if (password.value !== password2.value) {
        errors.value.push("The passwords don't match");
      }

      if (!errors.value.length) {
        const formData = {
          username: username.value,
          password: password.value,
        };

        axios
          .post('/api/v1/users/', formData)
          .then(() => {
            toast({
              message: 'Account created, please log in!',
              type: 'is-success',
              dismissible: true,
              pauseOnHover: true,
              duration: 2000,
              position: 'bottom-right',
            });
            router.push('/log-in'); // 跳转到登录页面
          })
          .catch((error) => {
            if (error.response) {
              for (const property in error.response.data) {
                errors.value.push(`${property}: ${error.response.data[property]}`);
              }
              console.log(JSON.stringify(error.response.data));
            } else if (error.message) {
              errors.value.push('Something went wrong. Please try again');
              console.log(JSON.stringify(error));
            }
          });
      }
    };

    return {
      username,
      password,
      password2,
      showPassword,
      errors,
      togglePasswordVisibility,
      submitForm,
    };
  },
};
</script>

<style scoped>
.page-sign-up {
  margin-top: 50px;
}

.is-flex {
  display: flex;
  align-items: center;
}
</style>
