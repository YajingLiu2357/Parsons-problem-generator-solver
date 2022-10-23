import { createRouter, createWebHashHistory, Router } from "vue-router"
import Home from "../views/Home.vue";

const webHistory = createWebHashHistory()

export default createRouter({
  history: webHistory,
  routes: [
    { path: "/", component: Home },
    { path: "/about", component: () => import(/* webpackChunkName: "home" */ "../views/About.vue") },
    { path: "/login", component: () => import(/* webpackChunkName: "home" */ "../views/Login.vue") },
    { path: "/input_question", component: () => import(/* webpackChunkName: "home" */ "../views/InputQuestion.vue") },
  ]
})