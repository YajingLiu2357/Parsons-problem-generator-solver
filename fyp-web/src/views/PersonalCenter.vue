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
const Cname = reactive([])
const CnameShow = reactive([])
const score = reactive([])
const count = ref(0)
const manageCount = ref(0)
const manageQuestionID = reactive([])
const manageQuestionName = reactive([])
const manageQuestionType = reactive([])
const showCreateClass = ref(false)
const className = ref('')
const classID = ref('')
const viewRecord = ref(true)
const viewQuestion = ref(false)
const viewClass = ref(false)
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
        const query = "http://" + config.apiServer + ":" + config.port + "/api/record/getAll/teacher/" + state.value.UID
        axios.get(query).then((res) => {
            count.value = res.data.records.length
            console.log(res.data.status)
            // for (let i = 0; i < res.data.records.length; i++) {
            //     questionID.push(res.data.records[i].QID)
            //     score.push(res.data.records[i].Score)
            //     const query1 = "http://" + config.apiServer + ":" + config.port + "/api/question/" + questionID[i]
            //     axios.get(query1).then((res) => {
            //         if (res.data.status === 'success') {
            //             questionName.push(res.data.question.Qname)
            //             questionType.push(res.data.question.Type)
            //         } else {
            //             alert(res.data.status)
            //         }
            //     })
            // }
            for (let i = 0; i < res.data.records.length; i++){
                Cname.push(res.data.records[i].Cname)
                questionName.push(res.data.records[i].Qname)
                questionType.push(res.data.records[i].type)
                score.push(res.data.records[i].Score)
            }
            let temp = Cname[0]
            CnameShow.push(temp)
            for (let i = 0; i < Cname.length; i++){
                if (Cname[i] != temp){
                    CnameShow.push(Cname[i])
                    temp = Cname[i]
                }
            }
        })
    }
}
getAllScore()
const changeViewRecord = () => {
    viewRecord.value = true
    viewQuestion.value = false
    viewClass.value = false
}
const changeViewQuestion = () => {
    viewRecord.value = false
    viewQuestion.value = true
    viewClass.value = false
}
const changeViewClass = () => {
    viewRecord.value = false
    viewQuestion.value = false
    viewClass.value = true
}
const tryAgain = (i:number) => {
    router.push('/question/' + questionID[i] + '/' + questionType[i])
}
const listQuestion = async () => {
    if (state.value.userStatus != "student"){
        const query = "http://" + config.apiServer + ":" + config.port + "/api/question/getAll/teacher/" + state.value.UID
        axios.get(query).then((res) => {
            if (res.data.status === 'success') {
                manageCount.value = res.data.questions.length
                console.log(res.data.questions.length)
                for (let i = 0; i < res.data.questions.length; i++) {
                    manageQuestionID.push(res.data.questions[i].QID)
                    manageQuestionName.push(res.data.questions[i].Qname)
                    manageQuestionType.push(res.data.questions[i].Type)
                }
            } else {
                alert(res.data.status)
            }
        })
    }
}
// Create a new question
const createQuestion = () => {
    if (state.value.userStatus != "student"){
        router.push('/input_question')
    }
}

// Edit the question
const editQuestion = (i:number) => {
    if (state.value.userStatus != "student"){
        router.push('/edit_question/' + manageQuestionID[i])
    }
}

// Delete the question
const deleteQuestion = async (i:number) => {
    if (state.value.userStatus != "student"){
        const query = "http://" + config.apiServer + ":" + config.port + "/api/question/" + manageQuestionID[i]
        axios.delete(query).then((res) => {
        if (res.data.status === 'success') {
            alert("Delete successfully")
            manageQuestionID.splice(i, 1)
            manageQuestionName.splice(i, 1)
            manageQuestionType.splice(i, 1)
            manageCount.value -= 1
        } else {
            alert(res.data.status)
        }
    })
    }
}
listQuestion()

// Create a new class
const showCreateClassBox = () => {
    showCreateClass.value = true
}
// May lack of back-end support
// const createClass = async () => {
//     if (state.value.userStatus != "student"){
//         const query = "http://" + config.apiServer + ":" + config.port + "/api/class/create/" + state.value.UID
//         axios.post(query, {
//             Cname: className.value
//         }).then((res) => {
//             if (res.data.status === 'success') {
//                 alert("Create successfully")
//                 showCreateClass.value = false
//             } else {
//                 alert(res.data.status)
//             }
//         })
//     }
// }
// const listClass = async () => {
//     if (state.value.userStatus != "student"){
//         const query = "http://" + config.apiServer + ":" + config.port + "/api/class/getAll/teacher/" + state.value.UID
//         axios.get(query).then((res) => {
//             if (res.data.status === 'success') {
//                 classCount.value = res.data.classes.length
//                 for (let i = 0; i < res.data.classes.length; i++) {
//                     classID.push(res.data.classes[i].CID)
//                     className.push(res.data.classes[i].Cname)
//                 }
//             } else {
//                 alert(res.data.status)
//             }
//         })
//     }
// }
// const updateClass = async () => {
//     if (state.value.userStatus != "student"){
//         const query = "http://" + config.apiServer + ":" + config.port + "/api/class/" + classID.value
//         axios.put(query, {
//             Cname: className.value
//         }).then((res) => {
//             if (res.data.status === 'success') {
//                 alert("Update successfully")
//             } else {
//                 alert(res.data.status)
//             }
//         })
//     }
// }
// const deleteClass = async () => {
//     if (state.value.userStatus != "student"){
//         const query = "http://" + config.apiServer + ":" + config.port + "/api/class/" + classID.value
//         axios.delete(query).then((res) => {
//             if (res.data.status === 'success') {
//                 alert("Delete successfully")
//             } else {
//                 alert(res.data.status)
//             }
//         })
//     }
// }

