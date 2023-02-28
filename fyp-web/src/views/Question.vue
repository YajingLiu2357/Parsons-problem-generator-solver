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
    buffer: reactive([]),
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
const black = 'black'
const grey = '#778899'
const questionType = route.params.Type
const blocks = reactive([])
// For multiple solutions
const bid2 = ref('')
const sequence2 = reactive([])
const indent2 = reactive([])
const indentAnswer2 = reactive([])
const color2 = reactive([])
const solutionName = ref('')
const solutionName2 = ref('')
const distractorCode2 = reactive([])
const distractorReason2 = reactive([])
const isPlaceholder = reactive([])
// const numberIconList = ['\u{278A}', '\u{278B}', '\u{278C}', '\u{278D}', '\u{278E}', '\u{278F}', '\u{2790}', '\u{2791}', '\u{2792}', '\u{2793}']
const scoreShow = ref('')
const scoreShow2 = ref('')
const totalScore = ref('')
const contextNum = ref(0)

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
            if (questionType === 'traditional'){
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
            }else if (questionType === 'context'){
                for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[i].BID
                // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
                if (res.data.fragments[i].Type === 'not context'){
                    let icon = '\u{00A0}\u{00A0}\u{00A0}\u{00A0}\u{00A0}'
                    icon = icon + res.data.fragments[i].Code.replace(/\n/g, '')
                    pool.code.push(icon)
                    // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, ''))   
                }
                // indent.push(0)
                // color.push('white')
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
            }else if (questionType === 'insert-key-code'){
                for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[i].BID
                // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
                if (res.data.fragments[i].Type === 'key code'){
                    pool.code.push(res.data.fragments[i].Code.replace(/\n/g, ''))   
                }
                // indent.push(0)
                // color.push('white')
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
            }else if (questionType === "multiple-steps"){
                for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[i].BID
                // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
                let temp = "\u{3010}Step"
                // let icon = ""
                let fragmentInBlock = []
                for (let j = 0; j < blocks.length; j++){
                    fragmentInBlock=blocks[j].split(";")
                    fragmentInBlock.pop()
                    for (let k = 0; k < fragmentInBlock.length; k++){
                        if (fragmentInBlock[k] === res.data.fragments[i].FID){
                            temp = temp + " " + (j+1) + "\u{3011} "
                            // icon = numberIconList[j]
                        }
                    }
                    fragmentInBlock = []
                }
                temp = temp + res.data.fragments[i].Code.replace(/\n/g, '')
                pool.code.push(temp)
                // icon = icon + res.data.fragments[i].Code.replace(/\n/g, '')
                // pool.code.push(icon)
                // indent.push(0)
                // color.push('white')
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
        }else if (questionType === 'compare-algorithm'){
            for (let i = 0; i < res.data.fragments.length; i++) {
                bid.value = res.data.fragments[0].BID
                getSolutionName()
                if(res.data.fragments[i].BID != bid.value){
                   bid2.value = res.data.fragments[i].BID
                     getSolutionName2()
               }
                // pool.code.push(res.data.fragments[i].Code.replace(/\n/g, '').replace(/ /g, '\u00a0'))
                pool.code.push(res.data.fragments[i].Code.replace(/\n/g, ''))
                // indent.push(0)
                // color.push('white')
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
            getSequence2()
         }
        getSequence()
    }})
}
const getSolutionName = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/solution_name/" + bid.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            solutionName.value = res.data.Sname
            console.log(solutionName.value)
        }
    })
}
const getSolutionName2 = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/solution_name/" + bid2.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            solutionName2.value = res.data.Sname
        }
    })
}
const getSequence = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/sequence/" + bid.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            for (let i = 0; i < res.data.sequence.length; i++) {
                sequence.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
                // sequence.push(res.data.sequence[i].replace(/\n/g, ''))
                let temp = 0
                for (let j = 0; j < res.data.sequence[i].length; j=j+4){
                    if (res.data.sequence[i][j] === ' ' && res.data.sequence[i][j+1] === ' ' && res.data.sequence[i][j+2] === ' ' && res.data.sequence[i][j+3] === ' '){
                        temp = temp + 1
                    }
                    else{
                        break
                    }
                }
                indent.push(0)
                color.push('white')
                indentAnswer.push(temp)
                if(questionType=== 'context'){
                    if (res.data.FragmentType[i] === 'context'){
                        let icon = '\u{1F4CD}'
                        icon = icon + res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0')
                        pool.answer.push(icon)
                        // pool.answer.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
                        indent[i] = temp
                        isPlaceholder[i] = false
                        contextNum.value = contextNum.value + 1
                    }else{
                        let number = i + 1
                        let text = 'Placeholder'+' Line' + number + ': drag it to the left code pool before checking.'
                        pool.answer.push(text)
                        isPlaceholder[i] = true
                    }
                }else if (questionType === 'insert-key-code'){
                    if (res.data.FragmentType[i] === 'not key code'){
                        pool.answer.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
                        indent[i] = temp
                        contextNum.value = contextNum.value + 1
                    }
                } 
            }    
        }
    })
}
const getSequence2 = async () =>{
    const query = "http://" + config.apiServer + ":" + config.port + "/api/sequence/" + bid2.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            for (let i = 0; i < res.data.sequence.length; i++) {
                sequence2.push(res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0'))
                // sequence.push(res.data.sequence[i].replace(/\n/g, ''))
                let temp = 0
                for (let j = 0; j < res.data.sequence[i].length; j=j+4){
                    if (res.data.sequence[i][j] === ' ' && res.data.sequence[i][j+1] === ' ' && res.data.sequence[i][j+2] === ' ' && res.data.sequence[i][j+3] === ' '){
                        temp = temp + 1
                    }
                    else{
                        break
                    }
                }
                indent2.push(0)
                color2.push('white')
                indentAnswer2.push(temp)
            }
            console.log(sequence2)    
        }
    })
}
const check = async () =>{
    if (questionType === 'context'){
        let deletePlaceHolder = 0
        for (let i = 0; i < sequence.length; i++){
            if(pool.answer[i - deletePlaceHolder].toString().includes("Placeholder")){
                let placeHolderLine = pool.answer[i - deletePlaceHolder].toString()
                pool.answer.splice(i - deletePlaceHolder, 1)
                pool.code.push(placeHolderLine)
                deletePlaceHolder = deletePlaceHolder + 1
            }
        }
    }
    checked.value = true
    let score = 0
    let score2 = 0
    for (let i = 0; i < sequence.length; i++) {
        if (pool.answer.length <= i){
            let difference = sequence.length - pool.answer.length
            alert("Need to add " + difference + " more lines in the right code pool.")
            break
        }
        let tempSeq = sequence[i]
        let tempAnswer = pool.answer[i]
        tempSeq = tempSeq.replace(/\u00a0/g, ' ')
        if(questionType === 'multiple-steps'){
            tempAnswer = tempAnswer.slice(8, tempAnswer.length)
        }
        if (questionType === 'context'){
            tempAnswer = tempAnswer.slice(2, tempAnswer.length)
        }
        tempAnswer = tempAnswer.replace(/\u00a0/g, ' ')
        tempSeq = tempSeq.toString().trim()
        tempAnswer = tempAnswer.toString().trim()
        if (tempSeq !== tempAnswer) {
            color[i] = '#ff6251'
            score = score + 0
            for(let j = 0; j < distractorCode.length; j++){
                let tempDistractor = distractorCode[j].toString().trim()
                if (tempDistractor === tempAnswer){
                    alert("Reason: " + distractorReason[j])
                }
            }
        }else if (indent[i] !== indentAnswer[i]){
            color[i] = "#ffd877"
            score = score + 0.5
        }
        else{
            color[i] = "#b1dd8c"
            score = score + 1
        }
    }
    if (questionType === 'context' || questionType === 'insert-key-code'){
        score = score - contextNum.value
        if (score < 0){
            alert("You need to place the context in the original place with original indent.")
            scoreShow.value = (score * 100).toFixed(0) + "%"
            alert(Math.abs(Math.floor(score)) + " context line(s) is/are not placed in the original place with original indent.")
        }else if (score === 0){
            scoreShow.value = (score * 100).toFixed(0) + "%"
            alert("The answer on the left is scored as " + scoreShow.value + ".")
        }else {
            score = score / (sequence.length - contextNum.value)
            scoreShow.value = (score * 100).toFixed(0) + "%"
            alert("The answer on the left is scored as " + scoreShow.value + ".")
        }
    }else{
        scoreShow.value = (score / sequence.length * 100).toFixed(0) + "%"
        alert("The answer on the right is scored as " + scoreShow.value + ".")
    }
    if (questionType === "compare-algorithm"){
        for (let i = 0; i < sequence2.length; i++) {
            if (pool.buffer.length <= i){
                let difference = sequence2.length - pool.buffer.length
                alert("Need to add " + difference + " more lines in the middle code pool")
                break
            }
            let tempSeq = sequence2[i]
            let tempAnswer = pool.buffer[i]
            tempSeq = tempSeq.replace(/\u00a0/g, ' ')
            tempAnswer = tempAnswer.replace(/\u00a0/g, ' ')
            tempSeq = tempSeq.toString().trim()
            tempAnswer = tempAnswer.toString().trim()
            if (tempSeq !== tempAnswer) {
                color2[i] = '#ff6251'
                score2 = score2 + 0
                for(let j = 0; j < distractorCode2.length; j++){
                    let tempDistractor = distractorCode2[j].toString().trim()
                    if (tempDistractor === tempAnswer){
                        alert("Reason: " + distractorReason2[j])
                    }
                }
            }else if (indent2[i] !== indentAnswer2[i]){
                color2[i] = "#ffd877"
                score2 = score2 + 0.5
            }
            else{
                color2[i] = "#b1dd8c"
                score2 = score2 + 1
            }
        }
        scoreShow2.value = (score2 / sequence2.length * 100).toFixed(0) + "%"
        alert("The answer on the middle is scored as " + scoreShow2.value + ".")
    }
    totalScore.value = ((score + score2) / (sequence.length + sequence2.length) * 100).toFixed(0) + "%"
    console.log(totalScore.value)
    const queryScore = "http://" + config.apiServer + ":" + config.port + "/api/record/" + store.state.UID + "/" + QID
    axios.get(queryScore).then((res) => {
        if (res.data.status === 'success') {
            console.log(res.data.record)
            if (res.data.record.length === 0){
                const query = "http://" + config.apiServer + ":" + config.port + "/api/record/create"
                axios.post(query, {
                    UID: store.state.UID,
                    QID: QID,
                    Score: totalScore.value
                }).then((res) => {
                    if (res.data.status === 'success') {
                        console.log("Recorded")
                    }
                })
            }else{
                if (res.data.record.Score < totalScore.value){
                    const query = "http://" + config.apiServer + ":" + config.port + "/api/record/update/" + store.state.UID + "/" + QID
                    axios.post(query, {
                        Score: totalScore.value
                    }).then((res) => {
                        if (res.data.status === 'success') {
                            console.log("Recorded")
                        }
                    })
                }
            }
        }
    })
}
const decreaseIndent = (i: number) =>{
    if (questionType === 'multiple-steps'){
        let tempList = pool.answer[i].split('\u{3011}')
        tempList[1] = tempList[1].replace('\u00a0\u00a0\u00a0\u00a0', '')
        pool.answer[i] = tempList[0] + '\u{3011}' + tempList[1]
        indent[i] = indent[i] - 1
        if (indent[i] < 0){
            indent[i] = 0
        }
    }else if (questionType === 'context'){
        if (pool.answer[i].includes('\u{1F4D6}')){
            let tempList = pool.answer[i].split('\u{1F4D6}')
            tempList[1] = tempList[1].replace('\u00a0\u00a0\u00a0\u00a0', '')
            pool.answer[i] = tempList[0] + '\u{1F4D6}' + tempList[1]
            indent[i] = indent[i] - 1
            if (indent[i] < 0){
                indent[i] = 0
            }
        }else{
            indent[i] = indent[i] - 1
            if (indent[i] < 0){
                indent[i] = 0
            }else{
                pool.answer[i] = pool.answer[i].replace('\u00a0\u00a0\u00a0\u00a0', '')
            }
        }
    }else{
        pool.answer[i] = pool.answer[i].replace('\u00a0\u00a0\u00a0\u00a0', '')
        indent[i] = indent[i] - 1
        if (indent[i] < 0){
            indent[i] = 0
        }
    }  
}
const increaseIndent = (i: number) =>{
    if (questionType === 'multiple-steps'){
        let tempList = pool.answer[i].split('\u{3011}')
        tempList[1] = '\u00a0\u00a0\u00a0\u00a0' + tempList[1]
        pool.answer[i] = tempList[0] + '\u{3011}' + tempList[1]
        indent[i] = indent[i] + 1
    }else if (questionType === 'context'){
        if (pool.answer[i].includes('\u{1F4CD}')){
            let tempList = pool.answer[i].split('\u{1F4CD}')
            tempList[1] = '\u00a0\u00a0\u00a0\u00a0' + tempList[1]
            pool.answer[i] = tempList[0] + '\u{1F4CD}' + tempList[1]
            indent[i] = indent[i] + 1
        }else{
            pool.answer[i] = '\u00a0\u00a0\u00a0\u00a0' + pool.answer[i]
            indent[i] = indent[i] + 1
        }
    }else{
        pool.answer[i] = '\u00a0\u00a0\u00a0\u00a0' + pool.answer[i]
        indent[i] = indent[i] + 1
    }
}
const removeBackgroundColor = () =>{
    for (let i = 0; i < color.length; i++) {
        color[i] = 'white'
    }
}
const removeBackgroundColor2 = () =>{
    for (let i = 0; i < color2.length; i++) {
        color2[i] = 'white'
    }
}
const decreaseIndent2 = (i: number) =>{
    pool.buffer[i] = pool.buffer[i].replace('\u00a0\u00a0\u00a0\u00a0', '')
    indent2[i] = indent2[i] - 1
    if (indent2[i] < 0){
        indent2[i] = 0
    }
}
const increaseIndent2 = (i: number) =>{
    pool.buffer[i] = '\u00a0\u00a0\u00a0\u00a0' + pool.buffer[i]
    indent2[i] = indent2[i] + 1
}
// For multiple steps
const getBlocks= async () =>{
    if (questionType === 'multiple-steps'){
        const query = "http://" + config.apiServer + ":" + config.port + "/api/block/" + QID
        axios.get(query).then((res) => {
            if (res.data.status === 'success') {
                for (let i = 0; i < res.data.blocks.length; i++) {
                    blocks.push(res.data.blocks[i].FragmentSeq)
                }
                getFragments()
            }
        })
    }else{
        getFragments()
    }
}
getQuestionInformation()
getBlocks()
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
        <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded" v-show="questionType === 'compare-algorithm'">
        <h6>{{ solutionName2 }}</h6>
        <VueDraggableNext class = "draggable-list" :list="pool.buffer" group = "pool" @change="removeBackgroundColor2()">
            <div v-for="(fragment, i) in pool.buffer" :key="i" >
                <div v-bind:style="[checked == true? {backgroundColor: color2[i]} : {backgroundColor: white}]" class="bg-white mt-3 p-2 shadow border rounded">                        
                    <p>
                        <button @click="decreaseIndent2(i)" title="Decrease Indent" type="button" class="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <svg class="w-4 h-4 rotate-180" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            <span class="sr-only">Decrease Indent</span>
                        </button>
                        <button @click="increaseIndent2(i)" title="Increase Indent" type="button" class="text-blue-700 border border-blue-700 hover:bg-blue-700 hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                            <span class="sr-only">Increase Indent</span>
                        </button>
                        {{ fragment }}
                    </p>
                </div>
            </div>
        </VueDraggableNext>
    </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>{{ solutionName }}</h6>
        <VueDraggableNext class = "draggable-list" :list="pool.answer" group = "pool" @change="removeBackgroundColor()">
            <div v-for="(fragment, i) in pool.answer" :key="i" >
                <div v-bind:style="[(checked == true? {backgroundColor: color[i]} : {backgroundColor: white}), (isPlaceholder[i] == true? {color: grey} : {color: black})]" class="bg-white mt-3 p-2 shadow border rounded">                        
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