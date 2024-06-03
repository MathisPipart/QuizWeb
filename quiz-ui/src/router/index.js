import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from "@/stores/userStores";

import HomePage from '@/views/HomePage.vue'
import AdminPage from '@/views/AdminPage.vue'
import NewQuizPage from '@/views/NewQuizPage.vue'
import QuestionsPage from '@/views/QuestionsPage.vue'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'home',
			component: HomePage
		},
		{
			path: '/admin',
			name: 'admin',
			component: AdminPage,
			meta: { requiresAuth: true }
		},
		{
			path: '/new-quiz',
			name: 'new-quiz',
			component: NewQuizPage,
		},
		{
			path: '/questions',
			name: 'questions',
			component: QuestionsPage,
		}
	]
});

router.beforeEach((to, from, next) => {
	if (to.path === "/admin" && !useUserStore().token) {
		next("/");
		return;
	}

	if (
		to.matched.some((record) => record.meta.requiresAuth) && !useUserStore().token
	) {
		next("/");
		return;
	}

	next();
});

export default router
