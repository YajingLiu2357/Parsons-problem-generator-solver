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
const isEasierVersion = ref(false)

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
            if (isEasierVersion.value === true) {
                router.push('/customize_solution/' + QID + '/' + type.value)
            }else{
                router.push('/upload_solution/' + QID + '/' + type.value)
            }
        } else {
            alert(res.data.status)
        }
    })
}
const checkEasierVersion = async () => {
    const query = "http://" + config.apiServer + ":" + config.port + "/api/easier_version/check/" + QID
    axios.get(query).then((res) => {
        if (res.data.status === 'success') {
            isEasierVersion.value = res.data.isEasierVersion
        }
    })
}

getQuestionInformation()
checkEasierVersion()

</script>

<template>
    <div class="min-h-full flex items-center justify-center  px-4 sm:px-6 lg:px-8">
      <div class="w-5/6 space-y-4">
        <h2 class="text-left font-medium text-gray-900">
          <div class="text-2xl">Choose Proper Question Type:</div>
          <div class="text-md">You can get some ideas from the conceptual gif images, and choose most appropriate one to describe your question.</div>
          <div class="text-md"><span class="font-bold">Note: </span>What is shown in conceptual images may not be indentical with actual situation.</div>
        </h2>
        <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-1" type="radio" value="traditional" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-bold text-gray-900 dark:text-gray-300">Traditional</h5>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- This type of question is the most basic Parsons Problem.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- One code pool and one answer pool.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- The code is divided into line level.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- No tip.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- Distractor allowed.</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-2" type="radio" value="context" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/context.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-bold text-gray-900 dark:text-gray-300">Context</h5>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- This type of question provides some context codes as tips.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- One code pool and one answer pool.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- The code is divided into line level.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- Some codes can be given in order as tips.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- Distractor allowed.</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700" v-show="false">
                <input v-model="type" id="bordered-radio-3" type="radio" value="insert-key-code" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-medium text-gray-900 dark:text-gray-300">Insert Key Code</h5>
                    <p class="block text-lg font-medium text-gray-900 dark:text-gray-300">Some description</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700" v-show="false">
                <input v-model="type" id="bordered-radio-4" type="radio" value="check-only-inside-block" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-medium text-gray-900 dark:text-gray-300">Check Only Inside Every Block</h5>
                    <p class="block text-lg font-medium text-gray-900 dark:text-gray-300">Some description</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-5" type="radio" value="multiple-steps" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/multiple-steps.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-bold text-gray-900 dark:text-gray-300">Multiple Steps</h5>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- This type of question provides 'step' labels as tips.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- One code pool and one answer pool.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- The lines covered by each step need to be preset.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- 'Step' label given as tips.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- Distractor allowed.</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700" v-show="false">
                <input v-model="type" id="bordered-radio-6" type="radio" value="compare-data-structure-implementation" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-medium text-gray-900 dark:text-gray-300">Compare Data Structure Implementation</h5>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">Some description</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700">
                <input v-model="type" id="bordered-radio-7" type="radio" value="compare-algorithm" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/compare-algorithm.gif" class="object-scale-down float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-bold text-gray-900 dark:text-gray-300">Compare Algorithm</h5>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- This type of question is to split two algorithms from one code pool.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- One code pool and two answer pools.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- The code is divided into line level.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- No tip.</p>
                    <p class="block text-lg font-normal text-gray-900 dark:text-gray-300">- Distractor allowed.</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700" v-show="false">
                <input v-model="type" id="bordered-radio-8" type="radio" value="link-together" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-medium text-gray-900 dark:text-gray-300">Link Together</h5>
                    <p class="block text-lg font-medium text-gray-900 dark:text-gray-300">Some description</p>
                </div>  
            </div>
            <div class="mt-4 mb-4 border-double border-4 border-cyan-600 flex items-center pl-4 rounded dark:border-gray-700" v-show="false">
                <input v-model="type" id="bordered-radio-9" type="radio" value="algorithm-analysis" name="bordered-radio" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                <img src="../images/traditional.gif" class="float-left w-120 h-80 m-5"/>
                <div>
                    <h5 class="block mt-5 mb-3 text-lg font-medium text-gray-900 dark:text-gray-300">Algorithm Analysis</h5>
                    <p class="block text-lg font-medium text-gray-900 dark:text-gray-300">Some description</p>
                </div>  
            </div>
          </div>
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
  </template>

<style scoped></style>