// const updateUserInformation = () => {
//     if (state.value.userStatus != "student"){
//         router.push('/update_user_information')
//     }
// }
// const deleteUser = async () => {
//     if (state.value.userStatus != "student"){
//         const query = "http://" + config.apiServer + ":" + config.port + "/api/user/" + state.value.UID
//         axios.delete(query).then((res) => {
//             if (res.data.status === 'success') {
//                 alert("Delete successfully")
//             } else {
//                 alert(res.data.status)
//             }
//         })
//     }
// }
</script>
<template>
    <div class="container mx-auto sm:px-4 mt-5 mb-10">
        <div class="flex flex-col space-y-4 mb-10 ml-15 md:space-y-0 md:space-x-20 md:flex-row">
			<img v-show="state.userStatus == 'teacher' || state.userStatus == 'admin'" src="../images/teacher.png" alt="" class="w-56 h-56 ml-10 border rounded-full md:justify-self-start dark:bg-gray-500 dark:border-gray-700">
			<img v-show="state.userStatus == 'student'" src="../images/students.png" alt="" class="w-56 h-56 border rounded-full md:justify-self-start dark:bg-gray-500 dark:border-gray-700">
            <div class="flex flex-col">
				<h1 class="text-3xl font-semibold text-center py-3 md:text-left">{{ state.userName }}</h1>
                <h2 class="text-xl text-center py-3 md:text-left">{{ state.userEmail }}</h2>
                <h2 class="text-xl text-center py-3 md:text-left">{{ state.userStatus }}</h2>
			</div>
		</div>
        <div v-show="state.userStatus == 'teacher' || state.userStatus == 'admin'">
            <div v-show="viewRecord">
            <div>
                <ul class="flex border-b">
                <li class="-mb-px mr-1">
                    <a class="bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold">View Students' Exercise Records</a>
                </li>
                <li class="mr-1">
                    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" @click="changeViewQuestion">Manage Questions</a>
                </li>
                <li class="mr-1">
                    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" @click="changeViewClass">Manage Classes</a>
                </li>
                <!-- <li class="mr-1">
                    <a class="bg-white inline-block py-2 px-4 text-gray-400 font-semibold" href="#">Tab</a>
                </li> -->
                </ul>
            </div>
            <div class="container mx-auto sm:px-4 mt-5 mb-5" v-show="state.userStatus != 'student'">
                <div class="relative overflow-x-auto">
                    <div v-for="Class in CnameShow">
                        <h3 class="text-xl pb-5">{{ Class }}</h3>
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
                     <th v-show="Class == Cname[i-1]" scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ questionName[i-1] }}
                    </th>
                    <td class="px-6 py-4" v-show="Class == Cname[i-1]">
                        {{ questionType[i-1] }}
                    </td>
                    <td class="px-6 py-4" v-show="Class == Cname[i-1]">
                        {{ score[i-1] }}
                    </td>
                    </tr>
                    </tbody>
                    </table>
                    </div>
                </div>
                <!-- <div class="relative overflow-x-auto">
                    <h3 class="text-xl pb-5">COMP121</h3>
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
                </div>   -->
            </div>
            </div>
            <div v-show="viewQuestion">
            <div>
                <ul class="flex border-b">
                <li class="mr-1">
                    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" @click="changeViewRecord">View Students' Exercise Record</a>
                </li>
                <li class="-mb-px mr-1">
                    <a class="bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold">Manage Questions</a>
                </li>
                <li class="mr-1">
                    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" @click="changeViewClass">Manage Classes</a>
                </li>
                </ul>
            </div>
            <div class="container mx-auto sm:px-4 mt-5 mb-5" v-show="state.userStatus != 'student'">
                <div class="relative overflow-x-auto">
                    <button @click="createQuestion" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Create New Question</button>
                    <p class="text-lg font-semibold">Note: The edit action can only change the basic informaiton about the question (question name, question scope and question description).</p>
                    <p class="text-lg font-semibold">If you need to change the question type, prepared solution and customization, you can only delete the question and recreate it again.</p>
                    <table class="mt-3 w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                    <th scope="col" class="px-6 py-3">
                        Question Name
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Question Type
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Edit
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Delete
                    </th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="i in manageCount" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                     <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ manageQuestionName[i-1] }}
                    </th>
                    <td class="px-6 py-4">
                        {{ manageQuestionType[i-1] }}
                    </td>
                    <td class="px-6 py-4">
                        <a @click=" editQuestion(i-1)" class="px-4 py-2 font-medium tracking-wide text-white capitalize transition-colors duration-200 transform bg-blue-500 rounded-md dark:bg-gray-800 hover:bg-blue-600 dark:hover:bg-gray-700 focus:outline-none focus:bg-blue-600 dark:focus:bg-gray-700">
                        Edit
                    </a>
                    </td>
                    <td class="px-6 py-4">
                        <a @click=" deleteQuestion(i-1)" class="px-4 py-2 font-medium tracking-wide text-white capitalize transition-colors duration-200 transform bg-blue-500 rounded-md dark:bg-gray-800 hover:bg-blue-600 dark:hover:bg-gray-700 focus:outline-none focus:bg-blue-600 dark:focus:bg-gray-700">
                        Delete
                    </a>
                    </td>
                    </tr>
                    </tbody>
                    </table>
                </div>
            </div>
            </div>
        </div>
        <div v-show="state.userStatus == 'student' ">
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
        </div>
    </div>
</template>