<script lang="ts" setup>
import axios from "axios";
import {computed, reactive,ref} from "vue";
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'

const router = useRouter()
const store = useStore()
const route = useRoute()
const QID = route.params.QID
const name = ref("")
const description = ref("")
const scope = ref("")
const type = ref("")


// const createQuestion = () => {
//   if (name.value === "" || description.value === "" || scope.value === "") {
//     alert("Please fill in all the fields.")
//   } else {
//     if (store.state.userStatus === 'teacher') {
//       const query = "http://" + config.apiServer + ":" + config.port + "/api/question/create"
//       axios.post(query, {
//         Qname: name.value,
//         Scope: scope.value,
//         Description: description.value,
//         Type: type.value,
//       }).then((res) => {
//         if (res.data.status === 'success') {
//           router.push('/upload_solution/' + res.data.uuid)
//         } else {
//           alert(res.data.status)
//         }
//       })
//     } else {
//       alert("You do not have the authority to add a new product.")
//     }
//   }
// }
const getQuestionInformation = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            name.value = res.data.question.Qname
            description.value = res.data.question.Description
            scope.value = res.data.question.Scope
        }
    })
}
const choose = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/question_type/update/" + QID
    axios.post(query, {
        Type: type.value,
    }).then((res) => {
        if (res.data.status === 'success') {
            router.push('/customize_solution/' + QID + '/' + type.value)
        } else {
            alert(res.data.status)
        }
    })
}

getQuestionInformation()


</script>

<template>
    <div>
        <ol class="flex items-center w-full text-sm font-medium text-center text-gray-500 dark:text-gray-400 sm:text-base">
        <li class="flex md:w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-gray-200 after:border-1 after:hidden sm:after:inline-block after:mx-6 xl:after:mx-10 dark:after:border-gray-700">
        <span class="flex items-center after:content-['/'] sm:after:hidden after:mx-2 after:text-gray-200 dark:after:text-gray-500">
            <span class="mr-2">1</span>
            Input Question Information
        </span>
        </li>
        <li class="flex md:w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-gray-200 after:border-1 after:hidden sm:after:inline-block after:mx-6 xl:after:mx-10 dark:after:border-gray-700">
        <span class="flex items-center after:content-['/'] sm:after:hidden after:mx-2 after:text-gray-200 dark:after:text-gray-500">
            <span class="mr-2">2</span>
            Choose Question Type
        </span>
        </li>
        <li class="flex md:w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-gray-200 after:border-1 after:hidden sm:after:inline-block after:mx-6 xl:after:mx-10 dark:after:border-gray-700">
        <span class="flex items-center after:content-['/'] sm:after:hidden after:mx-2 after:text-gray-200 dark:after:text-gray-500">
            <span class="mr-2">3</span>
            Upload Solution
        </span>
        </li>
        <li class="flex md:w-full items-center after:content-[''] after:w-full after:h-1 after:border-b after:border-gray-200 after:border-1 after:hidden sm:after:inline-block after:mx-6 xl:after:mx-10 dark:after:border-gray-700">
        <span class="flex items-center after:content-['/'] sm:after:hidden after:mx-2 after:text-gray-200 dark:after:text-gray-500">
            <span class="mr-2">4</span>
            Customize Solution
        </span>
        </li>
        <li class="flex md:w-full items-center text-blue-600 dark:text-blue-500 sm:after:content-[''] after:w-full after:h-1 after:border-b after:border-gray-200 after:border-1 after:hidden sm:after:inline-block after:mx-6 xl:after:mx-10 dark:after:border-gray-700">
        <span class="flex items-center after:content-['/'] sm:after:hidden after:mx-2 after:text-gray-200 dark:after:text-gray-500">
            <svg aria-hidden="true" class="w-4 h-4 mr-2 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
            Choose Question Type (Easier)
        </span>
    </li>
    <li class="flex items-center">
        <span class="mr-2">6</span>
        Customize Solution (Easier)
    </li>
</ol>
    <div class="min-h-full flex items-center justify-center  px-4 sm:px-6 lg:px-8">
      <div class="w-3/6 space-y-4">
        <h2 class="text-left font-medium text-gray-900">
          <div class="text-2xl">Choose Proper Question Type For Easier Version:</div>
        </h2>
        <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4 border-solid border-2 border-gray-300 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-2" type="radio" value="context" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <div>
                    <h5 class="block mt-5 mb-3 ml-5 text-lg font-normal text-gray-900 dark:text-gray-300">Context</h5>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-solid border-2 border-gray-300 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-3" type="radio" value="insert-key-code" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <div>
                    <h5 class="block mt-5 mb-3 ml-5 text-lg font-normal text-gray-900 dark:text-gray-300">Insert Key Code</h5>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-solid border-2 border-gray-300 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-5" type="radio" value="multiple-steps" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <div>
                    <h5 class="block mt-5 mb-3 ml-5 text-lg font-normal text-gray-900 dark:text-gray-300">Multiple Steps</h5>
                </div>  
            </div>
          </div>
        </div>
        <div class="flex items-center justify-between">
        <p class="text-center text-lg text-gray-600">
          <router-link
              class="font-medium text-indigo-600 hover:text-indigo-500"
              :to="'/input_question_type/'+ QID.toString()" 
            >
            Forget the details of every type?
          </router-link>
        </p>
      </div>
        <button
            class="group relative w-full flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="choose"
        >
          Choose Question Type
        </button>
      </div>
    </div>
</div>
  </template>

<style scoped></style>
