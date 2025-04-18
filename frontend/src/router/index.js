import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Recommendations from '../components/Recommendations.vue' // 新增 推荐

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/recommendations', name: 'Recommendations', component: Recommendations }// 新增 推荐
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
