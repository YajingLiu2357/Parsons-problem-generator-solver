<script setup lang="ts">
// import Quickguide from "../components/Quickguide.vue";
// import { reactive, ref, watch } from 'vue'
// import { computed } from "vue";
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'

const questions = ref([]);
const store = useStore();
const router = useRouter();
const route = useRoute();

const state = computed(() => store.state)

const getAllQuestion = async () =>{
  const query = "http://" + config.apiServer + ":" + config.port + "/api/question/getAll"
  axios.get(query).then((res) => {
    if (res.data.status == 'success') {
      questions.value = res.data.questions
    } else {
      alert(res.data.status)
    }
  })
}
getAllQuestion()
</script>

<template>
  <!-- <div class="container text-center">
    <Quickguide :msg="hello" />
  </div> -->
  <div class ="px-8 py-8 bg-gray-100">
    <div class="flex justify-between container mx-auto">
      <div class="w-full lg:w-8/12">
        <div class = "mt-6" v-for="question in questions" :key="question.QID">
           <div class="w-full p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{question.Qname}}</h5>
          <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{question.Description}}</p>
          <router-link :to="'/question/' + question.QID + '/' + question.Type" class="inline-flex items-right px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
            Read more
          <svg aria-hidden="true" class="w-4 h-4 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
          </router-link>
        </div>
        </div>
        </div>
        <div class="-mx-8 w-4/12 lg:block">
          <h1 class="mb-4 text-xl font-bold text-gray-700">Scope</h1>
          <div class="flex flex-col bg-white px-4 py-6 max-w-sm mx-auto rounded-lg shadow-md">
            <ul class="">
              <li>
                - Data Structures
              </li>
              <li class="mt-2">
                - Algorithms
              </li>
            </ul>
          </div>
        </div>
    </div>
  </div>
</template>
