import Vue from 'vue';
import Router from 'vue-router';
import Photos from '../components/Photos.vue';
import Ping from '../components/Ping.vue';
import Products from '../components/Products.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Photos',
      component: Photos,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/products',
      name: 'Products',
      component: Products,
    },
  ],
});
