import Vue from 'vue'
import App from './App.vue'
import '../plugins/vue-bootstrap';
import VueRouter from 'vue-router';


import Explore from "./components/Explore.vue";
import CreateBubble from "./components/CreateBubble.vue";
import BubbleDetails from "./components/BubbleDetails.vue";
import Settings from "./components/Settings.vue";
import VerifiedMods from "./components/VerifiedMods.vue";
import Login from "./components/Login.vue";
import Signup from "./components/Signup.vue";
import Active from "./components/Active.vue";



Vue.config.productionTip = false
Vue.use(VueRouter);


const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: "/", name: "Login", component: Login},
    { path: "/signup", name: "Signup", component: Signup},
    { path: "/explore", name: "Explore", component: Explore },
    { path: "/active", name: "Active", component: Active},
    { path: "/create", name: "CreateBubble", component: CreateBubble },
    { path: "/bubbledetails", name: "BubbleDetails", component: BubbleDetails},
    {path:"/settings", name:"Settings",component: Settings},
    {path:"/verifiedmods",name:"VerifiedMods", component: VerifiedMods},
  ]
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
