import Vue from 'vue';
import Router from 'vue-router';
import Photos from '../components/Photos.vue';
import Ping from '../components/Ping.vue';

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
  ],
});
