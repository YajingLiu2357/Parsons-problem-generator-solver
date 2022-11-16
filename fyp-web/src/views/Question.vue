<script lang="ts" setup>
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'
import { VueDraggableNext } from 'vue-draggable-next'

const route = useRoute()
const router = useRouter()
const store = useStore()

let pool = {
    code: reactive([]),
    answer: reactive([]),
}
const qid = route.params.QID
const description = ref('')
description.value = ""
const sequence = reactive([])
const bid = ref('')
const getDescription = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + qid
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            description.value = res.data.question.Description
        }
    })
}
const getFragments = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment/" + qid
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[i].BID
                console.log(bid.value)
                pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
            }
            getSequence()
        }
    })
}
const getSequence = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/sequence/" + bid.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            for (let i = 0; i < res.data.sequence.length; i++) {
                sequence.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
            }
        console.log("sequence:" + sequence)
        }
    })
}
const check = () =>{
    let correct = true
    console.log("pool answer:" + pool.answer)
    for (let i = 0; i < sequence.length; i++) {
        console.log(pool.answer[i])
        if (sequence[i] !== pool.answer[i]) {
            correct = false
            break
        }
    }
    if (correct) {
        alert("Correct!")
    } else {
        alert("Wrong!")
    }
}
getDescription()
getFragments()
</script>
<template>
  <div class="container mx-auto sm:px-4 mt-5 mb-5">
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Question: {{ description }}</h6>
            <VueDraggableNext class = "draggable-list" :list="pool.code" group="pool" >
                <div v-for="(fragment, i) in pool.code" :key="i">
                    <div class="bg-white mt-3 p-2 shadow border rounded">
                        <p>{{ fragment }}</p>
                    </div>
                </div>
            </VueDraggableNext>
        </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Answer</h6>
        <VueDraggableNext class = "draggable-list" :list="pool.answer" group = "pool" >
            <div v-for="(fragment, i) in pool.answer" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>{{ fragment }}</p>
                </div>
            </div>
        </VueDraggableNext>
    </div>
    </div>
    <button
            class="float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="check"
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