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
const questionType = route.params.Type
description.value = ""
const sequence = reactive([])
const bid = ref('')
// const solutionType = ref('')
const FID = reactive([])
const addDistractorBoxShow = ref(false)
const codeLength = ref(0)
const distractorLine = ref(0)
const distractorCode = ref('')
const distractorReason = ref('')
const addDifficultyLevelBoxShow = ref(false)
const difficultyLevel = ref(1)
const addBlockBoxShow = ref(false)
const startLine = ref(0)
const endLine = ref(0)
const blockType = ref('')
const SID = reactive([])
const solutionSeq = ref('')
const difficultyLevelID = ref('')
const FragmentSeq = ref('')
const BlockSeq = ref('')
const blockCover = reactive([])
const context = reactive([])
const key = reactive([])
const divideCodeBoxShow = ref(false)
const step = reactive([])
// For multiple solutions
const sequence2 = reactive([])
const bid2 = ref('')
const FID2 = reactive([])
const codeLength2 = ref(0)
const blockCover2 = reactive([])
const context2 = reactive([])
const key2 = reactive([])
const addDistractorBoxShow2 = ref(false)
const distractorLine2 = ref(0)
const distractorCode2 = ref('')
const distractorReason2 = ref('')

const getQuestion = async () => {
   const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            QName.value = res.data.question.Qname
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
            for (let i = 0; i < res.data.fragments.length; i++) {
               if(res.data.fragments[i].BID != bid.value){
                   bid2.value = res.data.fragments[i].BID
                   console.log(bid2.value)
                   getSequence2()
                   break
               }
            }
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
                blockCover.push(false)
                context.push(false)
                key.push(false)
            }
        }
    })
}
// For multiple solutions
const getSequence2 = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/sequence/" + bid2.value
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            codeLength2.value = res.data.sequence.length
            for (let i = 0; i < res.data.sequence.length; i++) {
                FID2.push(res.data.FID[i])
                let j = i + 1
                let temp = "Line " + j.toString() + ": " + res.data.sequence[i].replace(/\n/g, '').replace(/ /g, '\u00a0')
                sequence2.push(temp)
                blockCover2.push(false)
                context2.push(false)
                key2.push(false)
            }
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

// For multiple solutions
const addDistractor2 = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/distractor/create"
    axios.post(query, {
        Code: distractorCode2.value,
        Reason: distractorReason2.value,
        FID: FID2[distractorLine2.value - 1],
    }).then((res) => {
        if (res.data.status === 'success') {
            alert("Add Distractor Success")
            addDistractorBoxShow2.value = false
            distractorLine2.value = 0
            distractorCode2.value = ''
            distractorReason2.value = ''
        }
    })
}

const getSID = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            solutionSeq.value = res.data.question.SolutionSeq
            let temp = []
            temp=solutionSeq.value.split(";")
            temp.pop()
            for (let i = 0; i < temp.length; i++) {
                SID.push(temp[i])
            }
        }
    })
}

const addDifficultyLevel = async () => {
    addDifficultyLevelBoxShow.value = true
    difficultyLevel.value = difficultyLevel.value + 1
    const query = "http://" + config.apiServer + ":" + config.port + "/api/difficulty_level/create"
    axios.post(query, {
        Level: difficultyLevel.value,
        BlockSeq: '',
        // SID for single solution
        SID: SID[0],
    }).then((res) => {
        if (res.data.status === 'success') {
            difficultyLevelID.value = res.data.uuid
        }
    })
}

