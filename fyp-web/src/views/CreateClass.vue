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

const Cname = ref("")

const createClass = () => {
  if (Cname.value === "") {
    alert("Please fill in all the fields.")
  } else {
    if (store.state.userStatus === 'teacher' || store.state.userStatus === 'admin') {
      const query = "http://" + config.apiServer + ":" + config.port + "/api/class"
      axios.post(query, {
        Cname: Cname.value,
        UID: store.state.UID
      }).then((res) => {
        if (res.data.status === 'success') {
          router.push('/personal-center')
        } else {
          alert(res.data.status)
        }
      })  
    } else {
      alert("You do not have the authority to add a new class.")
    }
  }
}
</script>

<template>
  <div class="min-h-full flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-extrabold text-gray-900">
          Create Class
        </h2>
      </div>
 <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Class Name</label
              >
              <input
                  v-model="Cname"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="text"
              />
            </div>
          </div>
        </div>
      <div>
        <button
            class="group relative w-full flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2  focus:ring-blue-300  dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="submit"
            @click="createClass"
        >
          Create
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
