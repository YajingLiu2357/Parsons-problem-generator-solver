<script setup lang="ts">
// import { reactive, ref, watch } from 'vue'
// import { computed } from "vue";
import axios from "axios"
import {computed, reactive, ref} from "vue"
import config from "../config"
import { useRoute, useRouter } from 'vue-router'
import { useStore} from 'vuex'
import FormData from 'form-data'

const questions = ref([]);
const store = useStore();
const router = useRouter();
const route = useRoute();

const state = computed(() => store.state)
const logout = () => {
    store.commit('signOut')
    router.push('/')
}

</script>
<template>
    <nav class="bg-white px-6 py-4">
        <div class="flex flex-col container mx-auto md:flex-row md:items-center md:justify-between">
            <div>
                    <a class="text-gray-800 text-xl font-bold md:text-2xl" href="#">
                        <img src="../images/parsons-problem-logo.png" class="h-12 inline-block">
                    </a>
                </div>
            <!-- <div class="flex justify-left">

            </div> -->
            <div class="flex flex-col md:flex-row md:-mx-4">
                <a class="my-1 text-gray-800 hover:text-blue-500 md:mx-4 md:my-0" href="#">Home</a>
                <a v-show= "state.userStatus == 'visitor'" class="my-1 text-gray-800 hover:text-blue-500 md:mx-4 md:my-0" href="#/login">Login</a>
                <a v-show="state.userStatus == 'teacher' || state.userStatus == 'admin'" class="my-1 text-gray-800 hover:text-blue-500 md:mx-4 md:my-0" href="#/input_question">Create New Question</a>
                <p v-show="state.userStatus != 'visitor'">Hi, {{ state.userName }}</p>
                <a v-show="state.userStatus != 'visitor'" class="my-1 text-gray-800 hover:text-blue-500 md:mx-4 md:my-0" href="#/personal-center">Personal center</a>
                <a v-show="state.userStatus != 'visitor'" class="my-1 text-gray-800 hover:text-blue-500 md:mx-4 md:my-0" @click ="logout">Logout</a>
            </div>
        </div>
    </nav>
</template>