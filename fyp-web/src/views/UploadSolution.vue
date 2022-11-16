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
const file = new File([],'')
const solutions = reactive([] as Array<File>)
const QID = route.params.QID

const initFile = () => {
    if (solutions.length > 0){
        while(solutions.length > 0){
            solutions.pop()
        }
    }
}

const onFileChange = (event) =>{
    initFile()
    const files = event.target.files || event.dataTransfer.files;
    if (files) {
        for (let i = 0; i < files.length; i++) {
            solutions.push(files[i])
        }
    }
}

const uploadSolution = () => {
    if (solutions.length === 0) {
        alert("Please select at least one file.")
    } else {
        if (store.state.userStatus === 'teacher') {
            const querySolution = "http://" + config.apiServer + ":" + config.port + "/api/solution/upload"
            const formData = new FormData()
            let solutionsName = ""
            for (let i = 0; i < solutions.length; i++) {
                formData.append('files', solutions[i])
                solutionsName += solutions[i].name + ";"
            }
            solutionsName = solutions[0].name
            axios.post(querySolution, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((res) => {
                if (res.data.status === 'success') {
                    const query = "http://" + config.apiServer + ":" + config.port + "/api/solution/create"
                    axios.post(query, {
                        Sname: solutionsName,
                        QID: QID,
                    }).then((res) => {
                        if (res.data.status === 'success') {
                            router.push('/question/' + QID)
                        } else {
                            alert(res.data.status)
                        }
                    })
                } else {
                    alert(res.data.status)
                }
            })
        } else {
            alert("You do not have the authority to add a new product.")
        }
    }
}

/**
const onFileChange = (event) => {
  const files = event.target.files || event.dataTransfer.files;
  solution.value = files[0]
  solutionName.value = solution.value.name
  let reader = new FileReader()
  reader.readAsDataURL(solution.value)
  reader.onload = function (){
    alert("finsh loading")
    const formData = new FormData();
    formData.append("files", solution.value)
    const queryFile = "http://" + config.apiServer + ":" + config.port + "/api/solution/upload"
    axios.post(queryFile, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
        }).then((res) => {
            if (res.data.status === 'success') {
                alert("File uploaded successfully")
            } else {
                alert(res.data.status)
            }
        })
    } 
}
*/

</script>
<template>
    <div class="min-h-full flex items-center justify-center py-6 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-4">
        <h2 class="text-left font-medium text-gray-900">
          <div class="text-2xl">Upload Solution</div>
        </h2>
        <div class="creation_form">
          <div class="border rounded-lg shadow-lg bg-white px-4">
            <div class="mt-4 mb-4">
              <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300"
              >Upload Solution File</label
              >
              <input
                  accept=".py"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder=""
                  required
                  type="file"
                  v-on:change="onFileChange"
                  multiple
              />
            </div>
          </div>
        </div>
        <button
            class="group relative w-full flex justify-center py-3 px-6 border border-transparent font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            type="submit"
            @click="uploadSolution"
        >
          Upload
        </button>
      </div>
    </div>
  </template>

<style scoped></style>