const addBlock = async () => {
    if (startLine.value > endLine.value) {
        alert("Start Line must be smaller than or equal to End Line")
        return
    }
    for (let i = startLine.value - 1; i < endLine.value; i++) {
        FragmentSeq.value = FragmentSeq.value + FID[i] + ";"
        blockCover[i] = true
    }
    const query = "http://" + config.apiServer + ":" + config.port + "/api/block/create"
    axios.post(query, {
        Type: blockType.value,
        FragmentSeq: FragmentSeq.value,
        DLID: difficultyLevelID.value,
    }).then((res) => {
        if (res.data.status === 'success') {
            BlockSeq.value = BlockSeq.value + res.data.uuid + ";"
            alert("Add Block Success")
            addBlockBoxShow.value = false
            startLine.value = 0
            endLine.value = 0
            blockType.value = ''
            FragmentSeq.value = ''
        }
    })
}

const updateDifficultyLevel = async () => {
    for (let i = 0; i < codeLength.value; i++) {
        if (blockCover[i] === false) {
            alert("Please cover all the code")
            return
        }
    }
    const query = "http://" + config.apiServer + ":" + config.port + "/api/difficulty_level/update/" + difficultyLevelID.value
    axios.post(query, {
        Level: difficultyLevel.value,
        BlockSeq: BlockSeq.value,
        // SID for single solution
        SID: SID[0],
    }).then((res) => {
        if (res.data.status === 'success') {
            addDifficultyLevelBoxShow.value = false
            addBlockBoxShow.value = false
            startLine.value = 0
            endLine.value = 0
            blockType.value = ''
            FragmentSeq.value = ''
            BlockSeq.value = ''
        }
    })
}

// const confirm = async () => {
//     const query = "http://" + config.apiServer + ":" + config.port + "/api/solution/update/" + SID[0]
//     axios.post(query, {
//         Type: solutionType.value,
//     }).then((res) => {
//         if (res.data.status === 'success') {
//             alert("Confirm Success")
//             router.push(('/question/' + QID))
//         }
//     })
// }
const confirm = async () => {
    //For context type question
    if (questionType == "context") {
        for (let i = 0; i < codeLength.value; i++) {
            if (context[i] === true) {
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "context",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        router.push(('/question/' + QID + '/' + questionType))
                    }
                })
            }else{
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "not context",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        router.push(('/question/' + QID + '/' + questionType))
                    }
                })
            }
        }
    }
    //For insert-key-code type question
    else if (questionType == "insert-key-code") {
        for (let i = 0; i < codeLength.value; i++) {
            if (key[i] === true) {
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "key code",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        router.push(('/question/' + QID + '/' + questionType))
                    }
                })
            }else{
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "not key code",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        router.push(('/question/' + QID + '/' + questionType))
                    }
                })
            }
        }
    }
    else{
        router.push(('/question/' + QID + '/' + questionType))
    }
}

