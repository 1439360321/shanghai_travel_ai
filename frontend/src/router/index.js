import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Recommendations from '../components/Recommendations.vue' // ���� �Ƽ�

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/recommendations', name: 'Recommendations', component: Recommendations }// ���� �Ƽ�
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router
