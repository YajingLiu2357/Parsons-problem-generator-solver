 <script lang="ts" setup>
import axios from "axios";
import {ref} from "vue";
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import {computed, reactive} from "vue"

const router = useRouter()
const store = useStore()
const route = useRoute()
const email = ref("")
const password = ref("")


const login = () => {
  const query1 = "http://" + config.apiServer + ":" + config.port + "/api/login_check/"
  axios
      .post(query1,
          {
            email: email.value,
            password: password.value
          }).then((res) => {
    if (res.data.status === 'success') {
      console.log(res.data.user)
      store.commit('chgUser', {
        UID: res.data.user.UID,
        userEmail: email.value,
        userName: res.data.user.Uname,
      })
      if (res.data.user.Utype === 'admin') {
        store.commit('chgStatus', {userStatus: 'admin'})
      } else if (res.data.user.UType === 'teacher'){
        store.commit('chgStatus', {userStatus: 'teacher'})
      } else {
        store.commit('chgStatus', {userStatus: 'student'})
      }
      router.push('/')
    } else {
      alert(res.data.status)
    }
  })
}


</script>

<template>
  <div class="min-h-full flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          Login Your Account
        </h2>
      </div>
      <input name="remember" type="hidden" value="true"/>
      <div class="rounded-md shadow-sm -space-y-px">
        <div>
          <label class="sr-only" for="email-address">Email address</label>
          <input
              id="email-address"
              v-model="email"
              autocomplete="email"
              class="appearance-none rounded-none relative block w-full px-3 py-4 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              name="email"
              placeholder="Email address"
              required
              type="email"
          />
        </div>
        <div>
          <label class="sr-only" for="password">Password</label>
          <input
              id="password"
              v-model="password"
              autocomplete="current-password"
              class="appearance-none rounded-none relative block w-full px-3 py-4 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              name="password"
              placeholder="Password"
              required
              type="password"
          />
        </div>
      </div>

      <div class="flex items-center justify-between">
        <p class="text-center text-sm text-gray-600">
          <router-link
              class="font-medium text-indigo-600 hover:text-indigo-500"
              to="/register"
            >
            Not have an account?
          </router-link>
        </p>
      </div>

      <div>
        <button
            class="group relative w-full flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2  focus:ring-blue-300  dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="submit"
            @click="login"
        >
          Login
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
