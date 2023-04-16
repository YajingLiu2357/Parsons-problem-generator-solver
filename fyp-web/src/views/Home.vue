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
const filteredQuestions = ref([]);
const type = ref("");
const store = useStore();
const router = useRouter();
const route = useRoute();
const filterAllFlag = ref(true);
const filterPythonBasisFlag = ref(false);
const filterDataStructuresFlag = ref(false);
const filterAlgorithmsFlag = ref(false);
const filterRecursionFlag = ref(false);
const filterOtherFlag = ref(false);
const white = ref("#FFFFFF");
const grey = ref("#D2D2DF");

const state = computed(() => store.state)

const getAllQuestion = async () =>{
  const query = "http://" + config.apiServer + ":" + config.port + "/api/question/getAll"
  axios.get(query).then((res) => {
    if (res.data.status == 'success') {
      questions.value = res.data.questions
      filteredQuestions.value = questions.value
      // for (let i = 0; i < questions.value.length; i++) {
      //   const query = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/check/" + questions.value[i].QID
      //   axios.get(query).then((res) => {
      //   if (res.data.status === 'success') {
      //       questions.value.splice(i, 1)
      //   }
      // })
      // }
    } else {
      alert(res.data.status)
    }
  })
}
getAllQuestion()
const filterAll = () => {
  filterAllFlag.value = true;
  filterPythonBasisFlag.value = false;
  filterDataStructuresFlag.value = false;
  filterAlgorithmsFlag.value = false;
  filterRecursionFlag.value = false;
  filterOtherFlag.value = false;
  filteredQuestions.value = questions.value
}
const filterPythonBasis = () => {
  filterAllFlag.value = false;
  filterPythonBasisFlag.value = true;
  filterDataStructuresFlag.value = false;
  filterAlgorithmsFlag.value = false;
  filterRecursionFlag.value = false;
  filterOtherFlag.value = false;
  filteredQuestions.value = questions.value.filter((question) => question.Scope === "python-basis")
  if (filteredQuestions.value.length === 0) {
    alert("No questions in this category yet.")
  }
}
const filterDataStructures = () => {
  filterAllFlag.value = false;
  filterPythonBasisFlag.value = false;
  filterDataStructuresFlag.value = true;
  filterAlgorithmsFlag.value = false;
  filterRecursionFlag.value = false;
  filterOtherFlag.value = false;
  filteredQuestions.value = questions.value.filter((question) => question.Scope === "data-structures")
  if (filteredQuestions.value.length === 0) {
    alert("No questions in this category yet.")
  }
}
const filterAlgorithms = () => {
  filterAllFlag.value = false;
  filterPythonBasisFlag.value = false;
  filterDataStructuresFlag.value = false;
  filterAlgorithmsFlag.value = true;
  filterRecursionFlag.value = false;
  filterOtherFlag.value = false;
  filteredQuestions.value = questions.value.filter((question) => question.Scope === "algorithms")
  if (filteredQuestions.value.length === 0) {
    alert("No questions in this category yet.")
  }
}
const filterRecursion = () => {
  filterAllFlag.value = false;
  filterPythonBasisFlag.value = false;
  filterDataStructuresFlag.value = false;
  filterAlgorithmsFlag.value = false;
  filterRecursionFlag.value = true;
  filterOtherFlag.value = false;
  filteredQuestions.value = questions.value.filter((question) => question.Scope === "recursion")
  if (filteredQuestions.value.length === 0) {
    alert("No questions in this category yet.")
  }
}
const filterOther = () => {
  filterAllFlag.value = false;
  filterPythonBasisFlag.value = false;
  filterDataStructuresFlag.value = false;
  filterAlgorithmsFlag.value = false;
  filterRecursionFlag.value = false;
  filterOtherFlag.value = true;
  filteredQuestions.value = questions.value.filter((question) => question.Scope === "other")
  if (filteredQuestions.value.length === 0) {
    alert("No questions in this category yet.")
  }
}
</script>

<template>
  <!-- <div class="container text-center">
    <Quickguide :msg="hello" />
  </div> -->
  <div class ="px-8 py-8 bg-gray-100">
    <div class="flex justify-between container mx-auto">
      <div class="w-full lg:w-8/12">
        <div class = "mt-6" v-for="question in filteredQuestions" :key="question.QID">
           <div class="w-full p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">{{question.Qname}}</h5>
          <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">{{question.Description}}</p>
          <router-link :to="'/question/' + question.QID + '/' + question.Type" v-show="store.state.userStatus != 'visitor'" class="inline-flex items-right px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
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
              <li v-bind:style="[filterAllFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
                <button @click="filterAll()">- All</button>
              </li>
              <li class="mt-2" v-bind:style="[filterPythonBasisFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
                <button @click="filterPythonBasis()" >- Python Basis</button>
              </li>
              <li class="mt-2" v-bind:style ="[filterDataStructuresFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
                <button @click="filterDataStructures()" value="DataStructures">- Data Structures</button>
              </li>
              <li class="mt-2" v-bind:style ="[filterAlgorithmsFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
              <button @click="filterAlgorithms()" value="Algorithms">- Algorithms</button>
              </li>
              <li class="mt-2" v-bind:style ="[filterRecursionFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
                <button @click="filterRecursion()" value="Recursion">- Recursion</button>
              </li>
              <li class="mt-2" v-bind:style ="[filterOtherFlag == true? {backgroundColor: grey} : {backgroundColor: white}]">
                <button @click="filterOther()" value="Other">- Other</button>
              </li>
            </ul>
          </div>
        </div>
    </div>
  </div>
</template>
