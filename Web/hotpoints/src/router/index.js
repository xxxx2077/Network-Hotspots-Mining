import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView/HomeView')
  }, {
    path: '/menu',
    name: 'Menu',
    component: () => import('@/components/Menu'),
    redirect: '/menu/developing',
    children: [{
      path: '/menu/developing',
      name: 'Developing',
      component: () => import('@/components/Developing')
    }, {
      path: '/menu/topic',
      name: 'Topic',
      component: () => import('@/views/Topic/index')
    }]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
