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
const userName = ref("")
const userType = ref("")
const passwordConfirm = ref("")
const classNames = reactive([])
const CID = ref("")

const register = async () => {
    if (email.value === "" || password.value === "" || userName.value === "" || userType.value === "" || passwordConfirm.value === "") {
        alert("Please fill in all the blanks.")
    } else {
        if (password.value !== passwordConfirm.value) {
            alert("Password and password confirmation are not the same.")
        } else {
            const query = "http://" + config.apiServer + ":" + config.port + "/api/user/create"
            axios.post(query, {
                Email: email.value,
                Password: password.value,
                Uname: userName.value,
                UType: userType.value,
                CID: CID.value
            }).then((res) => {
                if (res.data.status === 'success') {
                    alert("Register successfully.")
                    store.commit('setUser', {
                        email: email.value,
                        password: password.value,
                        userName: userName.value,
                        userType: userType.value,
                    })
                    router.push('/')
                } else {
                    alert(res.data.status)
                }
            })
        }
    }
}
const getClassName = async () => {
    const query1 = "http://" + config.apiServer + ":" + config.port + "/api/class/getAll"
    axios.get(query1).then((res) => {
        if (res.data.status === 'success') {
           for (let i = 0; i < res.data.classes.length; i++) {
               classNames.push(res.data.classes[i])
           }
        } else {
            alert(res.data.status)
        }
    })
}
getClassName()
</script>

<template>
  <div class="min-h-full flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          Register New Account
        </h2>
      </div>
 <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >User Name</label
              >
              <input
                  v-model="userName"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="text"
              />
            </div>
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Email</label
              >
              <input
                  v-model="email"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="email"
              />
            </div>
            <div class="mt-4 mb-4">
                <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                >Are you students or teachers?</label>
                <select
                    v-model="userType"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                >
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                </select>
            </div>
            <div class="mt-4 mb-4">
                <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                >Which class do you belong to / supervise?</label>
                <select
                    v-model="CID"
                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                >
                <option v-for="item in classNames" :key="item" :value="item.CID">{{item.Cname}}</option>
                </select>
            </div>
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Password</label
              >
              <input
                  v-model="password"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="password"
              />
            </div>
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Password Confirm</label
              >
              <input
                  v-model="passwordConfirm"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="password"
              />
              </div>
          </div>
        </div>
      <div>
        <button
            class="group relative w-full flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2  focus:ring-blue-300  dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="submit"
            @click="register"
        >
          Register
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
