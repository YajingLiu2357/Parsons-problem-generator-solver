<script lang="ts" setup>
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'
import router from "../router/router"
const store = useStore()
const state = computed(() => store.state)
const questionName = reactive([])
const questionType = reactive([])
const questionID = reactive([])
const score = reactive([])
const count = ref(0)
const getAllScore = async() =>{
    if (state.value.userStatus == "student"){
        const query = "http://" + config.apiServer + ":" + config.port + "/api/record/getAll/student/" + state.value.UID
        axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            count.value = res.data.records.length
           for (let i = 0; i < res.data.records.length; i++) {
               questionID.push(res.data.records[i].QID)
               score.push(res.data.records[i].Score)
               const query1 = "http://" + config.apiServer + ":" + config.port + "/api/question/" + questionID[i]
                axios.get(query1).then((res) => {
                     if (res.data.status === 'success') {
                          questionName.push(res.data.question.Qname)
                          questionType.push(res.data.question.Type)
                     } else {
                          alert(res.data.status)
                     }
                })
           }
        } else {
            alert(res.data.status)
        }
    })
    }else{
        const query = "http://" + config.apiServer + ":" + config.port + "/api/record/getAll/teacher/"
        axios.get(query).then((res) => {
            count.value = res.data.records.length
            console.log(res.data.status)
            for (let i = 0; i < res.data.records.length; i++) {
                questionID.push(res.data.records[i].QID)
                score.push(res.data.records[i].Score)
                const query1 = "http://" + config.apiServer + ":" + config.port + "/api/question/" + questionID[i]
                axios.get(query1).then((res) => {
                    if (res.data.status === 'success') {
                        questionName.push(res.data.question.Qname)
                        questionType.push(res.data.question.Type)
                    } else {
                        alert(res.data.status)
                    }
                })
            }
        })
    }
}
getAllScore()
const tryAgain = (i:number) => {
    router.push('/question/' + questionID[i] + '/' + questionType[i])
}
</script>
<template>
<div class="container mx-auto sm:px-4 mt-5 mb-5" v-show="state.userStatus == 'student'">
    <div class="relative overflow-x-auto">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Question Name
                </th>
                <th scope="col" class="px-6 py-3">
                    Question Type
                </th>
                <th scope="col" class="px-6 py-3">
                    Highest Score
                </th>
                <th scope="col" class="px-6 py-3">
                    Try Again
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="i in count" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {{ questionName[i-1] }}
                </th>
                <td class="px-6 py-4">
                    {{ questionType[i-1] }}
                </td>
                <td class="px-6 py-4">
                    {{ score[i-1] }}
                </td>
                <td class="px-6 py-4">
                    <a @click=" tryAgain(i-1)" class="px-4 py-2 font-medium tracking-wide text-white capitalize transition-colors duration-200 transform bg-blue-500 rounded-md dark:bg-gray-800 hover:bg-blue-600 dark:hover:bg-gray-700 focus:outline-none focus:bg-blue-600 dark:focus:bg-gray-700">
                        Try Again
                    </a>
                </td>
            </tr>
        </tbody>
    </table>
</div>  
</div>
<div class="container mx-auto sm:px-4 mt-5 mb-5" v-show="state.userStatus != 'student'">
    <div class="relative overflow-x-auto">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Question Name
                </th>
                <th scope="col" class="px-6 py-3">
                    Question Type
                </th>
                <th scope="col" class="px-6 py-3">
                    Average Score
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="i in count" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                    {{ questionName[i-1] }}
                </th>
                <td class="px-6 py-4">
                    {{ questionType[i-1] }}
                </td>
                <td class="px-6 py-4">
                    {{ score[i-1] }}
                </td>
            </tr>
        </tbody>
    </table>
</div>  
</div>
</template>