// For multiple difficulty level 
const createEasierVersion = async () => {
    //For context type question
    if (questionType == "context") {
        for (let i = 0; i < codeLength.value; i++) {
            if (context[i] === true) {
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "context",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        const queryEasierVersion = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/create"
                        axios.post(queryEasierVersion, {
                            QID: QID,
                            UID: store.state.UID,
                        }).then((res) => {
                            if (res.data.status === 'success') {
                                alert("Create Easier Version Success")
                                router.push(('/input_question_type/' + res.data.EasierVersionQID))
                            }
                        })
                    }
                })
            }else{
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "not context",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        const queryEasierVersion = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/create"
                        axios.post(queryEasierVersion, {
                            QID: QID,
                            UID: store.state.UID,
                        }).then((res) => {
                            if (res.data.status === 'success') {
                                alert("Create Easier Version Success")
                                router.push(('/input_question_type/' + res.data.EasierVersionQID))
                            }
                        })
                    }
                })
            }
        }
    }
    //For insert-key-code type question
    else if (questionType == "insert-key-code") {
        for (let i = 0; i < codeLength.value; i++) {
            if (key[i] === true) {
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "key code",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        const queryEasierVersion = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/create"
                        axios.post(queryEasierVersion, {
                            QID: QID,
                            UID: store.state.UID,
                        }).then((res) => {
                            if (res.data.status === 'success') {
                                alert("Easier version created")
                                router.push(('/input_question_type/' + res.data.EasierVersionQID))
                            }
                        })
                    }
                })
            }else{
                const query = "http://" + config.apiServer + ":" + config.port + "/api/fragment_type/update/" + FID[i]
                axios.post(query, {
                    Type: "not key code",
                }).then((res) => {
                    if (i == codeLength.value - 1){
                        const queryEasierVersion = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/create"
                        axios.post(queryEasierVersion, {
                            QID: QID,
                            UID: store.state.UID,
                        }).then((res) => {
                            if (res.data.status === 'success') {
                                alert("Easier version created")
                                router.push(('/input_question_type/' + res.data.EasierVersionQID))
                            }
                        })
                    }
                })
            }
        }
    }
    else{
        const queryEasierVersion = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/create"
        axios.post(queryEasierVersion, {
            QID: QID,
            UID: store.state.UID,
        }).then((res) => {
            if (res.data.status === 'success') {
                alert("Easier version created")
                router.push(('/input_question_type/' + res.data.EasierVersionQID))
            }
        })
    }
}
// For context type question
const setContext = (i: number) =>{
    if (context[i] === true) {
        context[i] = false
    } else {
       context[i] = true
    }   
}
// For insert-key-code type question
const setKeyCode = (i: number) =>{
    if (key[i] === true) {
        key[i] = false
    } else {
       key[i] = true
    }   
}
// For multiple steps type question
const divideCode = async () =>{
    divideCodeBoxShow.value = true
    difficultyLevel.value = difficultyLevel.value + 1
    const query = "http://" + config.apiServer + ":" + config.port + "/api/difficulty_level/create"
    axios.post(query, {
        Level: difficultyLevel.value,
        BlockSeq: '',
        // SID for single solution
        SID: SID[0],
    }).then((res) => {
        if (res.data.status === 'success') {
            difficultyLevelID.value = res.data.uuid
        }
    })
}
const groupCode = async () =>{
    if (startLine.value > endLine.value) {
        alert("Start Line must be smaller than or equal to End Line")
        return
    }
    for (let i = startLine.value - 1; i < endLine.value; i++) {
        FragmentSeq.value = FragmentSeq.value + FID[i] + ";"
        blockCover[i] = true
    }
    step.push("Line" + startLine.value + " - Line" + endLine.value)
    const query = "http://" + config.apiServer + ":" + config.port + "/api/block/create"
    axios.post(query, {
        Type: '',
        FragmentSeq: FragmentSeq.value,
        DLID: difficultyLevelID.value,
    }).then((res) => {
        if (res.data.status === 'success') {
            BlockSeq.value = BlockSeq.value + res.data.uuid + ";"
            alert("Add Block Success")
            addBlockBoxShow.value = false
            startLine.value = 0
            endLine.value = 0
            FragmentSeq.value = ''
        }
    })    
}
const finshDivideCode = async () =>{
    for (let i = 0; i < codeLength.value; i++) {
        if (blockCover[i] === false) {
            alert("Please cover all the code")
            return
        }
    }
    const query = "http://" + config.apiServer + ":" + config.port + "/api/difficulty_level/update/" + difficultyLevelID.value
    axios.post(query, {
        Level: difficultyLevel.value,
        BlockSeq: BlockSeq.value,
        // SID for single solution
        SID: SID[0],
    }).then((res) => {
        if (res.data.status === 'success') {
            divideCodeBoxShow.value = false
            addBlockBoxShow.value = false
            startLine.value = 0
            endLine.value = 0
            blockType.value = ''
            FragmentSeq.value = ''
            BlockSeq.value = ''
            for (let i = 0; i < step.length; i++) {
                step.pop()
            }
        }
    })
}
getQuestion()
getBID()
getSID()
</script>
<template>
    <div>
  <!-- <div class="container mx-auto sm:px-4 mt-5 mb-5">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
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
                  required
              >
                <option value="fixed order">fixed order</option>
                <option value="not fixed order">not fixed order</option>
                <option value="insert key code">insert key code</option>
              </select>
            </div>
            <div class="mt-2 mb-2 inline-block">
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
                    @click="addDifficultyLevel"
                >
                Add Difficulty Level
                </button>
            </div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
            <div v-if="addDifficultyLevelBoxShow">
                <h6>Add Difficulty Level</h6>
                <div>Level: {{ difficultyLevel-1 }}</div>
                <button
                    class="inline-block mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addBlockBoxShow = true"
                >
                Add Block 
                </button>
                <div v-if="addBlockBoxShow">
                <h6>Add Block</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >From line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="startLine"
                        required
                    >
                        <option v-for="i in codeLength" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >To line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="endLine"
                        required
                    >
                        <option v-for="i in codeLength" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Block Type:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="blockType"
                        required
                    >
                    <option value="single fragment">single fragment</option>
                    <option value="multiple fragments(context)">multiple fragments(context)</option>
                    <option value="multiple fragments(unit)">multiple fragments(unit)</option>
                    <option value="multiple fragments(standard)">multiple fragments(standard)</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <button
                        class="ml-3 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="addBlock"
                    >
                    Add Block
                    </button>
                </div>
            </div>
                <div class="mt-2 mb-2">
                    <button
                        class="ml-3 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="updateDifficultyLevel"
                    >
                    Finsh
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
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm
        </button> 
  </div> -->
  <div class="container mx-auto sm:px-4 mt-5 mb-5" v-if="questionType === 'traditional'">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2 inline-block">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button>
            </div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm and go to home page
          <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button> 
        <button
            class="float-right mt-7 mr-5 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="createEasierVersion"
        >
          Confirm and create easier version
          <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button> 
  </div>
  <div class="container mx-auto sm:px-4 mt-5 mb-5" v-if="questionType === 'context'">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2 inline-block">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button>
            </div>
            <div><p>You can press the pin icons to set some context codes as tips for students</p></div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
                    <p>                        
                        <button @click="setContext(i)" v-show="context[i] == false" title="Choose this line as context" type="button" class="text-blue-700  hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <img src="../images/push-pin-blue-icon.png" class="w-4 h-4"/>
                            <span class="sr-only">Choose this line as context</span>
                        </button>
                        <button @click="setContext(i)" v-show="context[i] == true" title="Choose this line as context" type="button" class="text-blue-700  hover:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-small rounded-lg text-sm p-1.5 text-center inline-flex items-center mr-2 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:focus:ring-blue-800">
                            <img src="../images/push-pin-blue-icon-pinned.jpeg" class="w-4 h-4"/>
                            <span class="sr-only">Choose this line as context</span>
                        </button>
                        {{ fragment }}
                    </p>
                </div>
            </div>

    </div>
    </div>
    <button
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm
        </button>
        <button
            class="float-right mt-7 mr-5 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="createEasierVersion"
        >
          Confirm and create easier version
          <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button> 
  </div>
  <div class="container mx-auto sm:px-4 mt-5 mb-5" v-if="questionType === 'insert-key-code'">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2 inline-block">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button>
            </div>
            <div><p>You can click the line you think is important to mark it as key code, and click agin to cancel.</p></div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
                    <p @click="setKeyCode(i)">
                        <img src="../images/key-code.png" v-show="key[i] == true" class="w-6 h-6 inline-block"/>
                        {{ fragment }}
                    </p>
                </div>
            </div>

    </div>
    </div>
    <button
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm
        </button>
        <button
            class="float-right mt-7 mr-5 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="createEasierVersion"
        >
          Confirm and create easier version
          <svg aria-hidden="true" class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button> 
  </div>
  <div class="container mx-auto sm:px-4 mt-5 mb-5" v-if="questionType === 'multiple-steps'">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2 inline-block">
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
                    @click="divideCode"
                    >
                    Divide Code Into Several Steps
                </button>
            </div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
            <div v-if="divideCodeBoxShow" class="block w-full">
                <h6>Divide Code Into Several Steps</h6>
                <div v-for="(s,i) in step" :key="i">Step {{ i+1 }}: {{ s }}</div>
                <button
                    v-if="!addBlockBoxShow"
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addBlockBoxShow = true"
                >
                Add Step 
                </button>
                <div v-if="addBlockBoxShow" class="block w-full">
                <h6>Group Codes</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >From line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="startLine"
                        required
                    >
                        <option v-for="i in codeLength" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >To line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="endLine"
                        required
                    >
                        <option v-for="i in codeLength" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <button
                        class="ml-3 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="groupCode"
                    >
                    Group
                    </button>
                </div>
            </div>
            <br/>
            <br/>
                <div class="mt-5 mb-2 block">
                    <button
                        class="block ml-3 float-right group relative justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="finshDivideCode"
                    >
                    Finsh
                    </button>
                </div>
            </div>
        </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Code</h6>
            <div v-for="(fragment, i) in sequence" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p @click="setKeyCode(i)">
                        <img src="../images/key-code.png" v-show="key[i] == true" class="w-6 h-6 inline-block"/>
                        {{ fragment }}
                    </p>
                </div>
            </div>

    </div>
    </div>
    <button
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm
        </button> 
  </div>
  <div class="container mx-auto sm:px-4 mt-5 mb-5" v-if="questionType === 'compare-algorithm'">
    <h2 class="text-center mb-6 font-medium text-gray-900">
          <div class="text-2xl">Customize Solution</div>
        </h2>
    <div class="flex flex-wrap ">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <h6>Question: {{ QName }}</h6>
            <p>{{ description }}</p>
            <div class="mt-2 mb-2 inline-block">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button>
            </div>
            <div v-if="addDistractorBoxShow">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
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
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode"
                        required
                    >
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
        <h6>Solution 1</h6>
            <div v-for="(fragment, i) in sequence" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>
                        {{ fragment }}
                    </p>
                </div>
            </div>
    </div>
