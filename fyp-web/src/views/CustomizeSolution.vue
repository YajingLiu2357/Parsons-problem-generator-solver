<script lang="ts" setup>
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'

const route = useRoute()
const router = useRouter()
const store = useStore()

const QID = route.params.QID
const QName = ref('')
const description = ref('')
const questionType = ref('')
description.value = ""
const sequence = reactive([])
const bid = ref('')
const solutionType = ref('')
const FID = reactive([])
const addDistractorBoxShow = ref(false)
const codeLength = ref(0)
const distractorLine = ref(0)
const distractorCode = ref('')
const distractorReason = ref('')

const getQuestion = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            QName.value = res.data.question.Qname
            questionType.value = res.data.question.Type
            description.value = res.data.question.Description
        }
    })
}
const getBID = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            bid.value = res.data.fragments[0].BID
            getSequence()
        }
    })
}
const getSequence = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/sequence/" + bid.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            codeLength.value = res.data.sequence.length
            for (let i = 0; i < res.data.sequence.length; i++) {
                FID.push(res.data.FID[i])
                let j = i + 1
                let temp = "Line " + j.toString() + ": " + res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0')
                sequence.push(temp)
            }
        console.log("sequence:" + sequence)
        }
    })
}

const addDistractor = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/distractor/create"
    axios.post(query, {
        Code: distractorCode.value,
        Reason: distractorReason.value,
        FID: FID[distractorLine.value - 1],
    }).then((res) => {
        if (res.data.status === 'success') {
            alert("Add Distractor Success")
            addDistractorBoxShow.value = false
            distractorLine.value = 0
            distractorCode.value = ''
            distractorReason.value = ''
        }
    })
}
getQuestion()
getBID()
</script>
<template>
  <div class="container mx-auto sm:px-4 mt-5 mb-5">
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Solution Type:</label
              >
              <select
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  v-model="solutionType"
                  required
              >
                <option value="fixed order">fixed order</option>
                <option value="not fixed order">not fixed order</option>
                <option value="insert key code">insert key code</option>
              </select>
            </div>
            <div class="mt-2 mb-2">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button> 
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                >
                Add Block 
                </button>
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                >
                Add Difficulty Level 
                </button>
            </div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorLine"
                        required
                    >
                        <option v-for="i in codeLength" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Distractor Code:</label
                    >
                    <textarea
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
                    </textarea>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >The reason to add this distractor (This reason will be shown as feedback when students choose this distractor): </label
                    >
                    <textarea
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorReason"
                        required
                    >
                    </textarea>
                </div>
                <div class="mt-2 mb-2">
                    <button
                        class="ml-3 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="addDistractor"
                    >
                    Add Distractor
                    </button>
                </div>
            </div>
        </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Code</h6>
            <div v-for="(fragment, i) in sequence" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>{{ fragment }}</p>
                </div>
            </div>

    </div>
    </div>
    <button
            class="float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
        >
          Check
        </button> 
  </div>
</template>

<style scoped>
h6 {
    font-weight: 700;
}

.col {
    height: 90vh;
    overflow:auto;
}
.dragable-list {
    min-height: 10vh;
}

.dragable-list > div {
    cursor: pointer;
}
</style>