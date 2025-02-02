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
    const username = ref('');
    const password = ref('');
    const errors = ref([]);
    const router = useRouter();
    const route = useRoute();
    const store = useStore();

    const submitForm = async () => {
        // clear the error messages
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

            console.log(response.data);  
            const token = response.data.auth_token;

            // store user name
            localStorage.setItem('username', username.value);  

            // update Vuex Store
            store.commit('setToken', token);

            // set Axios headers
            axios.defaults.headers.common['Authorization'] = 'Token ' + token;

            // store Token 
            localStorage.setItem('token', token);

            // navigate to the specified page
            const toPath = route.query.to || '/my-account';
            router.push(toPath);

            } catch (error) {
                console.log(error);  
                if (error.response) {
                    for (const property in error.response.data) {
                        errors.value.push(`${property}: ${error.response.data[property]}`);
                    }
                } else {
                errors.value.push('Something went wrong. Please try again');
                }
            }
    };

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