import { createRouter, createWebHashHistory, Router } from "vue-router"
import Home from "../views/Home.vue";

const webHistory = createWebHashHistory()

export default createRouter({
  history: webHistory,
  routes: [
    { path: "/", component: Home },
    // { path: "/", component: () => import (/* webpackChunkName: "home" */ "../views/InputQuestion.vue")},
    { path: "/about", component: () => import(/* webpackChunkName: "home" */ "../views/About.vue") },
    { path: "/login", component: () => import(/* webpackChunkName: "home" */ "../views/Login.vue") },
    { path: "/register", component: () => import(/* webpackChunkName: "home" */ "../views/Register.vue") },
    { path: "/input_question", component: () => import(/* webpackChunkName: "home" */ "../views/InputQuestion.vue") },
    { path: "/upload_solution/:QID/:Type", component: () => import(/* webpackChunkName: "home" */ "../views/UploadSolution.vue") },
    { path: "/question/:QID/:Type", component: () => import(/* webpackChunkName: "home" */ "../views/Question.vue") },
    { path: "/customize_solution/:QID/:Type", component: () => import(/* webpackChunkName: "home" */ "../views/CustomizeSolution.vue") },
    { path: "/input_question_type/:QID", component: () => import(/* webpackChunkName: "home" */ "../views/InputQuestionType.vue") },
    { path: "/personal-center", component: () => import(/* webpackChunkName: "home" */ "../views/PersonalCenter.vue") },
  ]
})