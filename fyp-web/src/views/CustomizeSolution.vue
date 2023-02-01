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
            for (let i = 0; i < res.data.sequence.length; i++) {
                let j = i + 1
                let temp = "Line " + j.toString() + ": " + res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0')
                sequence.push(temp)
            }
        console.log("sequence:" + sequence)
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