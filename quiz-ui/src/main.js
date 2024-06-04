import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import "./css/Scores.css";
import "./assets/main.css";

import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";

import SidebarNavVue from "./components/SidebarNav.vue";

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);

app.component("SidebarNav", SidebarNavVue);

app.mount("#app");