</div>
<div class="flex flex-wrap mt-10">
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
            <div class="mt-2 mb-2 inline-block">
                <button
                    class="mr-9 mb-3 mt-3 float-left group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    type="submit"
                    @click="addDistractorBoxShow = true"
                >
                Add Distractor
                </button>
            </div>
            <div v-if="addDistractorBoxShow2">
                <h6>Add Distractor</h6>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Compare with line:</label
                    >
                    <select
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorLine2"
                        required
                    >
                        <option v-for="i in codeLength2" :value="i">{{ i }}</option>
                    </select>
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >Distractor code (one line python code):</label
                    >
                    <input
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorCode2"
                        required
                    >
                </div>
                <div class="mt-2 mb-2">
                    <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                    >The reason to add this distractor (This reason will be shown as feedback when students choose this distractor): </label
                    >
                    <textarea
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        v-model="distractorReason2"
                        required
                    >
                    </textarea>
                </div>
                <div class="mt-2 mb-2">
                    <button
                        class="ml-3 float-right group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        type="submit"
                        @click="addDistractor2"
                    >
                    Add Distractor
                    </button>
                </div>
            </div>
        </div>
      <div class="relative flex-grow max-w-full flex-1 px-4 mx-2 px-2 py-3 bg-gray-100 border rounded">
        <h6>Solution 2</h6>
            <div v-for="(fragment, i) in sequence2" :key="i">
                <div class="bg-white mt-3 p-2 shadow border rounded">
                    <p>
                        {{ fragment }}
                    </p>
                </div>
            </div>
    </div>
</div>
    <button
            class="float-right mt-7 group relative flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="confirm"
        >
          Confirm
        </button> 
  </div>
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