<script lang="ts" setup>
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'
import { VueDraggableNext } from 'vue-draggable-next'
import { nestedDraggable } from 'vue-draggable-next'
// import {BaseTree, Draggable, ExternalDataHandler, pro} from '@he-tree/vue'
// import '@he-tree/vue/style/default.css'

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
const sequence = reactive([])
const bid = ref('')

// const treeData = reactive([
//     {
//         text: 'Projects',
//         children: [
//             {
//                 text: 'Frontend',
//                 children: [
//                     {
//                         text: 'Vue',
//                         children: [
//                             {},
//                         ],
//                     },
//                 ],
//             },
//         ],
//     },
// ])
// const list = reactive([
//     {
//         name: "task 1",
//         tasks: [
//             {
//                 name: "task 2",
//                 tasks: []
//             }
//         ]
//     }, 
//     {
//         name: "task 3",
//         tasks: [
//             {
//                 name: "task 4",
//                 tasks: []
//             }
//         ]
//     }
// ])

// getName()

const getDescription = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
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
                console.log(bid.value)
                pool.code.push(res.data.fragments[i].Code.replace(/\n/g, ''))
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
const decreaseIndent = (i: number) =>{
    pool.answer[i] = pool.answer[i].replace('\u00a0\u00a0\u00a0\u00a0', '')
    
}
const increaseIndent = (i: number) =>{
    pool.answer[i] = '\u00a0\u00a0\u00a0\u00a0' + pool.answer[i]
    
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
        <!-- <nested-draggable class = "draggable-list" :list="pool.answer" group = "pool">
            <div v-for="(fragment, i) in pool.answer" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>{{ fragment }}</p>
                </div>
            </div>
        </nested-draggable> -->
        <!--<Draggable v-model="treeData"></Draggable>-->
        <!-- <nested-draggalbe :tasks="list"></nested-draggalbe>
        <rawDisplayer class="col-3" :value="list" title="List"></rawDisplayer> -->

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