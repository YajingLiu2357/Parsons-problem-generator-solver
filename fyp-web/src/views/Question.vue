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

const QID = route.params.QID
const description = ref('')
description.value = ""
const name = ref('')
name.value = ""
const sequence = reactive([])
const bid = ref('')
const indent = reactive([])
const indentAnswer = reactive([])
const checked = ref(false)
const color = reactive([])
const distractorCode = reactive([])
const distractorReason = reactive([])
const white = 'white'

const getQuestionInformation = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            name.value = res.data.question.Qname
            description.value = res.data.question.Description
        }
    })
}
const getFragments = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[i].BID
                // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
                pool.code.push(res.data.fragments[i].Code.replace(/\n/g, ''))
                indent.push(0)
                color.push('white')
                const query = "http://" + config.apiServer + ":" + config.port + "/api/distractor/" + res.data.fragments[i].FID
                axios.get(query).then((res) => {
                    if (res.data.status === 'success') {
                        for (let j = 0; j < res.data.distractors.length; j++) {
                            pool.code.push(res.data.distractors[j].Code.replace(/\n/g, ''))
                            distractorCode.push(res.data.distractors[j].Code.replace(/\n/g, ''))
                            distractorReason.push(res.data.distractors[j].Reason)
                        }
                    }
                })
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
                // sequence.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
                sequence.push(res.data.sequence[i].replace(/\n/g, ''))
                let temp = 0
                for (let j = 0; j < res.data.sequence[i].length; j=j+4){
                    if (res.data.sequence[i][j] === ' ' && res.data.sequence[i][j+1] === ' ' && res.data.sequence[i][j+2] === ' ' && res.data.sequence[i][j+3] === ' '){
                        temp = temp + 1
                    }
                    else{
                        break
                    }
                }
                indentAnswer.push(temp)   
            }
        }
    })
}
const check = () =>{
    checked.value = true
    for (let i = 0; i < sequence.length; i++) {
        if (pool.answer.length <= i){
            let difference = sequence.length - pool.answer.length
            alert("Need to add " + difference + " more lines")
            return
        }
        let tempSeq = sequence[i]
        let tempAnswer = pool.answer[i]
        tempSeq = tempSeq.toString().trim()
        tempAnswer = tempAnswer.toString().trim()
        if (tempSeq !== tempAnswer) {
            color[i] = '#ff6251'
            for(let j = 0; j < distractorCode.length; j++){
                let tempDistractor = distractorCode[j].toString().trim()
                if (tempDistractor === tempAnswer){
                    alert("Reason: " + distractorReason[j])
                }
            }
        }else if (indent[i] !== indentAnswer[i]){
            color[i] = "#ffd877"
        }
        else{
            color[i] = "#b1dd8c"
        }
    }
}
const decreaseIndent = (i: number) =>{
    pool.answer[i] = pool.answer[i].replace('\u00a0\u00a0\u00a0\u00a0', '')
    indent[i] = indent[i] - 1
    
}
const increaseIndent = (i: number) =>{
    pool.answer[i] = '\u00a0\u00a0\u00a0\u00a0' + pool.answer[i]
    indent[i] = indent[i] + 1
    
}
getQuestionInformation()
getFragments()
</script>
<template>
  <div class="container mx-auto sm:px-4 mt-5 mb-5">
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Question: {{ name }}</h6>
        <p>{{ description }}</p>
            <VueDraggableNext class = "draggable-list" :list="pool.code" group="pool" >
                <div v-for="(fragment, i) in pool.code" :key="i">
                    <div class="bg-white mt-3 p-2 shadow border rounded">
                        <p>{{ fragment }}</p>
                    </div>
                </div>
            </VueDraggableNext>
            <p class="font-bold mt-3">Note: <br>
                <span class="text-red-500">Red:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Wrong Code;</span><br>
                <span class="text-yellow-400">Yellow: &nbsp;Wrong Indent;</span> <br>
                <span class="text-green-500">Green: &nbsp;&nbsp;Correct</span>
            </p>
        </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Answer</h6>
        <VueDraggableNext class = "draggable-list" :list="pool.answer" group = "pool" >
            <div v-for="(fragment, i) in pool.answer" :key="i">
                <div v-bind:style="[checked == true? {backgroundColor: color[i]} : {backgroundColor: white}]" class="bg-white mt-3 p-2 shadow border rounded">                        
                    <p>
                        <button @click="decreaseIndent(i)" title="Decrease Indent" type="button" class="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <svg class="w-4 h-4 rotate-180" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            <span class="sr-only">Decrease Indent</span>
                        </button>
                        <button @click="increaseIndent(i)" title="Increase Indent" type="button" class="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            <span class="sr-only">Increase Indent</span>
                        </button>
                        {{ fragment }}
                    </p>
                </div>
            </div>
        </VueDraggableNext>
    </div>
    </div>
    <button
            class="mt-4 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
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