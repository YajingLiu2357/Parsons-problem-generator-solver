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
const name = ref("")
const description = ref("")
const scope = ref("")
const type = ref("")

const editQuestion = () => {
  if (name.value === "" || description.value === "" || scope.value === "") {
    alert("Please fill in all the fields.")
  } else {
    if (store.state.userStatus === 'teacher' || store.state.userStatus === 'admin') {
      const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + route.params.QID
      axios.patch(query, {
        Qname: name.value,
        Scope: scope.value,
        Description: description.value,
      }).then((res) => {
        if (res.data.status === 'success') {
          router.push('/question/' + route.params.QID + '/' + type.value)
          // router.push('/upload_solution/' + res.data.uuid)
        } else {
          alert(res.data.status)
        }
      })  
    } else {
      alert("You do not have the authority to add a new question.")
    }
  }
}
const getQuestion = async () => {
  if (store.state.userStatus === 'teacher' || store.state.userStatus === 'admin') {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + route.params.QID
    axios.get(query).then((res) => {
      if (res.data.status === 'success') {
        name.value = res.data.question.Qname
        scope.value = res.data.question.Scope
        description.value = res.data.question.Description
        type.value = res.data.question.Type
      } else {
        alert(res.data.status)
      }
    })
  } else {
    alert("You do not have the authority to edit this question.")
  }
}
getQuestion()
</script>

<template>
    <div class="min-h-full flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-4">
        <h2 class="text-left font-medium text-gray-900">
          <div class="text-2xl">Edit Question</div>
        </h2>
        <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Name</label
              >
              <!-- <p class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
              {{ name }}  
                </p> -->
              <input
                  v-model="name"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="text"
              />
            </div>
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Scope</label
              >
              <input
                  v-model="scope"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="text"
              />
            </div>
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Description</label
              >
              <textarea
                  v-model="description"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="text"
              />
            </div>
          </div>
        </div>
        <button @click="editQuestion" type="button" class="text-lg group relative w-full flex justify-center py-3 px-6 border border-transparent font-large rounded-md shadow-sm text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300  text-center items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
          Edit
        </button>
      </div>
    </div>
  </template>

<style scoped></style>
